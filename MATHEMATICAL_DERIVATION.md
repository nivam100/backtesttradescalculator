# The Mathematics of Backtest Validation: How Many Trades Do You Need to Trust Your Results?

## Introduction

You've run a backtest. Your strategy shows a 60% win rate with a 1:4 risk-reward ratio. The equity curve looks promising. But here's the critical question:

**How many trades do you need to accurately estimate your Expected Value (EV) for position sizing decisions?**

This is fundamentally a **confidence interval** problem in statistics. We need to determine the minimum number of independent trades required to estimate your EV within a desired precision (e.g., ±20%) with a given confidence level (e.g., 95%).

Unlike edge detection (which asks "Do I have an edge?"), EV estimation asks: "What is my edge, and how precisely do I know it?"

In this post, we'll derive the exact formula from first principles, step by step.

---

## 1. The Statistical Framework

### 1.1 Expected Value (EV)

For a strategy with win rate $p$ and risk-reward ratio $RR$ (defined as reward:risk, e.g., RR = 4 means we risk 1 unit to gain 4 units):

- **Win:** Gain $RR$ units (with probability $p$)
- **Loss:** Lose $1$ unit (with probability $1-p$)

The expected value per trade is:

$$
EV = p \cdot RR + (1-p) \cdot (-1) = p \cdot RR - (1-p)
$$

Simplifying:

$$
EV = p \cdot RR - 1 + p = p(RR + 1) - 1
$$

**Example:** With 60% win rate and 1:4 risk-reward:
- $EV = 0.60 \times 4 - (1 - 0.60) = 2.4 - 0.4 = 2.0$

So you expect to make 2 units per trade on average.

### 1.2 The Problem: Estimating EV with Confidence

When you backtest, you observe a sample of trades. From this sample, you estimate:
- Your win rate: $\hat{p} = \frac{\text{number of wins}}{n}$
- Your EV: $\widehat{EV} = \hat{p}(RR + 1) - 1$

But this is just an **estimate**. The true EV might be different. We want to know:

**"How many trades do I need so that my EV estimate is within ±20% of the true value, with 95% confidence?"**

This means: If your true EV is 2.0, you want your estimate to be between 1.6 and 2.4, and you want to be 95% confident this range contains the true value.

---

## 2. Confidence Intervals for EV

### 2.1 The Central Limit Theorem

Each trade is a Bernoulli trial: win with probability $p$, lose with probability $1-p$.

For $n$ independent trades, the number of wins $X$ follows a binomial distribution:

$$
X \sim \text{Binomial}(n, p)
$$

The observed win rate is $\hat{p} = X/n$. By the Central Limit Theorem, for large $n$:

$$
\hat{p} \sim \mathcal{N}\left(p, \frac{p(1-p)}{n}\right)
$$

This means the win rate estimate is approximately normally distributed with:
- **Mean:** $p$ (the true win rate)
- **Variance:** $\frac{p(1-p)}{n}$

### 2.2 Standard Error of EV

Since $EV = p(RR + 1) - 1$, and we're estimating $p$ with $\hat{p}$, we need to find the standard error of our EV estimate.

Using the formula for the variance of a linear transformation:

$$
\text{Var}(\widehat{EV}) = \text{Var}(\hat{p}(RR + 1) - 1) = (RR + 1)^2 \cdot \text{Var}(\hat{p})
$$

Since $\text{Var}(\hat{p}) = \frac{p(1-p)}{n}$:

$$
\text{Var}(\widehat{EV}) = (RR + 1)^2 \cdot \frac{p(1-p)}{n}
$$

The **standard error** of EV is the square root of the variance:

$$
\text{SE}(\widehat{EV}) = (RR + 1) \cdot \sqrt{\frac{p(1-p)}{n}}
$$

For practical purposes, we use the observed variance $\hat{p}(1-\hat{p})$ instead of $p(1-p)$:

