import numpy as np


def option_price(S, K, u, d, r, T):
    ''' Calculates the stock option for riskless portifolio.
    Parameters:
        S: stock current price
        K: price of buy
        u: increase percentage on the value of S; >1
        d: decrease percentage on the value of S; 0<x<1
        r: free risk rate
        '''


    option_value = S*u - K

    shares = option_value/S(u - d)

    Ptf = K - S*u(1 - shares)

    pft = Ptf*np.exp(-r*shares)

    opt_price1 = S*shares - pft

	# Based on the payoff at the maturity (European option)

    fu, fd = 1, 1

    shares = (fu - fd)/S(u - d)

    p = (np.exp(r*T)-d)/(u-d)

    opt_price2 = np.exp(r*T)*(p*fu+(1-p)*fd)

    return opt_price1, opt_price2


def option_payoff(r, T):
    ''' Calculates the option price considering branchs payoff.
    Parameters:
        r: free risk rate
        T: maturity
        '''




