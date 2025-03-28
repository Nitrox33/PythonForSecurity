import argparse
import json
import os
""" INSTRUCTIONS
made to brute force a caesar cipher
    -i: text to decode
    -o: output file name
    -w: path to the dictionnary
    --print-only: print the output only
    
    example:
        python caesar_bruteForcer.py -i "khoor" -o "output.txt" -w "dico.json"
        python caesar_bruteForcer.py -i intput.txt -o output.txt -w words_dictionary.json
        python caesar_bruteForcer.py -i intput.txt -w words_dictionary.json --print-only
"""

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def import_dico(path):
    if not os.path.exists(path):
        print("The file does not exist")
        exit(1)
    with open(path, "r") as file:
        dico = json.load(file)
    return dico

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

def brute_forcer(text, path_dico, verbose=False):
    dico = import_dico(path_dico)
    best_matching_words = 0
    best_shift = 0
    for i in range(26):
        output = decode_caesar_cipher(text, i)  
        matching_words = 0
        for word in output.split():
            if word in dico:
                matching_words += 1
        if matching_words > best_matching_words:
            best_matching_words = matching_words
            best_shift = i
        print(f"Shift: {i}, matching words: {matching_words}")
        if verbose: print(output)
        
    
    print(f"Best shift: {best_shift}, matching words: {best_matching_words}")
    if best_matching_words == 0:
        print("No matching words found")
        return best_shift, "No matching words found"
    else:
        return best_shift, decode_caesar_cipher(text, best_shift)
        
    
if __name__ == "__main__":
    # Create the parser
    argument_parser = argparse.ArgumentParser(description="Caesar cipher")
    argument_parser.add_argument("-i", type=str, help="Text to cipher")
    argument_parser.add_argument("-o", type=str, help="Output file name")
    argument_parser.add_argument('-w', type=str, help="Path to the dictionnary")
    argument_parser.add_argument("--print-only", action="store_true", help="Print the output only")

    # Parse the arguments
    args = argument_parser.parse_args()

    # check inputs
    if not args.i:
        print("You must provide a text to decode")
        exit(1)
    if not args.o and not args.print_only:
        print("You must provide an output file name")
        exit(1)
    if not args.w:
        print("You must provide a path to the dictionnary")
        exit(1)
    
    #import text
    if str(args.i).split(".")[-1] == "txt":
        print("the input is a file")
        if not os.path.exists(args.i):
            print("The file does not exist")
            exit(1)
        with open(args.i, "r") as file:
            text = file.read()
    else:
        text = args.i
    
    # brute force
    best_shift, output_text = brute_forcer(text, args.w)
    
    # Print or save the output
    if args.print_only:
        print(output_text)
    else:
        with open(args.o, "w") as file:
            file.write(output_text)
    