$$
\text{SE}(\widehat{EV}) = (RR + 1) \cdot \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}
$$

Let $v = \hat{p}(1-\hat{p})$ be the variance term. Then:

$$
\text{SE}(\widehat{EV}) = (RR + 1) \cdot \sqrt{\frac{v}{n}}
$$

### 2.3 Margin of Error

The **margin of error** is how far off our estimate might be. For a confidence level of $(1-\alpha)$ (e.g., 95% means $\alpha = 0.05$), we use the critical value $z_{1-\alpha/2}$ from the standard normal distribution.

For 95% confidence, $z_{0.975} \approx 1.96$.

The margin of error is:

$$
\text{Margin of Error} = z_{1-\alpha/2} \cdot \text{SE}(\widehat{EV})
$$

$$
\text{Margin of Error} = z_{1-\alpha/2} \cdot (RR + 1) \cdot \sqrt{\frac{v}{n}}
$$

### 2.4 Confidence Interval

The confidence interval for EV is:

$$
\widehat{EV} \pm \text{Margin of Error}
$$

Or more precisely:

$$
\left[ \widehat{EV} - z_{1-\alpha/2} \cdot (RR + 1) \cdot \sqrt{\frac{v}{n}}, \quad \widehat{EV} + z_{1-\alpha/2} \cdot (RR + 1) \cdot \sqrt{\frac{v}{n}} \right]
$$

---

## 3. Sample Size Calculation

### 3.1 Desired Precision

We want the margin of error to be a certain percentage of the EV. For example, ±20% means:

$$
\text{Margin of Error} = EV \cdot \frac{\text{CI Width \%}}{100}
$$

If we want ±20% precision:
$$
\text{Margin of Error} = EV \cdot 0.20
$$

### 3.2 Solving for Sample Size

We want:

$$
z_{1-\alpha/2} \cdot (RR + 1) \cdot \sqrt{\frac{v}{n}} = EV \cdot \frac{\text{CI Width \%}}{100}
$$

Solving for $n$:

$$
\sqrt{\frac{v}{n}} = \frac{EV \cdot \frac{\text{CI Width \%}}{100}}{z_{1-\alpha/2} \cdot (RR + 1)}
$$

$$
\frac{v}{n} = \left( \frac{EV \cdot \frac{\text{CI Width \%}}{100}}{z_{1-\alpha/2} \cdot (RR + 1)} \right)^2
$$

$$
n = \frac{v}{\left( \frac{EV \cdot \frac{\text{CI Width \%}}{100}}{z_{1-\alpha/2} \cdot (RR + 1)} \right)^2}
$$

Rearranging:

$$
n = v \cdot \left( \frac{z_{1-\alpha/2} \cdot (RR + 1)}{EV \cdot \frac{\text{CI Width \%}}{100}} \right)^2
$$

Simplifying:

$$
n = \left( \frac{z_{1-\alpha/2} \cdot (RR + 1) \cdot \sqrt{v}}{EV \cdot \frac{\text{CI Width \%}}{100}} \right)^2
$$

This is the formula we use.

### 3.3 Complete Formula

Putting it all together, the required number of trades is:

$$
n = \left\lceil \left( \frac{z_{1-\alpha/2} \cdot (RR + 1) \cdot \sqrt{p(1-p)}}{EV \cdot \frac{\text{CI Width \%}}{100}} \right)^2 \right\rceil
$$

Where:
- $p$ = win rate (as decimal, e.g., 0.60 for 60%)
- $RR$ = reward:risk ratio (e.g., 4 for 1:4 risk-reward)
- $EV = p(RR + 1) - 1$ = expected value per trade
- $v = p(1-p)$ = variance of win rate
- $\text{CI Width \%}$ = desired confidence interval width as percentage (e.g., 20 for ±20%)
- $z_{1-\alpha/2}$ = critical value from standard normal distribution (e.g., 1.96 for 95% confidence)
- $\lceil \cdot \rceil$ = ceiling function (round up)

