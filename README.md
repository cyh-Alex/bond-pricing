# Bond Pricing

This repository contains small utilities for analyzing yield curves.

## PCA on the Yield Curve

The script `pca_yield_curve.py` loads a CSV file of daily yields across
maturities and performs principal component analysis (PCA).  The first
three principal components are plotted and the explained variance ratio
and component loadings are saved to CSV files.

### Usage

```bash
python pca_yield_curve.py yield_curve.csv
```

The CSV file should have one row per date and one column per maturity
(e.g. `1Y`, `2Y`, ... `30Y`).  Any rows with missing values are dropped
before running PCA.

The script produces the following outputs:

- `explained_variance.csv` - variance explained by each component
- `component_loadings.csv` - PCA loadings for each maturity
- `principal_components.png` - plot of the first three components

The printed messages describe the usual interpretation of the first three
components: level, slope and curvature.
