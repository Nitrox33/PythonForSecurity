# This script is a simple implementation of the transposition ciphering
# imports
import argparse
import os
import numpy as np
from colorama import Fore, Style
import doctest

# define
def table_transpose(text:str, n:int, verbose:bool=False) -> str:
    """
    Transpose a table with a key.
    For example the text "hello im max" with a key of 3 columns will be transposed as follow:
    h e l
    l o _
    i m _ 
    m a x
    =>  
    h l i m
    e o m a
    l _ _ x
    => 'hlimeomal  x'
    >>> table_transpose("hello im max", 3)
    'hlimeomal  x'
    >>> table_transpose("This is a test", 3)
    'Tss sh  ttiiae '
    """
    if len(text) % n != 0: # the text must be a multiple of n, if not we add spaces
        text += " " * (n - len(text) % n)
    table = np.array([list(text[i:i+n]) for i in range(0, len(text), n)])
    if verbose: print(table)
    if verbose: print("transposed:")
    if verbose: print(table.T)
    table = ''.join(table.T.flatten())
    return table

def error(message: str) -> None:
    print(Fore.RED + Style.BRIGHT + message + Style.RESET_ALL)
    os._exit(1)

def indicator(message: str) -> None:
    print(Fore.GREEN + message + Style.RESET_ALL)

def main():
    # Create the parser
    argument_parser = argparse.ArgumentParser(description="Caesar cipher")
    argument_parser.add_argument("-i", type=str, help="Text to cipher")
    argument_parser.add_argument("-o", type=str, help="Output file name")
    argument_parser.add_argument("-K", type=int, help="Number of columns")
    argument_parser.add_argument("-e", action="store_true", help="Encode")
    argument_parser.add_argument("-d", action="store_true", help="Decode")
    argument_parser.add_argument("-v", '--verbose', action="store_true", help="Verbose mode")

    # Parse the arguments
    args = argument_parser.parse_args()

    # Check the arguments
    if not args.i:
        error("You must provide a text to cipher with the -i option")
    if not args.o:
        args.print_only = True
    if not args.K:
        error("You must provide the number of columns with the -K option")
    if not args.e and not args.d:
        error("You must provide an action: -e for encoding and -d for decoding")
        
    if args.d: # if we are decoding we need to calculate the number of rows from the length of the text
        args.K = len(args.i) // args.K if len(args.i) % args.K == 0 else len(args.i) // args.K + 1

    """ --- --- --- --- --- Checking if the input is a file or a text  --- --- --- --- ---"""

    # Check if the input is a file or just a string
    if str(args.i).split(".")[-1] == "txt":
        indicator("file input detected...")
        if not os.path.exists(args.i):
            error("The file does not exist")
        with open(args.i, "r") as file:
            text = file.read()
    else:
        text = args.i
    
    """ --- --- --- --- --- Process the text  --- --- --- --- ---"""
    
    output = table_transpose(text, args.K, args.verbose)
    
    # Print or save the output
    if args.print_only:
        print(f"'{output}'")
    else:
        with open(args.o, "w") as file:
            file.write(output)
            

if __name__ == "__main__":
    doctest.testmod()
    main()