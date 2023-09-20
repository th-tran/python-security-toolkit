from argparse import ArgumentParser
import nmap

def nmap_scan(target_host, target_ports):
    '''
    Provides a more in-depth scan (using additional scan types such as ACK, RST, FIN, and SYN-ACK) via nmap.

    target_host: str
        the host's IP address
    target_ports: list[str]
        the ports to scan
    '''
    nm_scan = nmap.PortScanner()
    for target_port in target_ports:
        nm_scan.scan(target_host, target_port)
        try:
            state = nm_scan[target_host]['tcp'][int(target_port)]['state']
            print(f'[*] {target_host} tcp/{target_port} {state}')
        except KeyError: # ip is unreachable
            print(f'Target host {target_host} is not reachable.')
            return

if __name__ == '__main__':
    parser = ArgumentParser(usage='nmap_scan.py TARGET_HOST -p TARGET_PORTS')
    parser.add_argument('target_host', type=str, metavar='TARGET_HOST', help="Specify target host's IP address")
    parser.add_argument('-p', required=True, type=str, metavar='TARGET_PORTS', help='Specify target port(s) comma separated (no spaces)')
    args = parser.parse_args()

    args.target_ports = str(args.p).split(',')
    nmap_scan(args.target_host, args.target_ports)