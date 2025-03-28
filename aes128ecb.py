import argparse
from colorama import Fore, Style
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from random import randint

"""
Command line interface for the AES ECB encryption/decryption algorithm
using the pycryptodome library.

Usage:

python aes128ecb.py -i "text to cipher" -K "key" -o "output file name" -e
python aes128ecb.py -i input_file.txt -K key.key -d
python aes128ecb.py -i "0x5468697320697320612074657374" -K "0x546869732069732061206b6579" -o "output_file.bin" -d

To encode as file be sure to provide the file extension in the -i option
To encode as hexadecimal be sure to provide the 0x prefix in the -i option
To encode as binary be sure to provide the 0b prefix in the -i option
Else the input will be treated as a string (ascii encoding)

This also works for the key input
"""

def encrypt_aes_ecb(data: bytes, key: bytes,) -> bytes:
    """Encrypt the data with the key using the AES ECB mode
    Block size is 128 bits (16 bytes)
    The key and the data are padded in the process

    Args:
        data (bytes): Bytes to encrypt
        key (bytes): Key to use for encryption

    Returns:
        bytes: Encrypted data

    >>> encrypt_aes_ecb(b"this is a test", b"key")
    b'\n\x8d\xb0;\xee\xd4\x86B(2\xf5\xc8\x9d\xf1\x99\xf8'
    
    >>> encrypt_aes_ecb(b"this is a test", b"key").hex()
    '0a8db03beed486422832f5c89df199f8'
    
    """
    padded_key = pad(key, AES.block_size) # Pad the key to be a multiple of the block size
    cipher = AES.new(padded_key, AES.MODE_ECB) # Create a new AES cipher with the key in ECB mode
    padded_data = pad(data, AES.block_size) # Pad the data to be a multiple of the block size
    ciphertext = cipher.encrypt(padded_data) # Encrypt the padded data
    return ciphertext

def decrypt_aes_ecb(data: bytes, key: bytes) -> bytes:
    """Decrypt the data with the key using the AES ECB mode
    Block size is 128 bits (16 bytes)
    The key & data are padded in the process
    Args:
        data (bytes): Input data to decrypt
        key (bytes): Key to use for decryption

    Returns:
        bytes: Decrypted data
        
    >>> decrypt_aes_ecb(b'\n\x8d\xb0;\xee\xd4\x86B(2\xf5\xc8\x9d\xf1\x99\xf8', b"key")
    b'this is a test'
    """
    padded_key = pad(key, AES.block_size)  # Pad the key to be a multiple of the block size
    cipher = AES.new(padded_key, AES.MODE_ECB) # Create a new AES cipher with the key in ECB mode
    decrypted_data = cipher.decrypt(data) # decrypt the data
    original_data = unpad(decrypted_data, AES.block_size)# Unpad the decrypted data 
    return original_data

def keyGenerator(n:int) -> bytes:
    output = bytes()
    while len(output) < n:
        r = randint(33, 126)
        if r in [34, 39, 47, 92]: continue
        else: output += bytes([r])
    return output

def check_encoding(data: str) -> str:
    if data[:2] == "0x" and set(data[2:]) <= set("0123456789abcdef"): # Hexadecimal input detected
        return bytes.fromhex(data[2:]) 
    elif data[:2] == "0b" and set(data[2:]) <= set("01"): # Binary input detected
        return int(data[2:], 2).to_bytes()
    else:
        return data.encode('ascii')
    
def error(message: str):
    print(Fore.RED + Style.BRIGHT + message + Style.RESET_ALL)
    os._exit(1)
    
def indicator(message: str):
    print(Fore.GREEN + message + Style.RESET_ALL)
    
def main():
    # Create the parser
    argument_parser = argparse.ArgumentParser(description="AES ECB")
    argument_parser.add_argument("-i", type=str, help="Text to cipher")
    argument_parser.add_argument("-K", type=str, help="the key")
    argument_parser.add_argument("-o", type=str, help="Output file name")
    argument_parser.add_argument("-e", action="store_true", help="Encode")
    argument_parser.add_argument("-d", action="store_true", help="Decode")
    
    args = argument_parser.parse_args()
    
    #### Check the arguments
    if not args.i: # Check if the input is provided
        error("You must provide a text to cipher with the -i option")
    if not args.o:
        args.print_only = True
        
    if not args.e and not args.d:
        error("You must provide an action: -e for encoding and -d for decoding")
    elif args.e and args.d:
        error("You must provide only one action: -e for encoding and -d for decoding")
    if args.e and not args.K: # Check if the key is provided for encryption, if not generate a random one
        indicator("No key provided, creating a new one... (～￣▽￣)～")
        args.K = keyGenerator(AES.block_size)
        print(Style.BRIGHT + f" -> Key: {args.K.decode('ascii')}" + Style.RESET_ALL)
    if args.d and not args.K: 
        error("You must provide a key with the -K option")
    
    #### Check if the input is a file or just a string
    if str(args.i).split(".")[-1] == ["txt", "bin"]: 
        indicator("file input detected...")
        if not os.path.exists(args.i): 
            error("The file does not exist")
        with open(args.i, "rb") as file:
            text = file.read()
    else:
        text = check_encoding(args.i)
        
    if str(args.K).split(".")[-1]  in ["txt", "bin", "key"]:
        indicator("Key file input detected...")
        if not os.path.exists(args.K):
            error("The file does not exist")
        with open(args.K, "rb") as file:
            args.K = file.read()
    else:
        args.K = check_encoding(args.K)
    
    if len(args.K) > AES.block_size:
        args.K = args.K[:AES.block_size]
    
    # Process the text
    if args.e: output = encrypt_aes_ecb(text, args.K)
    else:      output = decrypt_aes_ecb(text, args.K)
    
    # Print or save the output
    if args.print_only:
        print("Output:")
        print(output.hex())
        try:
            print(output.decode('ascii'))
        except:
            pass
    else:
        with open(args.o, "wb") as file:
            file.write(output)
            
if __name__ == "__main__":
    main()