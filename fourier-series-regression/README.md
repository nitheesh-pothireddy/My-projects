# Fourier Series Regression

Fits a regression model on a periodic dataset by using FFT to pick the dominant frequencies and feeding the resulting `sin`/`cos` components into a `LinearRegression`. On `scr-dataset.csv`, plain linear and polynomial regression sit at RMSE ~0.9; this approach drops it to ~0.0003.

## How it works

1. Run an FFT on `y` and compute the amplitude at each frequency.
2. Keep frequencies whose amplitude exceeds `AMPLITUDE_THRESHOLD` (tuned for this dataset).
3. Build feature matrix `[x, sin(2πf₁x), cos(2πf₁x), ..., sin(2πfₖx), cos(2πfₖx)]`.
4. Fit `LinearRegression` on an 80/20 train/test split and report MAE and RMSE.
5. Predict `y` for `x = 50` using the same feature builder.

## Requirements

```
numpy
pandas
matplotlib
scikit-learn
scipy
```

```bash
pip install -r requirements.txt
```

## Dataset

`scr-dataset.csv` — two columns `x` and `y`. Available on the `Crescer dataset` branch of this repo (legacy branch name). Place it next to the notebook before running.

## Run

Open `fourier_regression.ipynb` in Jupyter or VS Code and run all cells.

<img width="1196" alt="Screenshot 2024-04-01 at 5 38 43 PM" src="https://github.com/nitheesh-pothireddy/My-projects/assets/58605710/eaa7c5d3-fb9a-4e73-9ed5-0d60dee57b68">

Done By

Nitheesh Pothireddy
