"""
COMP 614
Homework 2: Statistics
"""

import math


def arithmetic_mean(data):
    """
    Given a list of numbers representing a data set, computes and returns 
    the arithmetic mean of the data set.
    """
    if(len(data) == 0):
        return None
    return sum(data)/len(data)


def pop_variance(data):
    """
    Given a list of numbers representing a data set, computes and returns 
    the population variance of the data set.
    """
    mean = arithmetic_mean(data)
    normalized = []

    for number in data:
        normalized.append((number - mean)**2)

    return arithmetic_mean(normalized)


def std_deviation(data):
    """
    Given a list of numbers representing a data set, computes and returns 
    the standard deviation of the data set.
    """
    return None if len(data) == 0 else math.sqrt(pop_variance(data))


def moving_avg(data, num_days):
    """
    Given a list of numbers representing a data set and an integer representing
    a number of days, builds and returns a new list where the i-th element is 
    the average of the data over the input number of days starting at position
    i in the data list.
    """
    if num_days <= 0:
        return None
    if num_days >= len(data):
        return [arithmetic_mean(data)]
    moving_averages = []
    for idx in range(len(data) - num_days + 1):
        window = data[idx:idx+num_days]
        average = arithmetic_mean(window)
        moving_averages.append(average)
    return moving_averages

def clean_with_deletion(data):
    """
    Given a list of lists representing a data set, cleans the data by creating
    and returning a new list of lists that contains the same data, minus any 
    rows that were originally missing values (denoted by None). Should not 
    mutate the original list.
    """
    cleaned_list = [data[0]] 

    for row in data[1:]:
        if None not in row:
            cleaned_list.append(row)
    return cleaned_list


def column_avgs(data):
    """
    Given a list of lists representing a data set, returns a new list where the
    i-th element is the arithmetic mean of the i-th column in the data set.
    """
    avg_list = []
    for idx in range(len(data[0])):
        column = [row[idx] for row in data[1:]]
        cleaned_column = [value for value in column if value is not None]
        if cleaned_column:  
            avg_list.append(arithmetic_mean(cleaned_column))
        else:
            avg_list.append(None)  
    return avg_list

def clean_with_mean(data):
    """
    Given a list of lists representing a data set, cleans the data by creating
    and returning a new list of lists that contains the same data, but with
    any values that were originally missing (denoted by None) filled in with 
    the arithmetic mean of the corresponding column.
    """
    avg_column = column_avgs(data)
    copy_data = [row.copy() for row in data] # Deep copy
    
    for row_index, row in enumerate(copy_data[1:], start=1):  
        for col_index, value in enumerate(row):
            if value is None:
                copy_data[row_index][col_index] = avg_column[col_index]
    
    return copy_data

