# Position Sizing: Why Your Win Rate Doesn't Matter (And What Does)

## Introduction

You've validated your strategy. You know you have an edge. Your backtest shows a 60% win rate with a 1:4 risk-reward ratio. The math checks out.

But here's where most traders blow it: **position sizing.**

You can have the best strategy in the world, but if you size your positions wrong, you'll either:
- **Underperform** by being too conservative (leaving money on the table)
- **Blow up** by being too aggressive (wiping out your account)

The problem? Most traders size positions based on gut feel, arbitrary percentages, or "rules of thumb" that ignore the mathematical reality of their strategy.

**This is where Monte Carlo simulation changes everything.**

Instead of guessing, you can visualize 1,000 possible futures your strategy could take—and see exactly how different position sizing methods affect your equity curve, drawdowns, and final PnL.

In this post, we'll explore:
1. Why position sizing is the difference between profitable and broke
2. The mathematics behind optimal position sizing (Kelly Criterion)
3. How Monte Carlo simulation reveals the hidden risks
4. Practical position sizing strategies that actually work

---

## 1. The Position Sizing Problem

### 1.1 The Same Strategy, Different Outcomes

Imagine two traders with identical strategies:
- **Win rate:** 60%
- **Risk-reward:** 1:4
- **Expected value:** +2.0 units per trade

Trader A risks 1% per trade.  
Trader B risks 10% per trade.

After 100 trades:
- **Trader A:** Steady growth, small drawdowns, final PnL: +20%
- **Trader B:** Volatile swings, massive drawdowns, final PnL: -50% (or worse, blown up)

**Same strategy. Same edge. Completely different outcomes.**

The difference? Position sizing.

### 1.2 The Three Position Sizing Mistakes

**Mistake #1: Fixed Percentage (Too Simple)**
"I'll risk 2% per trade, no matter what."

This ignores your strategy's characteristics. A 2% risk might be perfect for a 70% win rate, 1:2 strategy, but way too conservative for a 40% win rate, 1:5 strategy.

**Mistake #2: Full Kelly (Too Aggressive)**
"I'll use the Kelly Criterion to maximize growth."

The Kelly Criterion gives you the mathematically optimal bet size—but it assumes:
- You know your true win rate and risk-reward perfectly
- You have infinite capital
- You can handle 50%+ drawdowns

In reality, Kelly is too aggressive. Most traders can't stomach the volatility.

**Mistake #3: Ignoring Drawdowns**
"I'll size based on expected returns only."

This is the most dangerous mistake. You might calculate that 5% per trade maximizes growth, but you haven't considered:
- What if you hit a losing streak?
- What's your maximum drawdown?
- Can you survive long enough to realize your edge?

---

## 2. The Mathematics of Optimal Position Sizing

### 2.1 The Kelly Criterion

The Kelly Criterion was developed by John Kelly in 1956 to solve a problem: **What fraction of your capital should you bet to maximize long-term growth?**

For a trading strategy with:
- **Win rate:** $p$ (as decimal, e.g., 0.60 for 60%)
- **Risk-reward ratio:** $RR$ (e.g., 4 for 1:4)

The Kelly fraction is:

$$
f^* = \frac{p(RR + 1) - 1}{RR}
$$

**Derivation:**

Each trade is a bet where:
- You win with probability $p$, gaining $RR$ units
- You lose with probability $(1-p)$, losing $1$ unit

If you bet a fraction $f$ of your capital:
- **Win:** Capital becomes $1 + f \cdot RR$
- **Loss:** Capital becomes $1 - f$

After $n$ trades, your capital grows by a factor:

$$
W_n = \prod_{i=1}^{n} (1 + f \cdot X_i)
$$

Where $X_i = RR$ with probability $p$, and $X_i = -1$ with probability $(1-p)$.

Taking the logarithm and using the law of large numbers:

$$
\log(W_n) \approx n \cdot E[\log(1 + f \cdot X)]
$$

