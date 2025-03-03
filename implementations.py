# -*- coding: utf-8 -*-
import numpy as np


def standardize(tx, tX_test):
    """
    We do the standardization by subtracting the mean and dividing by the standard derivation for each dimension to get features which have a mean of 0 and a standard derivation of 1.

    Some values of features in the dataset are set to $-999$ to indicate an error in the measurement.
    To handle the error values we compute standardization means and variances without taking into account those error values and then replace error values by zero.
    """

    threshold = 0.1
    value_to_remove = -999

    for i in range(tx.shape[1]):

        col = tx[:,i]
        col_te = tX_test[:,i]

        clean_col = col[col != value_to_remove]

        mean = np.mean(clean_col, axis=0)

        col[col == value_to_remove] = mean
        col_te[col_te == value_to_remove] = mean

        tx[:,i] = (col - mean)
        tX_test[:,i] = (col_te - mean)

        derivation = np.std(clean_col, axis=0)

        if derivation < threshold :
            print("Warning, derivation is too small, we don't normalize by derivation the column ", i)
        else:
            tx[:,i] = tx[:,i] / derivation
            tX_test[:,i] = tX_test[:,i] / derivation

    return tx, tX_test

def build_poly(tx,d):
    """ Compute polynomial expansion of degree d"""

    result = tx
    for degree in range(2,d+1):
        expansion = tx**degree
        expansion[tx == -999] = -999
        result = np.hstack((result,expansion))
    return result

def remove_rows_with_faulty_values(tx):
    """ Remove rows containing - 999 """
    is_valid = np.zeros(tx.shape[0])

    rows_without_error = 0
    for i in range(tx.shape[0]):
        contains_no_error = True
        for j in range(tx.shape[1]):
            if (tx[i,j] == -999):
                contains_no_error = False
                break
        if (contains_no_error):
            is_valid[i] = 1
            rows_without_error = rows_without_error + 1
    print('rows_without_error: ', rows_without_error)
    return tx[is_valid == 1]

def remove_columns_with_faulty_values(tx):
    """ Remove columns containing - 999 """
    is_valid = np.zeros(tx.shape[1])

    columns_without_error = 0
    for j in range(tx.shape[1]):
        contains_no_error = True
        for i in range(tx.shape[0]):
            if (tx[i,j] == -999):
                contains_no_error = False
                break
        if (contains_no_error):
            is_valid[j] = 1
            columns_without_error = columns_without_error + 1
    print('columns_without_error: ', columns_without_error)
    return is_valid

def batch_iter(y, tx, batch_size, num_batches=1, shuffle=True):
    """
    Generate a minibatch iterator for a dataset.
    Takes as input two iterables (here the output desired values 'y' and the input data 'tx')
    Outputs an iterator which gives mini-batches of `batch_size` matching elements from `y` and `tx`.
    Data can be randomly shuffled to avoid ordering in the original data messing with the randomness of the minibatches.
    Example of use :
    for minibatch_y, minibatch_tx in batch_iter(y, tx, 32):
    """
    data_size = len(y)

    if shuffle:
        shuffle_indices = np.random.permutation(np.arange(data_size))
        shuffled_y = y[shuffle_indices]
        shuffled_tx = tx[shuffle_indices]
    else:
        shuffled_y = y
        shuffled_tx = tx
    for batch_num in range(num_batches):
        start_index = batch_num * batch_size
        end_index = min((batch_num + 1) * batch_size, data_size)
        if start_index != end_index:
            yield shuffled_y[start_index:end_index], shuffled_tx[start_index:end_index]

def compute_loss(y, tx, w):
    """ Compute MSE loss"""
    e = y - tx.dot(w)
    return 1/(2*len(y)) * (e.T.dot(e))

def compute_gradient(y, tx, w):
    """ Compute gradient """
    err = y - tx.dot(w)
    return -1/len(y) * tx.T.dot(err)

def least_squares_GD(y, tx, initial_w, max_iters, gamma):
    """ Least squares regression with gradient descent """
    w = initial_w

    for n_iter in range(max_iters):
        gradient = compute_gradient(y, tx, w)
        w = w - gamma * gradient
    loss = compute_loss(y, tx, w)
    return w, loss

