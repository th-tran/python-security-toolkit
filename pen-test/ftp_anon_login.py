from argparse import ArgumentParser
import ftplib

def anon_login(hostname):
    ftp = ftplib.FTP(hostname, timeout=5)
    try:
        ftp.login('anonymous', 'me@your.com')
        print(f'\n[*] {str(hostname)} FTP anonymous logon succeeded.')
        return True
    except Exception as e:
        print(f'\n[-] {str(hostname)} FTP anonymous logon failed.')
        print(f'[-] Exception: {e}')
        return False
    finally:
        ftp.quit()

if __name__ == '__main__':
    parser = ArgumentParser(usage='ftp_anon_login.py TARGET_HOST')
    parser.add_argument('target_host', type=str, metavar='TARGET_HOST', help="Specify target host (IP address or domain name)")

    args = parser.parse_args()
    anon_login(args.target_host)