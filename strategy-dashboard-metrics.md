# Strategy dashboard: CAGR, max drawdown, and compounding

This document describes **exactly** how the local **strategy dashboard** (`docs/strategy-dashboard.html`) computes **CAGR**, **max drawdown**, and **compounded** equity from a backtest run. The implementation lives in the `<script>` block of that file (search for the function names below).

The dashboard is a **viewer** on exported run artifacts (`trades.xlsx`, optional `equity_curve.xlsx`, optional `statistics.xlsx`). It is **not** identical to the Python backtester in every path, but it is designed to **align** where noted.

---

## Data sources and order of operations

When you select a run, the bar that shows **CAGR** and **Max DD** (`updateRunMetrics`) does the following:

1. Read **`trades.xlsx`** (first sheet) for P&amp;L columns and timestamps.
2. Read **`starting_balance`** from the strategy JSON in the picked repo folder (`portfolio.starting_balance`).
3. Compute **`yearsEngine`** from the trade sheet (see [CAGR time horizon](#cagr-time-horizon)).
4. **If `equity_curve.xlsx` exists** in the run folder: parse **Time** and **Balance** columns, optionally apply [risk scaling](#risk--slider) to the curve, then compute CAGR and max DD from that balance series using `yearsEngine` for CAGR.
5. **Else**, if there are sorted trades and `starting_balance > 0`: build a balance path with [`computeCompoundAnalytics`](#compounding-from-trades-replay) (same risk multiplier, same `yearsEngine` when available).
6. Optionally read **`statistics.xlsx`** and show the engine’s CAGR next to the dashboard figure for comparison (“engine truth” for the saved run).

If there is no equity file and no positive starting balance, CAGR/Max DD are not shown (see on-screen hint).

---

## Trade ordering (for replay and charts)

All replay logic that compounds from **`trades.xlsx`** uses the same ordering:

- Sort by **exit timestamp** ascending (`Exit Time`, `exit_time`, or `Exit` column via `parseCellDate`).
- If two rows share the same timestamp, preserve **sheet row order** (stable sort).

Functions: `buildSortedTradesForCompound`, `sortedDatedPnlsFromTradeRows`, `buildCumulativeFromTrades`.

The **P&amp;L** column is detected by `findPnlColumn` (e.g. `P&L`, case/spacing variants; excludes `%` columns).

---

## Compounding from trades (replay)

When the dashboard **does not** use `equity_curve.xlsx`, it builds a synthetic balance path in **`computeCompoundAnalytics(trades, startBal, riskMult, yearsOverride)`**.

State:

- `B` — simulated balance (starts at `startBal`).
- `origBefore` — **reference** level that tracks **`startBal` plus the sum of raw exported P&amp;Ls** for all trades processed so far (after each trade: `origBefore += p`).

For each trade in time order, with raw dollar P&amp;L `p` from the sheet:

```text
den     = max(origBefore, 1e-12)
dp      = riskMult * p * (B / den)
B       += dp
origBefore += p
```

After each step, the new `B` is appended to an internal **balances** array (the first point is `startBal` before any trade; then one point per trade close, so **length = 1 + number of trades**).

### Interpretation

- **`riskMult === 1`**: first trade adds `p` to balance; `origBefore` and `B` track the same cumulative sum after each trade **only if** you started from `startBal` and each `p` was generated at that reference scale. In practice this is a **replay** of exported dollar P&amp;Ls, not a full re-simulation of shares and stops.
- **`riskMult !== 1`**: each trade’s contribution is **scaled** by `m` and by **`B / origBefore`**, i.e. **equity-linked** scaling relative to the run’s cumulative P&amp;L path. This approximates “risk × m” in a way that grows with the simulated account (see UI tooltip on **Risk %**).

This is the same recurrence used for per-row scaled P&amp;L in **`computeScaledPnlByRowIndex`** (cumulative chart from trades).

---

## Compounding from `equity_curve.xlsx` + risk slider

If **`equity_curve.xlsx`** is present, balances come from the **engine export** (`Time`, `Balance`). When **`riskMult`** is not 1, the dashboard does **not** multiply the whole curve by a constant. It uses **`scaleEquityBalancesRiskAware(values, mult)`**:

- Output starts as `[values[0]]`.
- For each consecutive pair `(ev, ev1)` from the engine curve, with current scaled tail `cur` and `den = max(ev, 1e-12)`:

```text
d      = ev1 - ev
next   = cur + mult * d * (cur / den)
```

So each **step’s dollar change** is scaled by **`mult`** and by **current scaled balance / engine balance at that step**—again **equity-linked**, not a flat `× mult` on the entire series.

Then **CAGR** and **max DD** are computed from this scaled series (see below).

---

## Risk % slider

**`riskPnlScaleMultiplier(stem)`** (when the input is enabled):

- If the field parses as a **literal multiplier** (e.g. `×2`), that value is `riskMult`.
- Otherwise the field is a **target** `risk_per_trade_pct`. Then:

```text
riskMult = targetPct / baselineRiskPerTradePct(stem)
```

where `baselineRiskPerTradePct` comes from the strategy JSON’s `portfolio.risk_per_trade_pct`.

So **`riskMult = 1`** means “match the run as exported.”

---

## CAGR (formula)

For positive `startBal`, `endBal`, and `years`:

```text
CAGR (%) = ( (endBal / startBal)^(1/years) - 1 ) * 100
```

Implemented as **`cagrPctFromBalancesAndYears(startBal, endBal, years)`**. If `endBal/startBal` is not finite or positive, CAGR is omitted.

- **`startBal`**: first balance in the series used (either first point of scaled equity curve, or `starting_balance` for the trades replay).
- **`endBal`**: last balance in that series.

---

## CAGR time horizon (`years`)

The dashboard prefers the **same horizon as `backtester_engine._calculate_statistics`** when it can read entry/exit from **`trades.xlsx`**:

**`cagrYearsEngineStyle(minEntryMs, maxExitMs)`**

- `minEntryMs`: minimum **Entry Time** over rows with a valid P&amp;L.
- `maxExitMs`: maximum **Exit Time** over those rows; if exit is missing, that row’s **Entry Time** is used for the max (see `getTradeSpanForCagrMs`).

Then:

```text
days  = floor((maxExitMs - minEntryMs) / 86400000)
years = max(days / 365.25, 0.01)
```

So: **whole calendar days** between first entry and last exit, **365.25** days per year, **minimum 0.01 years**.

### Fallback when span cannot be computed

If `yearsEngine` is null, **`cagrAndMaxDdFromBalances`** and **`computeCompoundAnalytics`** use **`estimateCagrYears(t0, t1, count)`**:

- If both timestamps look valid (after 1995) and `t1 > t0`:  
  `years = (t1 - t0) / (365.25 * 86400 * 1000)` in ms (can be **fractional** days, unlike the engine’s `floor(days)`).
- Else: blends **`count / 252`** and **`7/365.25`**, then **`years = max(years, 1/252)`**.

So **CAGR years can differ** between “engine-style span from trades” vs “equity curve dates only” if the equity file’s first/last timestamps don’t match the trade span logic.

---

## Max drawdown (formula)

On a nonnegative balance path `balances[0..N]` (either from scaled equity curve or from **`computeCompoundAnalytics`**):

```text
peak   = balances[0]
maxDD  = 0
for each v in balances:
  peak  = max(peak, v)
  maxDD = max(maxDD, (peak - v) / peak * 100)   // if peak > 1e-9
```

**Max DD** is a **percentage** of the **running peak** (peak-to-trough in %). It is **not** logarithmic.

**Important:** these points are **only** at exported **trade closes** (replay path) or at **engine equity_curve** timestamps (typically one point per closed trade in the export). There is **no** intra-trade mark-to-market in this metric.

---

## Relation to the Python backtester

| Topic | Backtester (`backtester_engine._calculate_statistics`) | Strategy dashboard |
|--------|--------------------------------------------------------|--------------------|
| **Balance path** | Realized balance from simulation; `equity_curve.xlsx` matches that path (per exit). | Uses **`equity_curve.xlsx`** when present (after optional risk scaling), else **replays** `trades.xlsx` with the equity-linked formula above. |
| **Compounding** | Next position size from **current balance** and stop/risk rules; `balance +=` realized trade P&amp;L. | Replays **exported** dollar P&amp;Ls with **`dp = m * p * (B / origBefore)`** (or scaled engine deltas)—**not** a full resimulation of share count. |
| **CAGR formula** | Same geometric `(end/start)^(1/years)-1`. | Same. |
| **CAGR `years`** | `(last_exit - first_entry).days / 365.25`, floored day count via timedelta, `max(..., 0.01)`. | **`floor((maxExit - minEntry) ms / 86400000) / 365.25`**, `max(..., 0.01)` when span is parsed from trades. |
| **Max DD** | On `portfolio.equity_curve` balances. | On chosen balance series (scaled curve or replay). |

For an apples-to-apples check, compare dashboard numbers (with **Risk % = strategy default**, `riskMult = 1`) to **`statistics.xlsx`** / **`equity_curve.xlsx`** from the same run; small differences can still appear if timestamps or row filtering differ.

---

## File reference

- Dashboard UI and logic: `docs/strategy-dashboard.html`
- Engine statistics: `backtester_engine.py` → `_calculate_statistics`
- Exports: `run_backtest.py` → `trades.xlsx`, `equity_curve.xlsx`, `statistics.xlsx`
