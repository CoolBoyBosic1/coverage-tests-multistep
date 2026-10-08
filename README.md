# Restoring Size, Losing Power: Coverage Tests at Multi-Step Horizons

Code and data for the paper *Restoring Size, Losing Power: Coverage Tests at Multi-Step Horizons — Evidence from Overlapping Interval Forecasts*.

## What this is about

Interval forecasts for the next H days are usually backtested on every day, so neighbouring forecasts overlap and their hit/miss outcomes are strongly dependent. The Kupiec and Christoffersen coverage tests assume independence, so on daily data they reject correct models almost every time (size is 79% and 100% at H = 90). Evaluating only every s days, with s close to H, restores the size. The price is power: with only a few dozen non-overlapping forecasts, the Christoffersen test does not detect clustered violations. The paper measures this trade-off by simulation, checks several fixes (HAC and fixed-b tests, a duration test, self-normalized tests, combining phases), and applies the tests to GARCH-VaR forecasts for BTC, Brent crude and EUR/USD.

## Contents

| File | What it does | Paper |
|---|---|---|
| `01_monte_carlo_experiments.ipynb` | Size and power simulations, robustness checks, H–T–persistence surface | Tables 1–8, Figure 1 |
| `02_empirical_application.ipynb` | Phase-aggregation check; GARCH(1,1)-t VaR backtest for BTC, Brent, EUR/USD | Table 9 |
| `03_verification.ipynb` | Independent re-implementation that re-checks key results (24 checks) | Tables 1, 2, 7, 9 |
| `data/` | Daily price files used by notebook 02 | |
| `HT_surface.png` | Figure 1, written by notebook 01 | Figure 1 |
| `fetch_btc_data.py` | Optional: re-download BTC data from Binance | |

## How to run

```bash
pip install -r requirements.txt
jupyter notebook
```

Open a notebook and choose **Kernel → Restart & Run All**. Python 3.12 was used; any recent 3.x should work.

Run each notebook from top to bottom in a fresh kernel. All random numbers come from one generator seeded with 42, so every cell depends on the ones above it. Re-running a single cell gives different draws.

Approximate runtime on a laptop: notebook 01 about 1–2 minutes, notebook 02 a few minutes (GARCH refits), notebook 03 a few minutes. Set `FAST_RUN = True` near the top of a notebook for a quick check with fewer replications.

The notebooks are saved with their outputs, so you can read the results without running anything.

## Reading the results

Everything in notebooks 01 and 03 is a Monte Carlo estimate. A rejection rate near 5% from 1,000 replications has a standard error of about 0.7 percentage points, so differences of a point or two between runs or against the paper are sampling noise. The standard-error cell in notebook 01 shows the sizes. Notebook 03 passes a check when the new run is within a stated tolerance of a reference value.

## Data

| Series | File | Source | Licence |
|---|---|---|---|
| BTC/USDT daily | `data/btc_binance_daily.csv` | Binance spot klines | Binance terms of use |
| Brent crude daily | `data/brent-daily.csv` | [datasets/oil-prices](https://github.com/datasets/oil-prices) (U.S. EIA), downloaded 2026-10-08 | ODC-PDDL |
| EUR/USD daily | `data/euro-daily.csv` | [datasets/exchange-rates](https://github.com/datasets/exchange-rates) (Federal Reserve), downloaded 2026-10-08 | ODC-PDDL |

The files are frozen, so Table 9 gives the same numbers on every run. Notebook 02 downloads the current version from GitHub only if a file is missing, and then the sample sizes will differ slightly. Please do not regenerate the BTC file: `fetch_btc_data.py` writes to a separate file and is only meant for checking where the data came from.

## License

Code: MIT (see `LICENSE`). Data files keep the licences listed above.

## Citation

See `CITATION.cff`.
