# Backtest Sample Size Calculator

A statistical tool to determine how many trades you need in your backtest to validate your strategy with confidence, accounting for win rate, risk-reward ratio, and parameter optimization.

## 🎯 What This Tool Does

This calculator answers a critical question: **"How many trades do I need before my backtest's edge is statistically real and not just luck?"**

It uses rigorous statistical methods (hypothesis testing, Bonferroni correction for multiple testing) to determine the minimum number of trades needed to be confident your strategy has a real edge.

## 🌐 Live Calculator

The web application is available at: [Live Calculator](https://your-domain.com) *(update with your deployment URL)*

## 📊 Features

- **Win Rate Input**: Enter win rate as percentage (e.g., 25 for 25%)
- **Risk-Reward Ratio**: Specify your reward:risk ratio (e.g., 4 for 1:4)
- **Parameter Optimization**: Account for multiple parameter testing (Bonferroni correction)
- **Confidence Levels**: Choose between 95%, 99%, or 99.9% confidence
- **Real-time Calculation**: Auto-updates when confidence level changes
- **Comprehensive Q&A**: Learn how the tool works and interpret results

## 🚀 Quick Start

### Web Application

Simply open `index.html` in your web browser. No server required - it's a standalone HTML file with embedded JavaScript.

### Python Script

```python
from how_many import required_trades

# Example: 25% win rate, 1:4 risk-reward, 99% confidence, 3 parameters optimized
trades_needed = required_trades(p=0.25, RR=4, conf=0.99, m=3)
print(f"You need {trades_needed} trades")
```

### Parameters

- `p`: Win rate as decimal (0.0-1.0), e.g., 0.25 for 25%
- `RR`: Reward:risk ratio, e.g., 4 for 1:4 risk-reward
- `conf`: Confidence level (default: 0.99 for 99%)
- `m`: Number of parameters optimized (default: 1)

### Returns

- Integer: Minimum number of trades required
- `float('inf')`: If strategy has no edge (win rate ≤ break-even)

## 📚 How It Works

The calculation is based on:

1. **Hypothesis Testing**: Tests whether win rate > break-even win rate
2. **Sample Size Formula**: Uses statistical power analysis
3. **Bonferroni Correction**: Adjusts for multiple parameter testing
4. **Central Limit Theorem**: Approximates binomial distribution with normal

### Formula

```
n = ceil((z² × p(1-p)) / (p - p₀)²)
```

Where:
- `z` = z-score for confidence level (adjusted for multiple testing)
- `p` = observed win rate
- `p₀` = break-even win rate = 1/(1 + RR)
- `p - p₀` = effect size (edge)

For detailed mathematical derivation, see [MATHEMATICAL_DERIVATION.md](MATHEMATICAL_DERIVATION.md)

## 📖 Example

**Scenario:**
- Win rate: 25%
- Risk-reward: 1:4 (RR = 4)
- Confidence: 99%
- Parameters optimized: 3

**Calculation:**
- Break-even win rate: 1/(1+4) = 20%
- Effect size: 25% - 20% = 5%
- Bonferroni-adjusted alpha: 0.01/3 = 0.00333
- Result: **~555 trades needed**

This means: With 555 trades in your backtest, you can be 99% confident (accounting for 3 parameters optimized) that your observed 25% win rate with 1:4 risk-reward represents a real edge, not random chance.

## 📁 Project Structure

```
.
├── index.html              # Web application (standalone)
├── how_many.py             # Python implementation
├── MATHEMATICAL_DERIVATION.md  # Detailed mathematical explanation
└── README.md              # This file
```

## 🔬 Mathematical Background

This tool implements rigorous statistical methods:

- **White's Reality Check** (multiple hypothesis testing)
- **Bonferroni Correction** (family-wise error rate control)
- **Sample Size Calculation** (statistical power analysis)
- **Central Limit Theorem** (normal approximation of binomial)

For a complete mathematical derivation with proofs, see [MATHEMATICAL_DERIVATION.md](MATHEMATICAL_DERIVATION.md).

## ⚠️ Important Notes

1. **Statistical Significance ≠ Guaranteed Profitability**: This tool validates statistical confidence, not future performance
2. **Assumptions**: Trades must be independent, win rate and risk-reward should be relatively stable
3. **Market Regimes**: Test across different market conditions for robustness
4. **Execution Matters**: Real trading includes slippage, commissions, and execution constraints not captured here

For additional validation checks, see: [The Backtest Checklist](https://stonkscapital.substack.com/p/the-backtest-checklist-7-things-you)

## 🛠️ Requirements

### Web Application
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No dependencies - pure HTML/CSS/JavaScript

### Python Script
- Python 3.6+
- scipy

```bash
pip install scipy
```

## 📝 License

This project is open source. Feel free to use, modify, and distribute.

## 🙏 Acknowledgments

- Based on statistical methods from White (2000), Lo & MacKinlay (1990)
- Bonferroni correction for multiple testing
- Standard practice in quantitative finance and academic research

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**Made with ❤️ by [Stonks Capital](https://stonkscapital.substack.com/)**