### 3.4 Implementation Notes

**If $p \leq p_0$:** The strategy has no edge (EV ≤ 0), where $p_0 = \frac{1}{1 + RR}$ is the break-even win rate. The calculation doesn't apply for -EV strategies.

**Variance term:** We use $p(1-p)$ which captures the uncertainty in our win rate estimate.

**Z-score calculation:** The critical value $z_{1-\alpha/2}$ comes from the inverse cumulative distribution function (CDF) of the standard normal distribution:

$$
z_{1-\alpha/2} = \Phi^{-1}(1 - \alpha/2)
$$

Where $\Phi^{-1}$ is the inverse of the standard normal CDF.

For 95% confidence ($\alpha = 0.05$):
$$
z_{0.975} = \Phi^{-1}(0.975) \approx 1.96
$$

---

## 4. Why Each Component Matters

### 4.1 Why Variance Matters

The variance term $p(1-p)$ captures the uncertainty in your win rate estimate:
- **Low win rates (or high win rates)** have lower variance: $0.1(1-0.1) = 0.09$
- **50% win rate** has maximum variance: $0.5(1-0.5) = 0.25$

Higher variance means more uncertainty, requiring more trades to reach the same precision.

### 4.2 Why Risk-Reward Matters

The $(RR + 1)$ term amplifies the uncertainty. Higher risk-reward ratios create more variance in your returns, even with the same win rate variance.

**Example:** 
- Strategy A: 50% win rate, 1:2 risk-reward → Lower variance
- Strategy B: 50% win rate, 1:5 risk-reward → Higher variance

Strategy B needs more trades because the higher risk-reward amplifies the uncertainty.

### 4.3 Why Desired Precision Matters

The desired CI width appears in the denominator, squared. This means:
- **Halving the CI width** (from ±20% to ±10%) requires **4× more trades**
- **Doubling the CI width** (from ±20% to ±40%) requires **4× fewer trades**

This is why ±20% is a reasonable default—it balances precision with practicality.

### 4.4 Why Confidence Level Matters

Higher confidence levels require larger z-scores:
- 90% confidence: $z = 1.645$
- 95% confidence: $z = 1.96$
- 99% confidence: $z = 2.576$

Since $n \propto z^2$, going from 95% to 99% confidence requires $(2.576/1.96)^2 \approx 1.73×$ more trades.

---

## 5. Example Calculation

Let's work through an example:

**Inputs:**
- Win rate: $p = 0.60$ (60%)
- Risk-reward: $RR = 4$ (1:4)
- Desired CI width: 20% (±20%)
- Confidence level: 95% ($\alpha = 0.05$)

**Step 1: Calculate EV**
$$
EV = 0.60 \times 4 - (1 - 0.60) = 2.4 - 0.4 = 2.0
$$

**Step 2: Calculate variance**
$$
v = p(1-p) = 0.60 \times 0.40 = 0.24
$$

**Step 3: Get z-score**
For 95% confidence, $z_{0.975} = 1.96$

**Step 4: Calculate margin target**
$$
\text{Margin Target} = EV \times \frac{20}{100} = 2.0 \times 0.20 = 0.40
$$

**Step 5: Calculate standard error target**
$$
\text{SE Target} = \frac{\text{Margin Target}}{z} = \frac{0.40}{1.96} \approx 0.204
$$

**Step 6: Calculate required sample size**
$$
n = \left( \frac{(RR + 1) \cdot \sqrt{v}}{\text{SE Target}} \right)^2
$$

$$
n = \left( \frac{(4 + 1) \cdot \sqrt{0.24}}{0.204} \right)^2
$$

$$
n = \left( \frac{5 \times 0.490}{0.204} \right)^2
$$

$$
n = \left( \frac{2.449}{0.204} \right)^2
$$

$$
n = (12.00)^2 = 144
$$

