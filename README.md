# Inter-turn Short Cicruit (ITSC) Detection on Induction Motors

this project aims to build an MLP that can detect ITSCs on three-phase industrial induction motors.

the MLP is a multi-class classifier that should classify each motor into one of seven classes (from 0 to 6 representing the degree of fault damage):

- 0 -> Normal
- 1 -> High Impedance 1
- 2 -> High Impedance 2
- 3 -> HIgh Impedance 3
- 4 -> Low Impedance 1
- 5 -> Low Impedance 2
- 6 -> Low Impedance 3

where:

- High Impedance: represents the initial stage of the fault, in which the electric insulator is beginning to degrade and a parallel current path appears
- Low Impedance: represents a full short-circuit. The current flows in the new path and a voltage is induced in the shorted coil.

## 0. Setup

we are using mamba, the cli tool alternative to conda written in C++, but you can use conda as well

1. create the virtual environment and install all needed packages

```bash
mamba env create -f environment.yml
```

2. activate the env

```bash
mamba activate itsc-detection
```

the env name is 'itsc-detection'

3. install the MIT ITSC detection dataset from Kaggle [(link)](https://www.kaggle.com/datasets/rebecacunha/mit-short-circuit-flux-and-current-signals/data)

4. at the project root, create a new folder `data` and within it two other folders: `raw` and `processed`

5. extract the CSV files to location `data/raw`

6. run the feature extraction script at `src/data_pipeline.py`

```bash
python src/data_pipeline.py
```

a new file `features.csv` should be created at `data/processed`. this file represents the dataset we will be using in the notebook. you can now start running the notebook. For additional explanation, you can read below

## 1. Dataset Description

the dataset is located at Kaggle [(Link)](https://www.kaggle.com/datasets/rebecacunha/mit-short-circuit-flux-and-current-signals). it contains 2618 CSV files (almost 8.7 GB), each containing four columns:

0. TIME: represents moment of data recording
1. CH1: 1st phase current intensity
2. CH2: 2nd phase current intensity
3. CH3: 3rd phase current intensity
4. CH4: Magnetic flux

\*CH1, CH2, CH3 and CH4 are time-series

we will extract from each CSV file a set of features representing that motor sample, and we will combine the results from the 2618 sample in a new CSV file that we will feed to the MLP: we created a python script `src/data_pipeline.py` to achieve this:

- it reads the CSV files located at folder `data/row` (put the 2618 CSVs here)
- it extract the chosen features
- creates a Pandas DataFrame and feeds it the extracted data
- writes the dataframe object to a new CSV file `data/processed/features.csv` (this is the dataset we will be using in the notebook)

## 2. Feature Enginnering:

> **NOTE**: check `docs/signal_features` for the exact mathematical expressions of the extracted features

We have the following set of extracted features:

### 2.1. Time-Domain Features:

1. mean: calc. for each current (a, b and c)
2. std: calc. for each current and the flux
3. RMS: calc. for each current and the flux
4. std: calc. for each current and the flux
5. peak2peak: calc. for each current and the flux

6. skewness: calc. for each current and the flux
7. kurtosis: calc. for each current and the flux

8. Crest factor: calc. for each current and the flux
9. Form factor: calc. for each current and the flux
10. Clearance factor: calc. for each current and the flux
11. zcr: calc. for each current and the flux
12. signal energy: calc. for each current and the flux

### 2.2. Frequency Domain Features:

13. fundamental frequency: one per csv file (derived from phase A)
14. harmonic magnitudes: for each current and the flux
15. total harmonic distortion: for each current and the flux
16. spectral centroid: for each current and the flux
17. spectral spread: for each current and the flux
18. sideband ratio: for each current

### 2.3. Three-Phase Specific Features:

19. phase imbalance: one per csv file
20. park vector stats: one per csv file
21. flux-current phase angle: one per csv file
22. negative sequence current: one per csv file

as a summary:

| Feature Category | Feature Name                                                                                       | Applied To              | Total Column Count |
| ---------------- | -------------------------------------------------------------------------------------------------- | ----------------------- | ------------------ |
| Time Domain      | "Mean, Std, RMS, Peak2Peak, Skewness, Kurtosis, Crest, Form, Clearance, ZCR, Energy"               | "ia​,ib​,ic​, and Flux" | 11×4=44            |
| Frequency Domain | "Harmonic Magnitudes (3rd, 5th, 7th), THD, Spectral Centroid, Spectral Spread"                     | "ia​,ib​,ic​, and Flux" | 6×4=24             |
| Frequency Domain | Sideband Ratio                                                                                     | "ia​,ib​,ic​ only"      | 1×3=3              |
| Global System    | "Fundamental Freq, Phase Imbalance, Park Vector Stats (x3), Flux-Current Phase, Negative Sequence" | Combined System         | 7                  |
| Grand Total      |                                                                                                    |                         | 78 Features        |

**Note**
for global system features (Negative Sequence, Flux Phase Angle):
Use phase A as the master reference. The Negative Sequence calculation and the Flux-Current Phase Angle just need a single, consistent baseline index to compare the waves. phase A is the standard industry choice for this baseline.
