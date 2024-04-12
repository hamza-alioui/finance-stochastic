import csv
import pandas as pd
import numpy as np

# Create def and executions


def option_MC(option_prices,T,dt,j,r):
    x = np.exp(-r*(T-j*dt))*np.mean(option_prices)
    return x

NMC = 100
Nt = 252
t = np.linspace(0,T,Nt)
dt = T/Nt

meana=[] # vector used for averaging on all the results, for better accuracy.

for l in range(100): # loop for 100 option prices that will be averaged

    S = np.zeros([NMC,Nt]) # array for stock prices
    S[:,0] = S0

    for j in range(0, Nt-1):
        S[:,j+1] = S[:,j]*np.exp((r-sigma**2/2)*dt + sigma*np.sqrt(dt)*np.random.normal(0,1, NMC))

for i in range(0,NMC):
    plt.plot(t,S[i,:])
plt.axhline(S0, color='green', label='Stock Price (95)')
plt.axhline(K, color='red',linestyle = 'dashed', label='Strike Price (90)')
plt.legend()
plt.title('Monte-Carlo simulation, n=1000')
plt.show()

ST = S[:, -1]  # final price

option_prices = np.zeros(NMC)  # vector to store option prices
for i in range(NMC):
    if ST[i] >= K + 10:
        option_prices[i] = 10
    elif ST[i] <= K:
        option_prices[i] = 0
    else:
        option_prices[i] = ST[i] - K

meana.append(option_MC(option_prices,T,dt,0,r))
# end loop for all the option prices

np.mean(meana)
