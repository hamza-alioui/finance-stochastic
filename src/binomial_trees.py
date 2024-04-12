import csv
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

def eur_payoff_probability_sum(n, p, So, u, d, k):
    """
    Calculate the sum of probabilities in a binomial distribution
    up to a specified number of successes.

    Parameters:
        n (int): Number of step.
        So (int): Initial stock price.
        u (float): potential increase of So.
        d (float): potential decrease of So.
        k (int): strike price of the option for payoff

    Returns:
        float: Sum of probabilities for up to j successes.
    """
    call_sum_prob, put_sum_prob = 0, 0

    for j in range(n + 1):

        call_payoff_j = np.maximum(So*(u**j)*d**(n-j) - k, 0)

        put_payoff_j = np.maximum(k - So*(u**j)*d**(n-j), 0)

        prob_j = math.comb(n, j) * (p ** j) * ((1 - p) ** (n - j))

        call_sum_prob += prob_j*call_payoff_j

        put_sum_prob += prob_j*put_payoff_j

    return call_sum_prob, put_sum_prob

def binomial_tree_european_options(So, r, T, k, sigma, Nt):
    """
    Calculate the sum of probabilities in a binomial distribution
    up to a specified number of successes.

    Parameters:
        So (int): Initial stock price.
        r (float): Risk free rate (Neutral Risk).
        T (int): Maturity.
        Nt (int): Number of step.
        k (int): Strike price of the option for payoff.
        sigma (float): Standard deviations.
    Returns:
        Call (float): Option price for call
        Put (float): Option price for put
    """

    step = T/Nt # Maturity divided by the number of step

    # how to choose u & d:
    u = np.exp((r-(sigma**2)/2)*step + sigma*np.sqrt(step))
    d = np.exp((r-(sigma**2)/2)*step - sigma*np.sqrt(step))

    # how to calculate p (for neutral risk Q):
    p = (np.exp(r*step)-d)/(u-d)

    C_prob, P_prob = eur_payoff_probability_sum(Nt, p, So, u, d, k)

    # option price at t=0
    Call =np.exp(-r*T)*C_prob
    Put =np.exp(-r*T)*P_prob

    return Call, Put

def binomial_tree_american_options(So, r, T, k, sigma, Nt):
    """
	Calculate each step comparing the current and next branch
    payoff.

    Parameters:
        So (int): Initial stock price.
        r (float): Risk free rate (Neutral Risk).
        T (int): Maturity.
        Nt (int): Number of step.
        k (int): Strike price of the option for payoff.
        sigma (float): Standard deviations.
    Returns:
        Call (float): Option price for call
        Put (float): Option price for put

    """

    #precompute values
    dt = T/Nt

    # how to choose u & d:
    u = np.exp((r-(sigma**2)/2)*dt + sigma*np.sqrt(dt))
    d = np.exp((r-(sigma**2)/2)*dt - sigma*np.sqrt(dt))

    q = (np.exp(r*dt) - d)/(u-d)
    disc = np.exp(-r*dt)

    # initialise stock prices at maturity
    S = So * d**(np.arange(Nt,-1,-1)) * u**(np.arange(0,Nt+1,1))

    # option payoff
    P = np.maximum(0, k - S)
    C = np.maximum(0, S - k)

    # backward recursion through the tree
    for i in np.arange(Nt-1,-1,-1):
        S = So * d**(np.arange(i,-1,-1)) * u**(np.arange(0,i+1,1))

        P[:i+1] = disc * ( q*P[1:i+2] + (1-q)*P[0:i+1] )
        P = P[:-1]
        P = np.maximum(P, k - S)

        C[:i+1] = disc * ( q*C[1:i+2] + (1-q)*C[0:i+1] )
        C = C[:-1]
        C = np.maximum(C, S - k)

    return C[0], P[0]

def binomial_tree_bermudian_call(S, K, T, r, sigma, N):
    """
    Not ready
    """
    delta_t = T / N
    u = math.exp(sigma * math.sqrt(delta_t))
    d = 1 / u
    #u= 1.02
    #d=0.98
    p = (math.exp(r * delta_t) - d) / (u - d)
    dates = [ int(k*N/12) for k in range(1,13)]
    option_price = np.zeros((N+1,N+1))


    for i in range(N + 1):
        option_price[N,i] = np.maximum(0,S * u**( i) * d**(N-i)-K)
        if (option_price[N,i] > K+10):
            option_price[N,i] = 10

    for k in range(N - 1, -1, -1):
        for i in range(k + 1):
            if k in dates:

                payoff = np.minimum(10,np.maximum(0,S * u** (i) * d**(k-i)-K))

                option_price[k,i] = np.maximum(payoff, np.exp(-r*delta_t) * (p * option_price[k+1,i] + (1 - p) * option_price[k+1,i+1]))


            else:

                option_price[k,i] = np.exp(-r*delta_t) * (p * option_price[k+1,i] + (1 - p) * option_price[k+1,i+1])


    return option_price[0,0]


def plot_option_prices(So, r, T, k, sigma, Nt_values):

    prices = [[] for j in range(4)] # 4: call_ame, call_ame, call_eur, put_eur


    for Nt in Nt_values:
        call_ame, put_ame = binomial_tree_american_options(So, r, T, k, sigma, Nt)
        call_eur, put_eur = binomial_tree_european_options(So, r, T, k, sigma, Nt)
        # Add Bermudian
        prices[0].append(call_ame)
        prices[1].append(put_ame)
        prices[2].append(call_eur)
        prices[3].append(put_eur)

    # Plot Call Option Prices
    plt.figure(figsize=(10, 6))
    plt.plot(Nt_values, prices[0], color='red', label='American')
    plt.plot(Nt_values, prices[2], color='blue', linestyle='dashed', label='European')
    plt.xlabel('Number of Steps')
    plt.ylabel('Call Option Price')
    plt.title('Call Option Prices Across Different Number of Steps')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot Put Option Prices
    plt.figure(figsize=(10, 6))
    plt.plot(Nt_values, prices[1], label='American', color='red')
    plt.plot(Nt_values, prices[3], color='blue', linestyle='dashed', label='European')
    plt.xlabel('Number of Steps')
    plt.ylabel('Put Option Price')
    plt.title('Put Option Prices Across Different Number of Steps')
    plt.legend()
    plt.grid(True)
    plt.show()

    return prices

if __name__ == "__main__":
	So = 100
	r = 0.06
	T = 5
	Nt_values = range(10, 400, 10) # Varying number of steps
	k = 100
	sigma = 0.25

	prices = plot_option_prices(So, r, T, k, sigma, Nt_values)


