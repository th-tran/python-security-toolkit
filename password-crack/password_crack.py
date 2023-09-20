from argparse import ArgumentParser
from crypt import crypt # crypt algorithm that hashes UNIX passwords

def crack_pwd(encrypted_pwd, dict_file_name):
    '''
    Attempt to crack password by iterating through words in a dictionary 
    until password is found or all words are exhausted.

    encrypted_pwd: str
        the hashed password
    dict_file_name: str
        the dictionary file name
    '''
    salt = encrypted_pwd[:2] # strip salt from the hashed password
    
    with open(dict_file_name) as dict_file:
        for word in dict_file.readlines():
            word = word.strip('\n')
            pwd_to_test = crypt(word, salt) # create a new hashed password using dictionary word and salt
            if pwd_to_test == encrypted_pwd: # match found
                print(f'[+] Found password: {word}\n')
                return
        print('[-] Password not found.\n')
        return

def main(pwd_file_name, dict_file_name):
    with open(pwd_file_name) as pwd_file:
        for line in pwd_file.readlines():
            if ':' in line:
                user = line.split(':')[0]
                encrypted_pwd = line.split(':')[1].strip()
                print(f'[*] Cracking password for: {user}')
                crack_pwd(encrypted_pwd, dict_file_name)

if __name__ == '__main__':
    parser = ArgumentParser(usage='password_crack.py PWDFILE DICTFILE') # initialize parser
    parser.add_argument('pwdfile', type=str, metavar='PWDFILE', help = "Specify password file")
    parser.add_argument('dictfile', type=str, metavar='DICTFILE', help = "Specify dictionary file")
    args = parser.parse_args()
    main(args.pwdfile, args.dictfile)