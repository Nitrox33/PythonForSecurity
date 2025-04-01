# This script is a simple implementation of the caesar cipher
# import
import argparse
import os
import doctest
from sys import exit

# define
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def encode_caesar_cipher(text:str, decalage:int) -> str:
    """Encode a text using the caesar cipher
    Args:
        text (str): text to encode
        decalage (int): shift to the right
    Returns:
        str: encoded text
 
    >>> encode_caesar_cipher("hello", 3)
    'khoor'
    >>> [encode_caesar_cipher("test", i) for i in range(4)]
    ['test', 'uftu', 'vguv', 'whvw']
    """
    output = ""
    for letter in text.lower():
        if letter in alphabet: output += alphabet[(alphabet.index(letter)+decalage)%len(alphabet)]
        elif letter == " ": output += " "
        elif letter == "\n": output += "\n"
    return output

def decode_caesar_cipher(text:str, decalage:int) -> str:
    """decode a text using the caesar cipher
    Args:
        text (str): ciphered text to decode
        decalage (int): number of shift to the left
    Returns:
        str: decoded text    
    >>> decode_caesar_cipher("khoor", 3)
    'hello'
    >>> [decode_caesar_cipher("test", i) for i in range(4)]
    ['test', 'sdrs', 'rcqr', 'qbpq']
    """
    output = ""
    for letter in text.lower():
        if letter in alphabet: output += alphabet[(alphabet.index(letter)-decalage)%len(alphabet)]
        elif letter == " ": output += " "
        elif letter == "\n": output += "\n"
    return output

def main():
    # Create the parser
    argument_parser = argparse.ArgumentParser(description="Caesar cipher")
    argument_parser.add_argument("-i", type=str, help="Text to cipher")
    argument_parser.add_argument("-K", type=int, help="shift to the right when encoding and left when decoding")
    argument_parser.add_argument("-e", action="store_true", help="Encode")
    argument_parser.add_argument("-d", action="store_true", help="Decode")
    argument_parser.add_argument("-o", type=str, help="Output file name")
    argument_parser.add_argument("--print-only", action="store_true", help="Print the output only")

    # Parse the arguments
    args = argument_parser.parse_args()

    # Check the arguments
    if not args.i:
        print("You must provide a text to cipher with the -i option")
        exit(1)
    if not args.K:
        print("You must provide a shift value with the -K option")
        exit(1)
    if not args.e and not args.d:
        print("You must provide an action: -e for encoding or -d for decoding")
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
        with open(args.i, "r") as file:
            text = file.read()
    else:
        text = args.i
    

    # Process the text edit
    if args.e:
        output = encode_caesar_cipher(text, args.K)
    
    if args.d:
        output = decode_caesar_cipher(text, args.K)
    
    # Print or save the output
    if args.print_only:
        print(output)
    else:
        with open(args.o, "w") as file:
            file.write(output)


if __name__ == "__main__":
    doctest.testmod()
    main()
