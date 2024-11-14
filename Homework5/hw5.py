"""
COMP 614
Homework 5: Bag of Words
"""

from collections import defaultdict
import math
import numpy as np
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
   # Define the regular expressions for each of the patterns to filter out
    patterns = [
        r'\{\{.*?\}\}',             
        r'\{\|.*?\|\}',              
        r'\[\[.*?\]\]',              
        r'\[.*?\]',                    
        r'<.*?>',                        
        r'&lt;.*?&gt;',                  
        r'File:'                         
    ]

    combined_pattern = '|'.join(patterns)

    text = re.sub(combined_pattern, ' ', text)

    punctuation_to_remove = "[" + string.punctuation + "](?![st]\\s)"
    text = re.sub(punctuation_to_remove, ' ', text)
    text = text.lower()

    words = text.split()
    return words


def count_words(words):
    """
    Given a list of words, returns the total number of words as well as a 
    dictionary mapping each unique word to its frequency of occurrence.
    """
    count = defaultdict(int)
    for word in words:
        count[word] += 1
    return len(words), count


def count_all_words(filenames):
    """
    Given a list of filenames, returns three things. First, a list of the titles,
    where the i-th title corresponds to the i-th input filename. Second, a
    dictionary mapping each filename to an inner dictionary mapping each unique
    word in that file to its relative frequency of occurrence. Last, a dictionary 
    mapping each unique word --- including all words found across all files --- 
    to its total frequency of occurrence across all of the input files.
    """
    all_titles = []
    title_to_counter = {}
    total_counts = defaultdict(int)

    for filename in filenames:
        title, text = get_title_and_text(filename)
        all_titles.append(title)

        words = get_words(text)
        total_words, word_count = count_words(words)

        normalized_counter = {word: count / total_words for word, count in word_count.items()}
        title_to_counter[title] = normalized_counter

        for word, count in word_count.items():
            total_counts[word] += count

    return all_titles, title_to_counter, dict(total_counts)


def encode_word_counts(all_titles, title_to_counter, total_counts, num_words):
    """
    Given two dictionaries in the format output by count_all_words and an integer
    num_words representing the number of top words to encode, finds the top 
    num_words words in total_counts and builds a matrix where the element in 
    position (i, j) is the relative frequency of occurrence of the j-th most 
    common overall word in the i-th article (i.e., the article corresponding to 
    the i-th title in titles).
    """
    sorted_words = sorted(total_counts.items(), key=lambda tup: (-1 * tup[1], tup[0]))
    top_words = [word for word, _ in sorted_words[:num_words]]
    
    # Init an empty matrix
    matrix = np.zeros((len(all_titles), len(top_words)))
    
    for idx, title in enumerate(all_titles):
        word_counts = title_to_counter.get(title, {})
        
        for jdx, word in enumerate(top_words):
            # get the relative frequency of the j-th most common word in the i-th article
            matrix[idx, jdx] = word_counts.get(word, 0.0)
    
    return matrix


def nearest_neighbors(matrix, all_titles, title, num_nbrs):
    """
    Given a matrix, a list of all titles whose data is encoded in the matrix, such
    that the i-th title corresponds to the i-th row, a single title whose data is
    encoded in the matrix, and the desired number of neighbors to be found, finds 
    and returns the closest neighbors to the article with the given title.
    """
    if title not in all_titles:
        raise ValueError("The provided title is not in the list of all titles.")

    target_index = all_titles.index(title)

    target_vector = matrix[target_index]

    # distance between the target vector and all other vectors
    distances = []
    for idx, vector in enumerate(matrix):
        if idx != target_index:  
            distance = np.linalg.norm(target_vector - vector)
            distances.append((all_titles[idx], distance))

    # Sort the distances in ascending order
    distances.sort(key=lambda x: x[1])
    num_nbrs = min(num_nbrs, len(all_titles) - 1)
    nearest_titles = [title for title, _ in distances[:num_nbrs]]

    return nearest_titles


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


# 1) Find the top 30 words in "rice_university.xml". 
# Provide the words and their (raw/absolute, not normalized) counts in the form
# of a list of tuples of (word, count), sorted in descending order.
def get_top_words_from_file(filename):
    """
    given a filename, this function prints the top 30 words by raw count in 
    descending order as a list of tuples (word, count).
    """
    _, text = get_title_and_text(filename)
    
    _, word_count_dict = count_words(get_words(text))
    
    sorted_words = sorted(word_count_dict.items(), key=lambda item: -item[1])
    top_words = sorted_words[:30]
    
    print("Top 30 words and their counts:")
    for word, count in top_words:
        print(f"{word}: {count}")

#get_top_words_from_file("wikipedia_articles/television.xml")
