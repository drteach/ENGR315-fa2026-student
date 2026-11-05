"""
CULMINATING ASSIGNMENT 2: RSI

Create a program which will provide answers to the tasks posed in the assignment description.

For this assignment, you will start from scratch with this blank template.
It is your reponsibility to include all necessary program components in this file.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.

The relevant data file is named "all_participant_data_rsi.csv" and is located in data > drop-jump.

All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import chisquare, kurtosis, norm, skew, t, ttest_rel


# This relative path works when VS Code runs the script from its own folder.
data_file = Path("..") / ".." / "data" / "drop-jump" / "all_participant_data_rsi.csv"
data = pd.read_csv(data_file)

alpha = 0.05


# Task 1: Compare the two measurement methods for the same trials.
# The null hypothesis is that their average paired difference is zero.
# The alternative hypothesis is that their average paired difference is not zero.
paired_test = ttest_rel(data["force_plate_rsi"], data["accelerometer_rsi"])

print("TASK 1: Paired t-test")
print("H0: The mean paired difference (force plate - accelerometer) is 0.")
print("H1: The mean paired difference (force plate - accelerometer) is not 0.")
print(f"t-value: {paired_test.statistic:.4f}")
print(f"p-value: {paired_test.pvalue:.6g}")

if paired_test.pvalue < alpha:
    print("Decision: Reject the null hypothesis.")
    print(
        "Conclusion: The data provide evidence that the two methods have "
        "different average RSI measurements."
    )
else:
    print("Decision: Fail to reject the null hypothesis.")
    print(
        "Conclusion: The data do not provide sufficient evidence of a "
        "difference in the methods' average RSI measurements."
    )

print(f"Mean force plate RSI: {data['force_plate_rsi'].mean():.4f}")
print(f"Mean accelerometer RSI: {data['accelerometer_rsi'].mean():.4f}")


# Task 2: Fit a normal distribution and compare observed and expected counts.
accelerometer_rsi = data["accelerometer_rsi"].to_numpy()
fitted_mean, fitted_std = norm.fit(accelerometer_rsi)

# Six equal-probability bins keep the expected count in each bin above five,
# which is important for the chi-square approximation.
bin_probabilities = np.linspace(0, 1, 7)
bin_edges = norm.ppf(
    bin_probabilities,
    loc=fitted_mean,
    scale=fitted_std,
)
observed_counts, _ = np.histogram(accelerometer_rsi, bins=bin_edges)
expected_counts = np.full(
    len(observed_counts),
    len(accelerometer_rsi) / len(observed_counts),
)

# Two degrees of freedom are subtracted because the mean and standard
# deviation were estimated from the same data.
chi_square_test = chisquare(
    f_obs=observed_counts,
    f_exp=expected_counts,
    ddof=2,
)
accelerometer_skew = skew(accelerometer_rsi)
accelerometer_kurtosis = kurtosis(accelerometer_rsi)

print("\nTASK 2: Normal distribution chi-square goodness-of-fit test")
print(f"Fitted mean: {fitted_mean:.4f}")
print(f"Fitted standard deviation: {fitted_std:.4f}")
print(f"Chi-square statistic: {chi_square_test.statistic:.4f}")
print(f"p-value: {chi_square_test.pvalue:.4f}")

if chi_square_test.pvalue < alpha:
    print("Decision: Reject the normal-distribution fit.")
    print(
        "The observed counts differ from the fitted normal model. "
        "Skewness, outliers, or unusually heavy or light tails may contribute."
    )
else:
    print("Decision: The normal distribution is a reasonable fit (fail to reject).")
    print(
        f"The sample skewness is {accelerometer_skew:.3f}; a value near zero "
        "suggests little asymmetry. Its excess kurtosis is "
        f"{accelerometer_kurtosis:.3f}, suggesting a flatter shape than a "
        "normal distribution. The test does not prove normality."
    )

# Plot the RSI histogram and the fitted normal density curve.
plt.figure()
plt.hist(
    accelerometer_rsi,
    bins="auto",
    density=True,
    alpha=0.6,
    label="Accelerometer RSI",
)
curve_x = np.linspace(accelerometer_rsi.min(), accelerometer_rsi.max(), 300)
plt.plot(
    curve_x,
    norm.pdf(curve_x, loc=fitted_mean, scale=fitted_std),
    color="red",
    label="Fitted normal distribution",
)
plt.xlabel("RSI")
plt.ylabel("Probability density")
plt.title("Accelerometer RSI with Fitted Normal Distribution")
plt.legend()
plt.tight_layout()
plt.show()


# Task 3: Display Participant F's trials and calculate confidence intervals
# for each method's mean RSI.
participant_f = data[data["trial"].str.startswith("F_")]

print("\nTASK 3: Participant F trials")
print(participant_f)

print("\n95% confidence intervals for Participant F's mean RSI:")
for column, method_name in [
    ("force_plate_rsi", "Force plate"),
    ("accelerometer_rsi", "Accelerometer"),
]:
    measurements = participant_f[column]
    sample_mean = measurements.mean()
    standard_error = measurements.std(ddof=1) / np.sqrt(len(measurements))
    margin = t.ppf(0.975, df=len(measurements) - 1) * standard_error
    lower_bound = sample_mean - margin
    upper_bound = sample_mean + margin
    print(
        f"{method_name}: ({lower_bound:.4f}, {upper_bound:.4f}); "
        f"mean = {sample_mean:.4f}"
    )

print(
    "Participant F's confidence intervals overlap, so these trials alone do "
    "not show a clear difference in the methods' mean RSI. Overlap is not a "
    "formal test of the paired difference. The intervals describe uncertainty "
    "in the mean, not the range of individual trials."
)