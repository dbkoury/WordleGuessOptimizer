# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:11:24 2022

@author: dylankoury
"""
'''
WORDLE GUESSER ALGORITHM
    This algorithm was built to provide the best wordle guesses 
    depending on data from prior guesses. This data can be input
    in the "Input Data" section, the only section that should be edited.
    It will return a list of words ranked from a likelihood score,
    which is is determined by the prevalence of letters in the word
    when compared to every remaining word given the constraints.
'''

    #IMPORT LIBRARIES
import pandas as pd #library to create and manipulate dataframe
import numpy as np #library to remove duplicate words
import string #library with alphabet list
from nltk.corpus import words #library that contains list of all words in english dictionary
pd.set_option('mode.chained_assignment', None) #hiding warning messages

   #INPUT DATA -- (ONLY PART OF CODE THAT NEEDS TO BE EDITED EACH ROUND)
TopN = 10  #The number of word suggestions you want printed
guess_num = 1 #The guess number you are on
l1 = "" #First letter if position confirmed (should be green on wordle)
l2 = "" #Second letter 
l3 = "" #Third letter
l4 = "" #Fourth letter
l5 = "" #Fifth letter
contains = [""] #Any letters confirmed to be in word but position not certain (yellow on wordle)
not_contains = [] #any letters confirmed to not be in the word (grey on wordle)


   #CREATING WORD AND LETTER LISTS
word_list = [word.lower() for word in list(words.words())] #make all words lowercase
word_list = list(filter(lambda word: len(word) == 5, word_list)) #limiting word list to five letter words
word_list = list(np.unique(np.array(word_list))) #removing duplicate words
word_list = list(str(word) for word in word_list) #changing variable type back to string
alphabet = list(string.ascii_lowercase) #importing list of alphabet letters
alphabet = list(filter(lambda letter: letter not in [word for word in word_list], alphabet)) #removing letters not in words list
    
    #LIMITING WORD LIST BASED ON INPUTS
for i in range(5): #for each letter in 5 letter word
    if globals()[f"l{i+1}"] in alphabet: #if the letter exists in the alphabet (else input not valid)
        word_list = list(filter(lambda word: globals()[f"l{i+1}"] in word[i], word_list)) #filter word list to only include words with letter in the "i" position
    elif globals()[f"l{i+1}"] != "": #else if not blank guess
        print(f"Error: Postion {i} letter not valid letter") #error message for invalid input
for i in contains: #for each letter in the "contains" input
    if i in alphabet:
        word_list = list(filter(lambda word: i in word, word_list)) #filtering words list to only include words with this letter
    elif i != "":
        print(f"Error: Contains list {i} letter not valid letter") #error message for invalid input
for i in not_contains: #for each letter in the "not_contains" input
    if i in alphabet:
        word_list = list(filter(lambda word: i not in word, word_list)) #filtering words list to only include words without this letter
    elif i != "":
        print(f"Error: Not Contains list {i} letter not valid letter") #error message for invalid input

    #FINDING BEST GUESSES
Best_Letters = pd.DataFrame(data=alphabet,index=alphabet, columns=["Letter"]) #build best letters dataframe
Best_Letters['Count']=0 #set count of each letter to zero
for letter in alphabet: #for each letter
    count = 0 #count is zero
    for word in word_list: #for each word in word list
        for char in word: #for each character in the word from the word list
            if letter == char: #if that letter appears in the word
                count += 1 #increase the count by one
    Best_Letters["Count"][letter] += count #change the count for that letter to the total count
Best_Guesses = pd.DataFrame(data=word_list,index=word_list, columns=["Word"]) #build best guesses dataframe
Best_Guesses['Count']=0 #set count to zero
for letter in alphabet: #for each letter in the alphabet
    for word in word_list: #for each word in the word list
        if letter in word: #if the letter appears in the word
            Best_Guesses['Count'][word]+=Best_Letters["Count"][letter] #add the letters count value to the word
Best_Guesses = Best_Guesses.sort_values('Count',ascending=False,ignore_index=True) #sort by words with highest value (this will ensure the words with the most common letters are at the top)
print("Total guesses: ",guess_num,"\nGuesses left: ",6-guess_num) #print guess values
if len(Best_Guesses) < TopN: #if the number of words existing given the parameters is less than the number of words requested
    TopN = len(Best_Guesses) #set the number of words existing to the "Top N"
print(f"Top {TopN} Guesses:")
for i in range(TopN): #print the "Top N" best guesses (if "N" is 10, it will print 10 words)
    print(i+1,"\t\t",Best_Guesses["Word"][i]) 