So you need **144 trades** to estimate your EV within ±20% with 95% confidence.

---

## 6. Limitations and Assumptions

This calculation makes several assumptions:

1. **Independence:** Trades are independent (no autocorrelation)
2. **Fixed win rate:** Win rate doesn't change over time
3. **Fixed risk-reward:** Risk-reward ratio is consistent
4. **Large sample approximation:** Uses CLT, which requires sufficient $n$
5. **Binomial model:** Each trade is win/loss (no partial outcomes)
6. **Normal approximation:** Assumes normal distribution of win rate estimate

**When these assumptions break down:**
- If trades are correlated, you need even more samples
- If market conditions change, you need to test across different regimes
- If risk-reward varies, the calculation becomes more complex
- If you have partial wins/losses, you need a different model

---

## 7. Comparison with Edge Detection

It's important to distinguish between:

**Edge Detection (Hypothesis Testing):**
- **Question:** "Do I have an edge? (Is EV > 0?)"
- **Formula:** $n = \frac{z^2 \cdot p(1-p)}{(p - p_0)^2}$
- **Purpose:** Detect if strategy is profitable
- **Requires:** Fewer trades (just to confirm edge exists)

**EV Estimation (Confidence Intervals):**
- **Question:** "What is my EV, and how precisely do I know it?"
- **Formula:** $n = \left( \frac{z \cdot (RR + 1) \cdot \sqrt{p(1-p)}}{EV \cdot \frac{\text{CI Width \%}}{100}} \right)^2$
- **Purpose:** Estimate EV for position sizing
- **Requires:** More trades (to know EV precisely)

**Example:** A strategy might need 100 trades to confirm it has an edge (EV > 0), but 500+ trades to estimate that EV is 0.25 ± 0.05 with 95% confidence.

---

## 8. Practical Implications

### 8.1 Most Traders Underestimate

Most traders dramatically underestimate how many trades they need. A strategy with:
- 50% win rate, 1:2 risk-reward might need 500+ trades
- 70% win rate, 1:3 risk-reward might only need 100 trades

The difference? **Variance and effect size.**

### 8.2 Position Sizing Decisions

This formula is critical for position sizing methods like:
- **Kelly Criterion:** Requires accurate EV estimate
- **Fixed Fractional Sizing:** Needs to know EV to set risk percentage
- **Risk Management:** Can't size positions without knowing EV precision

If your EV estimate has a wide confidence interval (±50%), you can't confidently size positions. You need more trades.

### 8.3 The Trade-off

There's always a trade-off:
- **More precision** (narrower CI) = **More trades needed**
- **Higher confidence** = **More trades needed**
- **Higher variance** = **More trades needed**

The ±20% default is a practical balance—precise enough for sizing decisions, but not so strict that it requires thousands of trades.

---

## 9. Conclusion

The required sample size formula for EV estimation:

$$
n = \left\lceil \left( \frac{z_{1-\alpha/2} \cdot (RR + 1) \cdot \sqrt{p(1-p)}}{EV \cdot \frac{\text{CI Width \%}}{100}} \right)^2 \right\rceil
$$

Is derived from fundamental statistical principles:
- **Central Limit Theorem** to approximate the binomial distribution
- **Confidence intervals** to quantify uncertainty
- **Standard error** to measure precision

This isn't just a heuristic—it's rigorous statistical inference. When you see "you need 144 trades," that means: *with 144 trades, you can be 95% confident that your EV estimate is within ±20% of the true value.*

Use this formula to validate your backtests before making position sizing decisions. The mathematics are sound—but remember, statistical precision doesn't guarantee future profitability. Market conditions change, execution matters, and edge erosion is real.

---

## References

- Casella, G., & Berger, R. L. (2002). *Statistical Inference*. Duxbury.
- Rice, J. A. (2006). *Mathematical Statistics and Data Analysis*. Duxbury Press.
- Central Limit Theorem: The foundation for normal approximation of sample means.