$$
E[\log(1 + f \cdot X)] = p \cdot \log(1 + f \cdot RR) + (1-p) \cdot \log(1 - f)
$$

To maximize growth, we maximize this expectation. Taking the derivative with respect to $f$ and setting it to zero:

$$
\frac{d}{df} E[\log(1 + f \cdot X)] = \frac{p \cdot RR}{1 + f \cdot RR} - \frac{1-p}{1-f} = 0
$$

Solving for $f$:

$$
\frac{p \cdot RR}{1 + f \cdot RR} = \frac{1-p}{1-f}
$$

$$
p \cdot RR \cdot (1-f) = (1-p) \cdot (1 + f \cdot RR)
$$

$$
p \cdot RR - p \cdot RR \cdot f = 1-p + (1-p) \cdot f \cdot RR
$$

$$
p \cdot RR - (1-p) = f \cdot [p \cdot RR + (1-p) \cdot RR]
$$

$$
p(RR + 1) - 1 = f \cdot RR
$$

$$
f^* = \frac{p(RR + 1) - 1}{RR}
$$

**Example:**
- Win rate: 60% ($p = 0.60$)
- Risk-reward: 1:4 ($RR = 4$)

$$
f^* = \frac{0.60(4 + 1) - 1}{4} = \frac{0.60 \times 5 - 1}{4} = \frac{3 - 1}{4} = \frac{2}{4} = 0.50
$$

**Full Kelly = 50% per trade.**

This is the mathematically optimal bet size—but it's extremely aggressive. Most traders can't handle the volatility.

### 2.2 Fractional Kelly

To reduce volatility while maintaining most of the growth, traders use **fractional Kelly**:

- **Half Kelly:** $f = 0.5 \times f^*$
- **Quarter Kelly:** $f = 0.25 \times f^*$

**Example (continued):**
- Full Kelly: 50%
- Half Kelly: 25%
- Quarter Kelly: 12.5%

Fractional Kelly reduces drawdowns significantly while sacrificing only a small amount of growth.

### 2.3 Fixed Fractional Sizing

Instead of Kelly, some traders use a **fixed percentage** of capital:

$$
\text{Position Size} = \text{Capital} \times f_{\text{fixed}}
$$

Where $f_{\text{fixed}}$ is a constant (e.g., 1%, 2%, 5%).

This is simpler but ignores your strategy's characteristics. It's a "one-size-fits-all" approach that doesn't adapt to your edge.

### 2.4 Fixed Ratio Sizing

