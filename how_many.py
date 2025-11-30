import math
from scipy.stats import norm

def required_trades(p, RR, conf=0.99, m=1):
    """
    p   = observed win rate (0.0–1.0)
    RR  = reward:risk ratio (e.g., 6 for 1:6)
    conf = desired confidence level (e.g., 0.99)
    m    = number of tuned parameters (Bonferroni correction)
    """

    # Break-even win rate
    p0 = 1 / (1 + RR)

    # Bonferroni-adjusted alpha and z-score
    alpha = 1 - conf
    alpha_adj = alpha / m
    z = norm.ppf(1 - alpha_adj)

    # Avoid invalid cases
    if p <= p0:
        return float("inf")

    # Binomial variance term
    var = p * (1 - p)

    # Effect size
    delta = p - p0

    # Required sample size
    n = (z**2 * var) / (delta**2)

    return math.ceil(n)

# Example:
# p=0.20 winrate, RR=6, 99% confidence, 2 parameters optimized
print(required_trades(p=0.20, RR=6, conf=0.99, m=2))
