"""
COMP 614
Homework 3: Stock Prediction
"""

import comp614_module3 as stocks
import random
from collections import defaultdict

def markov_chain(data, order):
    """
    Creates and returns a Markov chain with the given order from the given data.

    inputs:
        - data: a list of ints or floats representing previously collected data
        - order: an integer repesenting the desired order of the Markov chain

    returns: a dictionary that represents the Markov chain
    """
    if order < 1:
        raise ValueError("Order of the Markov chain must be at least 1.")
    
    chain = defaultdict(lambda: defaultdict(int))
    
    for idx in range(len(data) - order):
        # get the current state
        current_state = tuple(data[idx:idx+order])
        next_bin = data[idx+order]
        
        chain[current_state][next_bin] += 1
    
    # normalize transitions for probabilities
    for _, transitions in chain.items():
        total_transitions = sum(transitions.values())
        for next_state in transitions:
            transitions[next_state] /= total_transitions
    
    return dict(chain)


def predict(model, last, num):
    """
    Predicts the next num values given the model and the last values.

    inputs:
        - model: a dictionary representing a Markov chain
        - last: a list (with length of the order of the Markov chain)
                representing the previous states
        - num: an integer representing the number of desired future states

    returns: a list of integers that are the next num states
    """
    predictions = []
    current_state = tuple(last)

    for _ in range(num):
        if current_state in model:
            next_states = list(model[current_state].keys())
            probabilities = list(model[current_state].values())
            
            cumulative_probabilities = []
            cumulative_sum = 0
            for prob in probabilities:
                cumulative_sum += prob
                cumulative_probabilities.append(cumulative_sum)
            
            rand_value = random.random()
            for idx, cumulative_prob in enumerate(cumulative_probabilities):
                if rand_value <= cumulative_prob:
                    next_value = next_states[idx]
                    break
        else:
            # randomly choose between 0 and 3 if state not in model
            next_value = random.randint(0, 3)

        predictions.append(next_value)
        current_state = tuple(list(current_state[1:]) + [next_value])
    
    return predictions

def mse(result, expected):
    """
    Calculates the mean squared error between two data sets. Assumes that the 
    two data sets have the same length.
    
    inputs:
        - result: a list of integers or floats representing the actual output
        - expected: a list of integers or floats representing the predicted output

    returns: a float that is the mean squared error between the two data sets
    """
    error = 0
    for idx in range(len(result)):
        error += (expected[idx] - result[idx])**2   
        
    mse_value = error / len(result)
    return float(mse_value)


def run_experiment(train, order, test, future, actual, trials):
    """
    Runs an experiment to predict the future of the test data based on the
    given training data.

    inputs:
        - train: a list of integers representing past stock price data
        - order: an integer representing the order of the markov chain
                 that will be used
        - test: a list of integers of length "order" representing past
                stock price data (different time period than "train")
        - future: an integer representing the number of future days to
                  predict
        - actual: a list representing the actual results for the next
                  "future" days
        - trials: an integer representing the number of trials to run

    returns: a float that is the mean squared error over the number of trials
    """
    model = markov_chain(train, order)
    
    total_mse = 0.0
    for _ in range(trials):
        predictions = predict(model, test, future)
        
        error = mse(predictions, actual)
        
        total_mse += error
    
    average_mse = total_mse / trials
    
    return average_mse


def run():
    """
    Runs the stock prediction application. You should not modify this function!
    """
    # Get the supported stock symbols
    symbols = stocks.get_supported_symbols()

    # Load the training data
    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

    # Load the test data
    testchanges = {}
    testbins = {}
    for symbol in symbols:
        testprices = stocks.get_test_prices(symbol)
        testchanges[symbol] = stocks.compute_daily_change(testprices)
        testbins[symbol] = stocks.bin_daily_changes(testchanges[symbol])

    # Display data
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

    # Run experiments
    orders = [1, 3, 5, 7, 9]
    ntrials = 500
    days = 5

    for symbol in symbols:
        print(symbol)
        print("====")
        print("Actual:", testbins[symbol][-days:])
        for order in orders:
            error = run_experiment(bins[symbol], order,
                                   testbins[symbol][-order-days:-days], days,
                                   testbins[symbol][-days:], ntrials)
            print("Order", order, ":", error)
        print()

        
# You may want to keep this call commented out while you're writing & testing
# your code. Uncomment it when you're ready to run the experiments.
run()