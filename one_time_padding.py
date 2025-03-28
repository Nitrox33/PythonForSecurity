import argparse
import os

def bytes_xor(a:bytes, b:bytes) -> bytes: return bytes(x^y for x,y in zip(a,b))

def bytes_to_bitstring(b:bytes) -> str: return ''.join(format(byte, '08b') for byte in b)

def bitstring_to_bytes(b:str) -> bytes: return bytes(int(b[i:i+8], 2) for i in range(0, len(b), 8))

def one_time_pad_encrypt(plaintext:bytes, key:bytes) -> bytes:
    if len(plaintext) != len(key): raise ValueError("Plaintext and key must have the same length")
    return bytes_xor(plaintext, key)

def main():
    """command line interface for the mono-alphabet cipher
    """
    # Create the parser
    argument_parser = argparse.ArgumentParser(description="Caesar cipher")
    argument_parser.add_argument("-i", type=str, help="Text to cipher")
    argument_parser.add_argument("-K", type=str, help="the keys alphabet")
    argument_parser.add_argument("-o", type=str, help="Output file name")
    argument_parser.add_argument("--print-only", action="store_true", help="Print the output only")
    
    # Parse the arguments
    args = argument_parser.parse_args()
    
    # Check the arguments
    if not args.i:
        print("You must provide a text to cipher with the -i option")
        exit(1)
    else:
        if os.path.exists(args.i):
            with open(args.i, "rb") as file:
                byte_input = file.read()
        else:
            print("file does not exist")
            exit(1)

    if not args.K:
        print("No key provided, creating a random one")
        args.K = os.urandom(len(byte_input))
        with open("key.bin", "wb") as file:
            file.write(args.K)
    else:
        if os.path.exists(args.K):
            with open(args.K, "rb") as file:
                args.K = file.read()
        else:
            print("key file does not exist")
            exit(1)
                
    if not args.o and not args.print_only:
        print("You must provide an output file name wtih the -o option")
        exit(1)
    
    # Process the text
    output = one_time_pad_encrypt(byte_input, args.K)
    
    # Print or save the output
    if args.print_only:
        print(output)
    else:
        with open(args.o, "wb") as file:
            file.write(output)

if __name__ == "__main__":
    main()