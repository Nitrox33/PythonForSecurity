# This script is a simple implementation of the caesar cipher
# import
import argparse
import os
import random
import doctest

# define
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def encode(text:str, key_alphanet:str) -> str:
    """encode a text using the mono-alphabet cipher
    Args:
        text (str): text to encode
        key_alphanet (str): key alphabet - example: "srecmjvtpxuholgnzdywiakfqb"
    Returns:
        str: encoded text
    >>> encode("abcde", "srecmjvtpxuholgnzdywiakfqb")
    'srecm'
    """
    output = ""
    for letter in text.lower():
        if letter in alphabet: output += key_alphanet[alphabet.index(letter)]
        elif letter == " ": output += " "
        elif letter == "\n": output += "\n"
    return output

def decode(text:str, key_alphanet:str) -> str:
    """decode a text using the mono-alphabet cipher
    Args:
        text (str): ciphered text to decode
        key_alphanet (str): key alphabet - example: "srecmjvtpxuholgnzdywiakfqb"
    Returns:
        str: clear text
    >>> decode("srecm", "srecmjvtpxuholgnzdywiakfqb")
    'abcde'
    """
    output = ""
    for letter in text.lower():
        if letter in key_alphanet: output += alphabet[key_alphanet.index(letter)]
        elif letter == " ": output += " "
        elif letter == "\n": output += "\n"
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
    argument_parser.add_argument("-K",type=str, help="the key alphabet")
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
        print("WARNING ! no key alphabet provided, generating a random one...", end=" ")
        key = keyGenerator()
        args.K = key
        print(f"Key alphabet: {key}")
    elif len(args.K) != 26:
        print("The key alphabet must be 26 characters long")
        exit(1)
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
        output = encode(text, args.K)
    
    if args.d:
        output = decode(text, args.K)
    
    
    # Print or save the output
    if args.print_only:
        print("")
        print(output)
    else:
        with open(args.o, "w") as file:
            file.write(output)






if __name__ == "__main__":
    doctest.testmod()
    main()
