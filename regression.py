import numpy as np
from scipy. optimize import curve_fit
import matplotlib.pyplot as plt

def inv_function(x, a, b,c):
  return a / (x+b) + c
# Dataset for relationship between distance and area
x_data = ([1, 2, 3, 4, 5,10,15,25])
y_data = ([535,740, 850, 920, 975,1090,1135,1160])
# Linspace x for running the function
x = np.linspace(2, 200, 100) # Generate discrete plot points
# Use curve fit to fit the model to the data
params, covariance = curve_fit(inv_function, x_data, y_data)
print(f"Parameters: {params} I I Covariance: {covariance}" )
a_fit, b_fit,c_fit = params

x=3.4

y = a_fit / (x + b_fit) +c_fit

print(round((y/1000)/1.2,2))