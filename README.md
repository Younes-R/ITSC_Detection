## Feature Enginnering:

We have the follwiing set of extracted features:

### 1. Time-Domain Features:

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

### 2. Frequency Domain Features:

13. fundamental frequency: one per csv file (derived from phase A)
14. harmonic magnitudes: for each current and the flux
15. total harmonic distortion: for each current and the flux
16. spectral centroid: for each current and the flux
17. spectral spread: for each current and the flux
18. sideband ratio: for each current

### 3. Three-Phase Specific Features:

19. phase imbalance: one per csv file
20. park vector stats: one per csv file
21. flux-current phase angle: one per csv file
22. negative sequence current: one per csv file

| Feature Category | Feature Name                                                                                       | Applied To              | Total Column Count |
| ---------------- | -------------------------------------------------------------------------------------------------- | ----------------------- | ------------------ |
| Time Domain      | "Mean, Std, RMS, Peak2Peak, Skewness, Kurtosis, Crest, Form, Clearance, ZCR, Energy"               | "ia​,ib​,ic​, and Flux" | 11×4=44            |
| Frequency Domain | "Harmonic Magnitudes (3rd, 5th, 7th), THD, Spectral Centroid, Spectral Spread"                     | "ia​,ib​,ic​, and Flux" | 6×4=24             |
| Frequency Domain | Sideband Ratio                                                                                     | "ia​,ib​,ic​ only"      | 1×3=3              |
| Global System    | "Fundamental Freq, Phase Imbalance, Park Vector Stats (x3), Flux-Current Phase, Negative Sequence" | Combined System         | 7                  |
| Grand Total      |                                                                                                    |                         | 78 Features        |

**Note**
For Global System Features (Negative Sequence, Flux Phase Angle):
Use Phase A as the master reference. The Negative Sequence calculation and the Flux-Current Phase Angle just need a single, consistent baseline index to compare the waves. Phase A is the standard industry choice for this baseline.
