# NYC Motor Vehicle Collisions Dashboard

An interactive Streamlit dashboard that visualizes motor vehicle collision data for New York City — injury hotspots on a map, hourly and per-minute breakdowns, and the top dangerous streets by affected road user.

## Requirements

See `requirements.txt`. `pydeck` is pinned to `0.7.1` because newer versions break the map rendering used by Streamlit here.

```bash
pip install -r requirements.txt
```

## Dataset

Download `Motor_Vehicle_Collisions_-_Crashes.csv` from:
https://drive.google.com/file/d/19qxw4rlmmCkmZjHrrrvs4x-k7AVNeUMI/view?usp=sharing

Place it in this folder next to `app.py`.

## Run

```bash
streamlit run app.py
```

## Screenshots

![w1](https://user-images.githubusercontent.com/113423102/189865832-506996cb-a34e-4c49-a348-94ba24bf4a69.jpg)
![w2](https://user-images.githubusercontent.com/113423102/189865854-ec5a8e2a-0208-4fdd-9902-a5ad4a7910c9.jpg)
![w3](https://user-images.githubusercontent.com/113423102/189865887-b0b79c6d-0690-4a57-949f-10f958ca00a9.jpg)
![w4](https://user-images.githubusercontent.com/113423102/189865908-1e8c10fa-90a1-4815-8540-d7846b65cd53.jpg)

Done By

Nitheesh Pothireddy