def least_squares_SGD(y, tx, initial_w, max_iters, gamma):
    """ Least squares regression with stochastic gradient descent """
    w = initial_w

    for n_iter in range(max_iters):
        for y_batch, tx_batch in batch_iter(y, tx, batch_size=2, num_batches=1):
            gradient = compute_gradient(y_batch, tx_batch, w)
            w = w - gamma * gradient
    loss = compute_loss(y, tx, w)
    return w, loss

def least_squares(y, tx):
    """ Least squares regression using normal equations"""
    w = np.linalg.solve(np.transpose(tx).dot(tx), np.transpose(tx).dot(y))
    loss = compute_loss(y, tx, w)
    return w, loss

def ridge_regression(y, tx, lambda_):
    """ Ridge regression using normal equations"""
    w = np.linalg.solve(np.transpose(tx).dot(tx) + (lambda_ * 2 * len(y) * np.identity(tx.shape[1])), np.transpose(tx).dot(y))
    loss = compute_loss(y, tx, w)
    return w, loss

def sigmoid(t):
    """Apply sigmoid function on t."""
    threshold = 1e2

    max_t = max(t)
    min_t = min(t)

    if min_t < -threshold or max_t > threshold:
        #print("WARNING: risk of overflow in exp : max = ", max(t),"\tmin = ", min(t))

        t[t > threshold] = threshold
        t[t < -threshold] = -threshold
        #print("Limiting values: max 2 = ", max(t),"\tmin 2 = ", min(t))

    exp = np.exp(-t)
    #print("exp = ",exp.shape)

    sig = 1.0 / (1 + exp)
    return sig

def calculate_log_likelihood_loss(y, tx, w):
    """Compute the loss by negative log likelihood."""
    threshold = 1e-9

    x_hat = tx.dot(w)
    pred = sigmoid(x_hat)

    mask_inf_to_min = (pred < threshold)
    mask_sup_to_max =(pred >= 1-threshold)

    if len(pred[mask_inf_to_min]) > 0 :
        pred[mask_inf_to_min] = threshold

    if len(pred[mask_sup_to_max]) > 0 :
        pred[mask_sup_to_max] = 1-threshold

    loss = y.T.dot(np.log(pred)) + (1 - y).T.dot(np.log(1 - pred))
    loss = -loss

    return loss

def calculate_gradient_sigmoid(y, tx, w):
    """Compute the gradient of loss with sigmoid activation."""
    pred = sigmoid(tx.dot(w))
    grad = tx.T.dot(pred - y)
    return grad

def learning_by_gradient_descent(y, tx, w, gamma):
    """
    Do one step of gradient descent using logistic regression with gradient descent and return the updated w.
    """
    grad = calculate_gradient_sigmoid(y, tx, w)
    w -= gamma * grad
    return w

def logistic_regression(y, tx, initial_w, max_iters, gamma):
    """Logistic regression using gradient descent."""
    w = initial_w
    threshold = 1e-20
    losses = []

    y[y<0]=0

    for i in range(max_iters):

        if i % 50 == 0:
            loss = calculate_log_likelihood_loss(y, tx, w)
            print("Iteration = ", i, "\tloss = ", loss)

            losses.append(loss)

            if len(losses) > 1 and np.abs(losses[-1] - losses[-2]) < threshold:
                print("Loss is not evolving, stopping the loop at iteration : ", i)
                break

        w = learning_by_gradient_descent(y, tx, w, gamma)

    loss = calculate_log_likelihood_loss(y, tx, w)
    return w, loss

def calculate_grad_sigmoid_with_penalty(y, tx, w, lambda_):
    """Compute the gradient with simoid activation and penalty term."""
    grad = calculate_gradient_sigmoid(y, tx, w) + 2 * lambda_ * w
    return grad

def learning_by_GD_with_penalty(y, tx, w, gamma, lambda_):
    """Compute the gradient descent with simoid activation and penalty term."""
    grad = calculate_grad_sigmoid_with_penalty(y, tx, w, lambda_)
    w -= gamma * grad
    return w

def reg_logistic_regression(y, tx, lambda_, initial_w, max_iters, gamma):
    """Regularized logistic regression using gradient descent."""
    w = initial_w

    y[y<0]=0

    for i in range(max_iters):

        if i % 50 == 0:
            loss = calculate_log_likelihood_loss(y, tx, w) + lambda_ * w.T.dot(w)
            print("Iteration = ", i, "\tloss = ", loss)

        w = learning_by_GD_with_penalty(y, tx, w, gamma, lambda_)

    loss = calculate_log_likelihood_loss(y, tx, w)
    return w, loss
