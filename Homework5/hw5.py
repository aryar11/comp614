"""
COMP 614
Homework 5: Bag of Words
"""

import math
import numpy
import re
import string
import comp614_module5

def get_title_and_text(filename):
    """
    Given the name of an XML file, extracts and returns the strings contained 
    between the <title></title> and <text></text> tags, supporting multi-line content.
    """
    title = ""
    text = ""
    in_text_tag = False  

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Title
            if "<title>" in line and "</title>" in line:
                start = line.find("<title>") + len("<title>")
                end = line.find("</title>")
                title = line[start:end]

            # Text
            if in_text_tag:
                if "</text>" in line:
                    end = line.find("</text>")
                    text += line[:end]
                    in_text_tag = False
                else:
                    text += line

            elif "<text" in line:
                start = line.find('>') + 1
                if "</text>" in line:
                    end = line.find("</text>")
                    text += line[start:end]
                    in_text_tag = False
                else:
                    text += line[start:]
                    in_text_tag = True

    text = text.replace('\n', ' ')
    return title.strip(), text


def get_words(text):
    """
    Given the full text of an XML file, filters out the non-body text (text that
    is contained within {{}}, [[]], [], <>, etc.) and punctuation and returns a 
    list of the remaining words, each of which should be converted to lowercase.
    """
    return []


def count_words(words):
    """
    Given a list of words, returns the total number of words as well as a 
    dictionary mapping each unique word to its frequency of occurrence.
    """
    return 0, {}


def count_all_words(filenames):
    """
    Given a list of filenames, returns three things. First, a list of the titles,
    where the i-th title corresponds to the i-th input filename. Second, a
    dictionary mapping each filename to an inner dictionary mapping each unique
    word in that file to its relative frequency of occurrence. Last, a dictionary 
    mapping each unique word --- including all words found across all files --- 
    to its total frequency of occurrence across all of the input files.
    """
    return [], {}, {}


def encode_word_counts(all_titles, title_to_counter, total_counts, num_words):
    """
    Given two dictionaries in the format output by count_all_words and an integer
    num_words representing the number of top words to encode, finds the top 
    num_words words in total_counts and builds a matrix where the element in 
    position (i, j) is the relative frequency of occurrence of the j-th most 
    common overall word in the i-th article (i.e., the article corresponding to 
    the i-th title in titles).
    """
    return numpy.matrix([[]])


def nearest_neighbors(matrix, all_titles, title, num_nbrs):
    """
    Given a matrix, a list of all titles whose data is encoded in the matrix, such
    that the i-th title corresponds to the i-th row, a single title whose data is
    encoded in the matrix, and the desired number of neighbors to be found, finds 
    and returns the closest neighbors to the article with the given title.
    """
    return []


def run():
    """
    Encodes the wikipedia dataset into a matrix, prompts the user to choose an
    article, and then runs the knn algorithm to find the 5 nearest neighbors
    of the chosen article.
    """
    # Encode the wikipedia dataset in a matrix
    filenames = comp614_module5.ALL_FILES
    all_titles, title_to_counter, total_counts = count_all_words(filenames)
    mat = encode_word_counts(all_titles, title_to_counter, total_counts, 20000)

    # Print all articles
    print("Enter the integer corresponding to the article whose nearest" +
          " neighbors you would like to find. Your options are:")
    for idx in range(len(all_titles)):
        print("\t" + str(idx) + ". " + all_titles[idx])

    # Prompt the user to choose an article
    while True:
        choice = input("Enter your choice here: ")
        try:
            choice = int(choice)
            break
        except ValueError:
            print("Error: you must enter an integer between 0 and " +
                  str(len(all_titles) - 1) + ", inclusive.")

    # Compute and print the results
    nbrs = nearest_neighbors(mat, all_titles, all_titles[choice], 5)
    print("\nThe 5 nearest neighbors of " + all_titles[choice] + " are:")
    for nbr in nbrs:
        print("\t" + nbr)


# Leave the following line commented when you submit your code to OwlTest/CanvasTest,
# but uncomment it to perform the analysis for the discussion questions.
#run()
