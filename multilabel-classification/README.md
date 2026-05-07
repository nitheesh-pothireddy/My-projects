# Multilabel Classification

Multilabel classification on a tabular dataset where each row can carry several `y` labels at once. Compares three classifiers via the `LabelPowerset` problem transformation from `scikit-multilearn`:

- Random Forest — ~82% accuracy (winner)
- Decision Tree — ~72%
- MLP Neural Network — ~25% (high variance)

The winning model is refit on the full training set and used to produce a Kaggle-style `id_label, pred` submission file.

## Preprocessing

- `YES` / `NO` → `1` / `0`, missing → `-1`.
- Hashed-string feature columns → integer codes via `sklearn.preprocessing.OrdinalEncoder`, fit on the union of train + test values so the mapping is consistent across the two sets and reproducible across runs. (The original version used Python's built-in `hash()`, which is salted per process and made results non-reproducible.)
- Features (`x*`) and labels (`y*`) are split by column name prefix.

## Requirements

```
pandas
numpy
scikit-learn
scikit-multilearn
```

```bash
pip install -r requirements.txt
```

## Dataset

`train.csv`, `test.csv`, `trainLabels.csv` — on the `GIBots - Multilabel Classification files` branch of this repo (legacy branch name). Place them next to the notebook before running.

## Run

Open `multilabel_classification.ipynb` in Jupyter or VS Code and run all cells. The final cell writes `NitheeshP-prediction-output.csv`.

<img width="1088" alt="Screenshot 2024-03-30 at 11 47 28 PM" src="https://github.com/nitheesh-pothireddy/My-projects/assets/58605710/441a04aa-3311-407a-bfb8-d15e4e54101f">
<img width="1091" alt="Screenshot 2024-03-30 at 11 51 04 PM" src="https://github.com/nitheesh-pothireddy/My-projects/assets/58605710/12efdea3-7d8f-4dec-bc72-22018f8a3f82">

Done By

Nitheesh Pothireddy
