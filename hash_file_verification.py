from Crypto.Hash import SHA256
from Crypto.Hash import SHA1
from Crypto.Hash import MD5
from colorama import Fore, Style
import os
import argparse

def error(message: str) -> None:
    print(Fore.RED + Style.BRIGHT + message + Style.RESET_ALL)
    os._exit(1)

def hash_file(file_path: str, hash_type: str) -> str:
    if hash_type == "sha1":
        h = SHA1.new()
    elif hash_type == "sha256":
        h = SHA256.new()
    elif hash_type == "md5":
        h = MD5.new()
    else:
        error("Invalid hash type")
        
    with open(file_path, "rb") as file:
        h.update(file.read())
    
    return h.hexdigest()

def main():
    argument_parser = argparse.ArgumentParser(description="Hash file verification")
    argument_parser.add_argument("-f", type=str, help="File to hash")
    argument_parser.add_argument("-t", type=str, help="Hash type (sha1, sha256, md5)")
    argument_parser.add_argument("--true-hash", type=str, help="The true hash of the file")
    
    args = argument_parser.parse_args()
    
    if not args.f:
        error("You must provide a file to hash with the -f option")
    else:
        if not os.path.exists(args.f):
            error("The file does not exist")
        
    if not args.t:
        error("You must provide a hash type with the -t option")
    
    hashed = hash_file(args.f, args.t)
    print(hashed)
    
    if args.true_hash:
        if hashed == args.true_hash:
            print('the hashes are the same')
        else:
            print("the hash are different")
            # test to change the hash to the true hash
    
if __name__ == "__main__":
    main()