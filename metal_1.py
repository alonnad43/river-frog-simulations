"""
Metal Data Analysis Module (Version 1)

Description:
Loads metal data from a CSV file, performs unit conversions, groups the data,
fits a linear model to diffusion data, computes the R² value, and plots the results.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf

def load_csv_file():
    """
    Loads data from a predefined CSV file.

    Returns:
    - DataFrame with the loaded data.
    """
    full_path = r"C:\Users\ramaa\Documents\frogsthriver\metal_data1.csv"
    if os.path.exists(full_path):
        print(f"File found: {full_path}")
        data_df = pd.read_csv(full_path)
        return data_df
    else:
        raise FileNotFoundError(f"File not found at: {full_path}")


def error_function(x, t, D):
    """
    Computes error function for C(x, t).

    Parameters:
    - x: Variable.
    - t: Time.
    - D: Diffusion coefficient.

    Returns:
    - Value of the error function.
    """
    return erf(x / (2 * np.sqrt(D * t)))


def linear_func(x, m, b):
    """
    Linear function for curve fitting.

    Parameters:
    - x: Independent variable.
    - m: Slope.
    - b: Intercept.

    Returns:
    - m*x + b
    """
    return m * x + b


# ===== FIRST GRAPH (Full Dataset) =====

data_df = load_csv_file()
print("Columns in the loaded CSV:", data_df.columns.tolist())

# Convert units:
# Convert Distance from µm to m (assumes column name is 'Distance'; corrected from 'Distence')
data_df['Distance_m'] = data_df['Distance'] * 1e-6
# Convert time from hours to seconds
data_df['time_s'] = data_df['hours'] * 3600

# Group data by hours to compute average and standard deviation
grouped = data_df.groupby('hours')
avg_distance_m = grouped['Distance_m'].mean()
std_distance_m = grouped['Distance_m'].std()

unique_hours = avg_distance_m.index.values
avg_distance_m_vals = avg_distance_m.values

# Convert hours to seconds and compute square root of time
time_seconds = unique_hours * 3600
sqrt_time_seconds = np.sqrt(time_seconds)

# Fit the linear function to the averaged data
popt, pcov = curve_fit(linear_func, sqrt_time_seconds, avg_distance_m_vals)
m, b = popt
perr = np.sqrt(np.diag(pcov))
m_err, b_err = perr

# Compute residuals and R² value
residuals = avg_distance_m_vals - linear_func(sqrt_time_seconds, m, b)
ss_res = np.sum(residuals ** 2)
ss_tot = np.sum((avg_distance_m_vals - np.mean(avg_distance_m_vals)) ** 2)
r_squared = 1 - (ss_res / ss_tot)

# Plot the first graph (full dataset)
plt.figure(figsize=(10, 6))
plt.plot(sqrt_time_seconds, avg_distance_m_vals, 'o', label='Averaged Data', linestyle='none')
x_line = np.linspace(min(sqrt_time_seconds), max(sqrt_time_seconds), 100)
y_line = linear_func(x_line, m, b)
plt.plot(x_line, y_line, 'r-', label='Linear fit')
plt.title('Diffusion distance as a function of sqrt(Time) (Full Data)')
plt.xlabel('√(Time) [s^{1/2}]')
plt.ylabel('Diffusion distance [m]')
plt.grid(True)
plt.legend(loc='lower right')

annotation_text = (
    f"Linear model: f(x) = p1*x + p2\n"
    f"p1 = {m:.4e} ± {m_err:.4e} [m/s^(1/2)]\n"
    f"p2 = {b:.4e} ± {b_err:.4e} [m]\n"
    f"R² = {r_squared:.4f}"
)
plt.text(0.05, 0.95, annotation_text, transform=plt.gca().transAxes,
         fontsize=10, verticalalignment='top',
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))
plt.savefig('diffusion_vs_time_root_averaged_full_SI.png', dpi=300)
plt.show()
plt.close()
