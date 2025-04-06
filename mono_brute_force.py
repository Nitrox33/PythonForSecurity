import matplotlib.pyplot as plt
import argparse
import os

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def frequency_analysis(text:str) -> dict:
    """return the frequency of each letter in the text
    Args:
        text (str): text to analyse
    Returns:
        dict: frequency of each letter
    """
    freq = {i:0 for i in alphabet}
    for letter in text.lower():
        if letter in alphabet:
            if letter in freq:
                freq[letter] += 1
            else:
                freq[letter] = 1
    return freq

def addlabels(x,y,size=10):
    for i in range(len(x)):
        plt.text(i, y[i]//2, y[i], ha = 'center', fontsize=size)

def plot_frequency(freq:dict):
    """plot the frequency of each letter
    Args:
        freq (dict): frequency of each letter
    """
    plt.bar(freq.keys(), freq.values())
    addlabels(list(freq.keys()), list(freq.values()), size=7)
    plt.show()

def find_e(text:str) -> dict:
    freq = frequency_analysis(text)
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_freq[0][0]

if __name__ == "__main__":
    # Create the parser
    argument_parser = argparse.ArgumentParser(description="Caesar cipher")
    argument_parser.add_argument("-i", type=str, help="Text to cipher")
    argument_parser.add_argument("--graph", action="store_true", help="show the graph of the frequency of the letters")
    
    # Parse the arguments
    args = argument_parser.parse_args()
    
    # Check the arguments
    if not args.i:
        print("You must provide a text to cipher with the -i option")
        exit(1)
        
    # Check if the input is a file or just a string
    if str(args.i).split(".")[-1] in ["txt", "csv", "json", "xml"]:
        print("file input detected...")
        if not os.path.exists(args.i):
            print("The file does not exist")
            exit(1)
        with open(args.i, "r", encoding='UTF-8') as file:
            text = file.read()
    else:
        text = args.i
    # Frequency analysis
    freq = frequency_analysis(text)
    
    
    print(f"the most frequent letter is: {find_e(text)} with {freq[find_e(text)]} occurences")
    if args.graph:
        plot_frequency(freq)
    
    