# Machine Learning Project 1: Find the Higgs boson

## Contributors

* Florian Grötschla
* Adrien Bertaud
* Maximilian Wessendorf

## Description

This directory contains all code necessary to rerun our tests and get a model that we submitted on [AIcrowd challenge](https://www.aicrowd.com/challenges/epfl-machine-learning-higgs).

The goal of this challenge is to train a binary classifier to identify the appearance of the Higgs boson on a dataset of decay signatures from CERN. We compare various machine learning methods and apply different preprocessing steps that were introduced in class.

Finally, we fit a classification model with the least squares method that scores an accuracy of 0.82 and a F1-score of 0.722.

## Report

* **ML_P1_Find_the_Higgs.pdf**

## Notation
* **Feedbacks.pdf**

## Usage

Code was developed with the following versions:
* **Python** 3.7.6
* **NumPy** 1.18.1

To run the code that generates our predictions, first copy the the train and test datasets to /data/train.csv and /data/test.csv. It then suffices to run `run.py`, the predictions are then stored in result/result.csv.

The codebase is splitted into several files with different contents:
* **run.py**: to get our model
* **plot_lin_reg_GD.ipynb**: plot results with linear regression using gradient descent results
* **plot_least_squares.ipynb**: plot results with least square regression using gradient descent results
* **plot_ridge_regression.ipynb**: plot results with ridge regression results
* **plot_logistic_reg.ipynb**: plot results with logistic regression using gradient descent results
* **plot_reg_log_regr.ipynb**: plot results with regularized logistic regression using gradient descent results
* **run_methods.ipynb**: contains code we used to run each method with various parameters
* **implementations.py**: contains the 6 methods we had to implement and all functions that are necessary to execute them
* **evaluation.py**: functions to do the evaluation, such as splitting the data, the cross validation and computing different metrics
* **proj1_helpers.py**: functions provided for the project 1 like loading the data




