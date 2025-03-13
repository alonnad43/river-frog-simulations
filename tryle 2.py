"""
Metal Data Analysis Module (Version 2)

Description:
Alternative version for analyzing metal diffusion data. Loads CSV data,
performs unit conversions (keeping Distance in µm), groups the data,
fits a linear model, computes the R² value, and plots the result.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def load_csv_file():
    """
    Loads metal data from a CSV file.

    Returns:
    - DataFrame with metal data.
    """
    full_path = r"C:\Users\ramaa\Documents\frogsthriver\metal_data1.csv"
    if os.path.exists(full_path):
        data_df = pd.read_csv(full_path)
        return data_df
    else:
        raise FileNotFoundError(f"File not found at: {full_path}")


def linear_func(x, m, b):
    """
    Linear function for fitting.

    Parameters:
    - x: Independent variable.
    - m: Slope.
    - b: Intercept.

    Returns:
    - m*x + b
    """
    return m * x + b


# ===== Process Data (Filtered Version) =====

data_df = load_csv_file()

# Convert time from hours to seconds
data_df['time_s'] = data_df['hours'] * 3600

# Group data by hours and compute average distance (µm)
grouped = data_df.groupby('hours')
avg_distance_um = grouped['Distance'].mean()  # Corrected from 'Distence'
std_distance_um = grouped['Distance'].std()

unique_hours = avg_distance_um.index.values
avg_distance_vals = avg_distance_um.values

time_seconds = unique_hours * 3600
sqrt_time_seconds = np.sqrt(time_seconds)

# Fit the linear model to the averaged data
popt, pcov = curve_fit(linear_func, sqrt_time_seconds, avg_distance_vals)
m, b = popt
perr = np.sqrt(np.diag(pcov))
m_err, b_err = perr

# Compute R² for the filtered dataset
residuals = avg_distance_vals - linear_func(sqrt_time_seconds, m, b)
ss_res = np.sum(residuals ** 2)
ss_tot = np.sum((avg_distance_vals - np.mean(avg_distance_vals)) ** 2)
r_squared = 1 - (ss_res / ss_tot)

# Plot the filtered data graph
plt.figure(figsize=(10, 6))
plt.plot(sqrt_time_seconds, avg_distance_vals, 'o', label='Averaged Data (Filtered)', linestyle='none')
x_line = np.linspace(min(sqrt_time_seconds), max(sqrt_time_seconds), 100)
y_line = linear_func(x_line, m, b)
plt.plot(x_line, y_line, 'r-', label='Linear fit')
plt.title('Diffusion distance as a function of sqrt(Time) (Filtered Data)')
plt.xlabel('√(Time) [s^{1/2}]')
plt.ylabel('Diffusion distance [µm]')
plt.grid(True)
plt.legend(loc='lower right')

annotation_text = (
    f"Linear model: f(x) = p1*x + p2\n"
    f"p1 = {m:.4f} ± {m_err:.4f} [µm/s^(1/2)]\n"
    f"p2 = {b:.4f} ± {b_err:.4f} [µm]\n"
    f"R² = {r_squared:.4f}"
)
plt.text(0.05, 0.95, annotation_text, transform=plt.gca().transAxes,
         fontsize=10, verticalalignment='top',
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))
plt.savefig('diffusion_vs_time_root_averaged_filtered_um.png', dpi=300)
plt.show()
plt.close()
