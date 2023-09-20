from argparse import ArgumentParser
from threading import Thread
from zipfile import ZipFile
import os

Found = False
OPath = 'cracked_zip'

def extract_file(zip_file, password):
    '''
    Attempt to unzip file using given password.

    zip_file: str
        the zip file to unzip
    password: str
        the password to try
    '''
    global Found
    
    try:
        zip_file.extractall(path=OPath, pwd=password.encode('utf-8'))
        print(f'[+] Found password: {password}\n')
        print(f'[+] Unzipped in folder: {OPath}\n')
        # Set flag to true (zip was cracked)
        Found = True
    except:
        pass

def main(zip_file_name, dict_file_name):
    zip_file = ZipFile(zip_file_name)
    with open(dict_file_name) as dict_file:
        # spawn a new thread for each password to test
        threads = []
        for line in dict_file.readlines():
            password = line.strip('\n')
            t = Thread(target=extract_file, args=(zip_file, password))
            threads.append(t)
        # start all threads
        for t in threads:
            t.start()
        # wait for all threads to finish
        for t in threads:
            t.join()
        if not Found:
            print('[-] No password found.\n')
            os.rmdir(OPath)

if __name__  == '__main__':
    parser = ArgumentParser(usage='zip_crack.py ZIPFILE DICTFILE')
    parser.add_argument('zipfile', type=str, metavar='ZIPFILE', help='Specify zip file')
    parser.add_argument('dictfile', type=str, metavar='DICTFILE', help='Specify dict file')
    args = parser.parse_args()
    main(args.zipfile, args.dictfile)