import matplotlib.pyplot as plt
import argparse
import os
from scipy.signal import savgol_filter

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

def find_most_common(text:str) -> int:
    freq = frequency_analysis(text)
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_freq[0][1]

def subsets(text, l=10,graph=False, verbose=False):
    histogram = []
    values = []
    for i in range(1,l):
        values.append(i)
        sub_text = text[::i]
        #freq = frequency_analysis(text[i-1::i])
        histogram.append(find_most_common(sub_text)/len(sub_text))
        #if verbose:print(f"the most frequent letter is: {find_e(text)} with {freq[find_e(text)]} occurences in {text[i-1::i]}") 
    if graph:
        plt.plot(values, histogram)
        plt.show()


if __name__ == "__main__":
    args_parse = argparse.ArgumentParser(description="Analyse the frequency of a subset of a text, and display the result on a graph")
    args_parse.add_argument('-i', '--input', type=str, help='file to analyse')
    args_parse.add_argument('-l', '--length', type=int, help='length of the subset')
    args_parse.add_argument('-v', '--verbose', action='store_true', help='verbose')
    args = args_parse.parse_args()
    
    if not args.input:
        print("You must provide a file to analyse")
        os._exit(1)
    
    if not args.length:
        print("You must provide a length for the subset")
        os._exit(1)
    
    with open(args.input, "r") as file:
        text = file.read()
    
    subsets(text, args.length, True, args.verbose)