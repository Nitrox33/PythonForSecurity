# This script is a simple implementation of the caesar cipher
# import
import argparse
import os
import random
# define
"""Poly-alphabet cipher
This script is a simple implementation of the poly-alphabet cipher


To use it, you need to provide a text to cipher and a key alphabets.
You can also provide a file name to save the output.

example:
python poly_alphabet_cipher.py -i "hello" -K "defghijklmnopqrstuvwxyzabc" -o output.txt -e
python poly_alphabet_cipher.py -i INPUT.txt -K "defghijklmnopqrstuvwxyzabc" "bcdefghijklmnopqrstuvwxyza" -o output.txt -e
python poly_alphabet_cipher.py -i INPUT.txt -o output.txt -e # can create random keys

python poly_alphabet_cipher.py -i INPUT.txt -K "defghijklmnopqrstuvwxyzabc" "bcdefghijklmnopqrstuvwxyza" -d
"""


alphabet = 'abcdefghijklmnopqrstuvwxyz'

def encode(text:str, key_alphanets:list[str]) -> str:
    """Encode a text using the poly-alphabet cipher => for each letter in the text, we use a different key alphabet modulo the number of key alphabets
    Args:
        text (str): input text
        key_alphanets (list): list of key alphabets

    Returns:
        str: encoded text
        
    >>> encode("hello", ["defghijklmnopqrstuvwxyzabc", "bcdefghijklmnopqrstuvwxyza"])
    'kfomr'
    
    >>> encode("hello", ["ndjemywsxchlqizauvbkptrogf", "bcdefghijklmnopqrstuvwxyza", "cdefghijklmnopqrstuvwxyzab"])
    'sfnlp'
    
    the first letter is ciphered with the first key, the second letter with the second key, and so on...
    """
    output = ""
    for i,letter in enumerate(text.lower()):
        if letter in alphabet: output += key_alphanets[i%len(key_alphanets)][alphabet.index(letter)]
        else: output += letter
    return output

def decode(text:str, key_alphanets:list[str]) -> str:
    """Decode a text using the poly-alphabet cipher => for each letter in the text, we use a different key alphabet modulo the number of key alphabets
    Args:
        text (str): input text
        key_alphanets (list): list of key alphabets
    Returns:
        str: decoded text
    >>> decode("kfomr", ["defghijklmnopqrstuvwxyzabc", "bcdefghijklmnopqrstuvwxyza"])
    'hello'
    
    >>> decode("dbvmbw", ["ndjemywsxchlqizauvbkptrogf", "bcdefghijklmnopqrstuvwxyza", "cdefghijklmnopqrstuvwxyzab"])
    'bateau'
    """
    output = ""
    for i,letter in enumerate(text.lower()):
        if letter in alphabet: output += alphabet[key_alphanets[i%len(key_alphanets)].index(letter)]
        else: output += letter
    return output

def keyGenerator() -> str:  
    """run a random key alphabet for the mono-alphabet cipher
    Returns:
        str: a random key alphabet
    """
    key = list(alphabet)
    random.shuffle(key)
    return ''.join(key)

def main():
    """command line interface for the mono-alphabet cipher
    """
    # Create the parser
    argument_parser = argparse.ArgumentParser(description="Caesar cipher")
    argument_parser.add_argument("-i", type=str, help="Text to cipher")
    argument_parser.add_argument("-K",nargs="+", type=str, help="the keys alphabet")
    argument_parser.add_argument("-o", type=str, help="Output file name")
    argument_parser.add_argument("-e", action="store_true", help="Encode")
    argument_parser.add_argument("-d", action="store_true", help="Decode")
    argument_parser.add_argument( "--create-key", action="store_true", help="Create a random key alphabet and exit")
    argument_parser.add_argument("--print-only", action="store_true", help="Print the output only")

    # Parse the arguments
    args = argument_parser.parse_args()

    # Check the arguments
    if args.create_key:
        print(keyGenerator())
        exit(0)
    
    if not args.i:
        print("You must provide a text to cipher with the -i option")
        exit(1)
    
    if not args.K:
        print("WARNING ! no key alphabet provided, generating a random ones...", end=" ")
        i = input("how meny keys do you want to generate ? : (type exit to exit) ")
        if i == "exit":
            exit(0)
        keys = []
        for _ in range(int(i)):
            keys.append(keyGenerator())
        args.K = keys
        print(f"Key alphabet: {keys}")
    else:
        for key in args.K:
            if len(key) != 26:
                print("The key alphabet must be 26 characters long")
                exit(1)
        print(f"Key alphabet: {args.K}")
                
    if not args.e and not args.d:
        print("You must provide an action: -e for encoding and -d for decoding")
        exit(1)
    if args.e and args.d:
        print("You must provide only one action: -e for encoding and -d for decoding")
        exit(1)
    if not args.o and not args.print_only:
        print("You must provide an output file name wtih the -o option")
        exit(1)

    # Check if the input is a file or just a string
    
    if str(args.i).split(".")[-1] == "txt":
        print("file input detected...")
        if not os.path.exists(args.i):
            print("The file does not exist")
            exit(1)
        with open(args.i, "r", encoding='UTF-8') as file:
            text = file.read()
    else:
        text = args.i
    

    # Process the text
    if args.e:
        text = encode(text, args.K)
    
    if args.d:
        text = decode(text, args.K)
    
    
    # Print or save the output
    if args.print_only:
        print("")
        print(text)
    else:
        with open(args.o, "w") as file:
            file.write(text)


if __name__ == "__main__":
    main()
