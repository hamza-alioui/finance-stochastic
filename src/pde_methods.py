import numpy as np
import matplotlib.pyplot as plt

# Create def and executions

# ---- Implicit Method

T =1
N = 200000

K=90
So = 95
upper_So = 150
lower_So = 50

M= 500

xmax = np.log(upper_So/So)
xmin = np.log(lower_So/So)


# the time step must be small than 1
dt = T/N
h = (xmax-xmin)/M
print('The value of alpha is',dt/h**2) # making sure we have the stability condition


# The constants for the equation
b = r*dt + 1 + dt*(sigma/h)**2
c = -r*dt/(2*h) - dt/(2*h)*(sigma**2)*(1/h-1/2)
a = c + (r-(sigma**2)/2)/h*dt


# Define the arrays for the stock price and time
x = np.linspace(xmin, xmax, M+1)
t = np.linspace(0, T, N+1)

# Define the initial and boundary conditions
V = np.zeros((N+1, M+1))
q=np.maximum(0,S0 * np.exp(x) - K)
V[N, :] = np.minimum(q, 10)

V[:, 0] = 0

for j in range(N+1):
    if S0*np.exp(xmax) >= K + 10:
        V[j,M] = 10* np.exp(-r*(T-j*dt))
    elif S0*np.exp(xmax) <= K:
        V[j,M] = 0
    else:
        V[j,M] = (S0*np.exp(xmax) - K)* np.exp(-r*(T-j*dt))

# Solve the equation using the explicit method

A = np.zeros((M-1, M-1))
for i in range(M-1):
    A[i, i] = b
    if i > 0:
        A[i, i-1] = a
    if i < M-2:
        A[i, i+1] = c

W = np.zeros((M-1)) # vector of boundary conditions

for i in range( N-1,-1,-1): # going backwards

    W[0] = -a * V[i,0]
    W[-1] = -c * V[i,-1]
    # Solve the matrix equation for V
    V[i,1:M] = np.dot(np.linalg.inv(A), V[i+1,1:M] + W)


# Plot the matrix
plt.imshow(V, origin='lower', extent=[50, 150, 0, 1], cmap='hot', aspect='auto')
plt.colorbar(label='Option Price')
plt.xlabel('Value of Stock Price')
plt.ylabel('Time')
plt.title(f'Option Price Matrix at T={T} for K={K}')
plt.show()

#------ Explicit Method

T =1
N = 200000

K=90
So = 95
upper_So = 150
lower_So = 50

M= 500

xmax = np.log(upper_So/So)
xmin = np.log(lower_So/So)


# Define the time and spatial step sizes
dt = T / N
h = (xmax - xmin) / M
print('The value of alpha is',dt/h**2) # making sure we have the stability condition

# Define the arrays for the stock price and time
x = np.linspace(xmin, xmax, M+1)
t = np.linspace(0, T, N+1)

# Define the initial and boundary conditions
V = np.zeros((N+1, M+1))
q=np.maximum(0,S0 * np.exp(x) - K)
V[N, :] = np.minimum(q, 10)
V[:, 0] = 0

for j in range(N+1):
    if S0*np.exp(xmax) >= K + 10:
        V[j,M] = 10* np.exp(-r*(T-j*dt))
    elif S0*np.exp(xmax) <= K:
        V[j,M] = 0
    else:
        V[j,M] = (S0*np.exp(xmax) - K)* np.exp(-r*(T-j*dt))
    # V[j,M] = 10

# Define the coefficients of the discretized equation

ce = ( 0.5 * r/h + (1/h - 1/2)* 0.5/h * sigma**2)*dt / (1+r*dt)
be = (1 -  dt * sigma**2/h**2) / (1+r*dt)
ae = (- 0.5 * r/h + (1/h + 1/2)* 0.5/h * sigma**2)*dt / (1+r*dt)

# Solve the equation using the explicit method
for i in range( N-1,-1,-1):

    for j in range(1, M):

        V[i, j] = ae*V[i+1, j-1] + be * (V[i+1, j]) + ce * (V[i+1, j+1] )

# for i in range(M+1):
#
#     plt.plot(t,V[:,i])
# plt.show()

# print("Option value at time 0: ", V[0, :])
# print("Option value at maturity T: ", V[N, :])
# Plot
plt.imshow(V, origin='lower', extent=[50, 150, 0, 1], cmap='hot', aspect='auto')
plt.colorbar(label='Option Price')
plt.xlabel('Value of Average Price')
plt.ylabel('Stock price')
plt.title(f'Option Price Matrix at T={T} for K={K}')
plt.show()