**Fixed ratio sizing** (Ralph Vince's method) sizes positions based on a fixed dollar amount per unit of risk, rather than a percentage of capital.

The position size grows more slowly than fixed fractional, reducing volatility during drawdowns.

---

## 3. Why Monte Carlo Simulation Matters

### 3.1 The Problem with Expected Value

Expected value tells you the average outcome, but it doesn't tell you:
- **What's the worst-case scenario?**
- **How likely are you to hit a 50% drawdown?**
- **What's the distribution of outcomes?**

A strategy with EV = +2.0 could mean:
- **Scenario A:** Steady +2.0 every trade (low variance)
- **Scenario B:** -10, -10, -10, +50, +50, +50 (high variance)

Both have the same EV, but completely different risk profiles.

### 3.2 Monte Carlo Simulation

**Monte Carlo simulation** runs your strategy thousands of times with random outcomes, showing you:
- **1,000 possible equity curves** your strategy could take
- **Distribution of final PnL** (best case, worst case, average)
- **Maximum drawdowns** across all scenarios
- **Consecutive win/loss streaks**

This reveals the hidden risks that expected value hides.

### 3.3 What You Learn from Monte Carlo

**1. Drawdown Risk**
- Full Kelly might show 70%+ drawdowns
- Half Kelly might show 40% drawdowns
- Quarter Kelly might show 20% drawdowns

**2. Volatility**
- Some sizing methods create smooth equity curves
- Others create wild swings (even with positive EV)

**3. Survival Probability**
- What's the chance you'll blow up before realizing your edge?
- How many trades can you survive a losing streak?

**4. Growth vs. Risk Trade-off**
- Full Kelly: Highest growth, highest risk
- Half Kelly: 75% of growth, 50% of risk
- Quarter Kelly: 50% of growth, 25% of risk

---

## 4. Practical Position Sizing Strategies

### 4.1 The Conservative Approach: Quarter Kelly

**Best for:**
- Traders who can't handle large drawdowns
- Strategies with uncertain parameters
- Real-world trading (where you don't know true win rate perfectly)

**Formula:**
$$
f = 0.25 \times \frac{p(RR + 1) - 1}{RR}
$$

**Pros:**
- Low drawdowns (typically 15-25%)
- Smooth equity curve
- High survival probability

**Cons:**
- Slower growth than full Kelly
- May be too conservative for high-confidence strategies

### 4.2 The Balanced Approach: Half Kelly

**Best for:**
- Traders comfortable with moderate drawdowns
- Strategies with well-validated parameters
- Most practical use cases

**Formula:**
$$
f = 0.5 \times \frac{p(RR + 1) - 1}{RR}
$$

**Pros:**
- Good balance of growth and risk
- Moderate drawdowns (typically 30-40%)
- Captures most of Kelly's growth with half the volatility

**Cons:**
- Still requires discipline during drawdowns
- May be too aggressive for some traders

### 4.3 The Aggressive Approach: Full Kelly

**Best for:**
- Traders with high risk tolerance
- Strategies with extremely high confidence
- Theoretical maximum growth (rarely used in practice)

**Formula:**
$$
f = \frac{p(RR + 1) - 1}{RR}
$$

**Pros:**
- Maximum long-term growth
- Mathematically optimal

**Cons:**
- Extreme drawdowns (50%+)
- High volatility
- Requires perfect knowledge of parameters (which you never have)

### 4.4 The Simple Approach: Fixed Percentage

**Best for:**
- Beginners
- Strategies where you can't calculate Kelly
- When you want simplicity over optimization

**Formula:**
$$
f = \text{fixed percentage} \text{ (e.g., 1%, 2%, 5%)}
$$

**Pros:**
- Simple to implement
- No calculations needed
- Easy to understand

**Cons:**
- Ignores strategy characteristics
- May be too conservative or too aggressive
- Not optimized for your edge

---

## 5. Real-World Considerations

### 5.1 Parameter Uncertainty

The Kelly Criterion assumes you know your true win rate and risk-reward perfectly. In reality, you're estimating from a sample.

**Solution:** Use fractional Kelly (half or quarter) to account for uncertainty.

If your backtest shows 60% win rate, your true win rate might be:
- 55% (you're overestimating)
- 60% (you're correct)
- 65% (you're underestimating)

Fractional Kelly protects you from overestimating your edge.

### 5.2 Psychological Factors

Even if full Kelly is mathematically optimal, you might not be able to handle:
- 50%+ drawdowns
- Months of losses
- Extreme volatility

**Solution:** Size based on what you can actually stick to. A 25% Kelly that you follow is better than a 50% Kelly that makes you quit.

### 5.3 Capital Constraints

Kelly assumes infinite capital. In reality:
- You have limited capital
- You might need to withdraw profits
- You can't trade fractional shares

**Solution:** Cap your position size at a maximum (e.g., 25% of capital) regardless of Kelly calculation.

### 5.4 Market Regime Changes

Your win rate and risk-reward might change over time:
- Market conditions shift
- Edge erodes
- Execution quality varies

**Solution:** Regularly re-evaluate your position sizing. Don't assume your backtest parameters hold forever.

---

## 6. How to Use Monte Carlo for Position Sizing

### 6.1 Step 1: Input Your Strategy Parameters

- **Win rate:** From your backtest
- **Risk-reward ratio:** Average win / average loss
- **Number of trades:** How many trades you plan to take

### 6.2 Step 2: Test Different Sizing Methods

Run Monte Carlo simulations for:
- **Full Kelly:** See maximum growth potential
- **Half Kelly:** See balanced approach
- **Quarter Kelly:** See conservative approach
- **Fixed Ratio:** See if it fits your risk tolerance

### 6.3 Step 3: Analyze the Results

Look at:
- **Average Final PnL:** Which method maximizes returns?
- **Average Max Drawdown:** Which method minimizes risk?
- **Worst Path Final PnL:** What's the worst-case scenario?
- **Worst Max Drawdown:** Can you survive this?

### 6.4 Step 4: Choose Based on Your Risk Tolerance

**If you can handle 40%+ drawdowns:** Use half Kelly or full Kelly  
**If you want smooth growth:** Use quarter Kelly  
**If you want simplicity:** Use fixed percentage (1-2%)

### 6.5 Step 5: Monitor and Adjust

As you trade:
- Track your actual win rate vs. backtest
- Adjust position sizing if parameters change
- Re-run Monte Carlo with updated numbers

---

## 7. Common Position Sizing Mistakes

### 7.1 Mistake: Sizing Based on Confidence

"I'm 90% confident this trade will win, so I'll risk 10%."

**Problem:** Confidence doesn't equal edge. You can be 90% confident and still have a -EV strategy.

**Solution:** Size based on your strategy's mathematical edge, not your gut feeling.

### 7.2 Mistake: Increasing Size After Wins

"I'm on a hot streak, let me increase my position size."

**Problem:** This is the gambler's fallacy. Past wins don't predict future wins.

**Solution:** Keep position sizing consistent based on your edge, not recent performance.

### 7.3 Mistake: Decreasing Size After Losses

"I just lost three in a row, let me reduce my size."

**Problem:** If your edge is real, losses are just variance. Reducing size after losses reduces your long-term growth.

**Solution:** Trust your edge. Keep sizing consistent (unless your edge has actually changed).

### 7.4 Mistake: Ignoring Drawdowns

"I'll use full Kelly because it maximizes growth."

**Problem:** Full Kelly can create 50%+ drawdowns. Can you survive that?

**Solution:** Use Monte Carlo to see actual drawdowns. Choose sizing you can stick to.

---

## 8. The Bottom Line

Position sizing is the difference between profitable and broke. You can have the best strategy in the world, but if you size wrong, you'll fail.

**Key Takeaways:**

1. **Kelly Criterion gives you the mathematically optimal bet size**—but it's usually too aggressive for real-world trading.

2. **Fractional Kelly (half or quarter) is the practical sweet spot**—most of the growth, fraction of the risk.

3. **Monte Carlo simulation reveals hidden risks**—expected value hides the worst-case scenarios.

4. **Size based on what you can stick to**—a conservative sizing you follow beats an aggressive sizing that makes you quit.

5. **Re-evaluate regularly**—your edge might change, and your position sizing should adapt.

**The mathematics are clear. The tools are available. The question is: Will you use them, or will you guess?**

Run the Monte Carlo simulation. See 1,000 possible futures. Understand the risks. Then size your positions based on data, not gut feel.

Your account balance will thank you.

---

## References

- Kelly, J. L. (1956). "A New Interpretation of Information Rate." *Bell System Technical Journal*, 35(4), 917-926.
- Vince, R. (1992). *Portfolio Management Formulas: Mathematical Trading Methods for the Futures, Options, and Stock Markets*. John Wiley & Sons.
- Thorp, E. O. (1962). "Beat the Dealer: A Winning Strategy for the Game of Twenty-One." *Vintage Books*.
- MacLean, L. C., Thorp, E. O., & Ziemba, W. T. (2010). "The Kelly Capital Growth Investment Criterion: Theory and Practice." *World Scientific*.

