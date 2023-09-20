from argparse import ArgumentParser
import socket
import threading

def connection_scan(target_host, target_port):
    '''
    Identifies whether a port of given host is open or closed via TCP connect scan,
    and determines the specific service running on the port if open.

    target_host: str
        the hostname
    target_port: int
        the port to scan
    '''
    # ensure only one thread can output to screen at a time
    screen_lock = threading.Semaphore()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection_socket:
        try: # attempt to connect to port
            connection_socket.connect((target_host, target_port))
            # port is open, so send string of data to it and wait for response
            connection_socket.send(bytes('ViolentPython\r\n', 'utf-8'))
            # gather gleened info
            results = connection_socket.recv(100).decode('utf-8')
            screen_lock.acquire()
            print(f'[+] {target_port}/tcp open')
            print(f'    [>] {results}')
        except Exception as e: # port is closed
            screen_lock.acquire()
            print(f'Error: {e}')
            print(f'[-] {target_port}/tcp closed')
        finally: # release lock to allow other threads to print
            screen_lock.release()

def port_scan(target_host, target_ports):
    '''
    Scans the given host and each of its ports to determine which are open or closed.

    target_host: str
        the hostname
    target_ports: list[str]
        the ports to scan
    '''
    # first attempt to resolve an IP address to a hostname, if possible
    try:
        target_ip = socket.gethostbyname(target_host)
    except socket.herror:
        print(f'[-] Cannot resolve {target_host}: Unknown host')
        return
    
    try:
        target_name = socket.gethostbyaddr(target_ip)
        print(f'\n[+] Scan results for: {target_name[0]}')
    except socket.herror: # cannot resolve to hostname, so display IP address instead
        print(f'\n[+] Scan results for: {target_ip}')
    
    # scan each port
    socket.setdefaulttimeout(1)
    for port in target_ports:
        t = threading.Thread(target=connection_scan, args=(target_host, int(port)))
        t.start()

if __name__ == '__main__':
    parser = ArgumentParser(
        usage='port_scan.py TARGET_HOST -p TARGET_PORTS'
              '\nexample: python3 port_scan.py host.org -p 12,42')
    parser.add_argument('target_host', type=str, metavar='TARGET_HOST', help='Specify target host (IP address or domain name)')
    parser.add_argument('-p', required=True, type=str, metavar='TARGET_PORTS', help='Specify target port(s) comma separated (no spaces)')
    args = parser.parse_args()

    args.target_ports = str(args.p).split(',')
    port_scan(args.target_host, args.target_ports)