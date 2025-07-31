#!/usr/bin/env python3
"""Perform PCA on yield curve data.

This script loads a ``yield_curve.csv`` file containing daily yields at
various maturities (columns like ``1Y``, ``2Y`` ... ``30Y``).  Missing
values are dropped before running PCA.  The first three principal
components are plotted and saved, and the explained variance ratio as
well as the component loadings are written to CSV files.

Running the script::

    python pca_yield_curve.py yield_curve.csv

The first principal component typically represents the overall level of
the yield curve, the second captures its slope (short versus long
maturities) and the third reflects curvature.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def load_data(path: Path) -> pd.DataFrame:
    """Load yield curve data and drop rows with missing values."""
    df = pd.read_csv(path)
    df = df.dropna(how="any")
    return df


def run_pca(df: pd.DataFrame) -> PCA:
    """Fit PCA on the dataframe and return the fitted estimator."""
    pca = PCA()
    pca.fit(df)
    return pca


def plot_components(pca: PCA, columns: list[str], n_components: int = 3, output: Path = Path("principal_components.png")) -> None:
    """Plot the first ``n_components`` principal components."""
    plt.figure(figsize=(10, 6))
    for i in range(n_components):
        plt.plot(columns, pca.components_[i], label=f"PC{i+1}")
    plt.xlabel("Maturity")
    plt.ylabel("Loading")
    plt.title("First 3 Principal Components")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output)
    plt.close()


def save_results(pca: PCA, columns: list[str], variance_file: Path = Path("explained_variance.csv"), loadings_file: Path = Path("component_loadings.csv")) -> None:
    """Save explained variance ratio and loadings to CSV."""
    explained = pd.DataFrame({
        "PC": [f"PC{i+1}" for i in range(len(pca.explained_variance_ratio_))],
        "explained_variance_ratio": pca.explained_variance_ratio_,
    })
    explained.to_csv(variance_file, index=False)

    loadings = pd.DataFrame(
        pca.components_.T,
        index=columns,
        columns=[f"PC{i+1}" for i in range(pca.components_.shape[0])],
    )
    loadings.to_csv(loadings_file)


def main(argv: list[str]) -> None:
    if len(argv) != 2:
        print("Usage: python pca_yield_curve.py yield_curve.csv")
        return

    csv_path = Path(argv[1])
    df = load_data(csv_path)
    pca = run_pca(df)
    save_results(pca, list(df.columns))
    plot_components(pca, list(df.columns))

    # Provide a short textual explanation of the components.
    print("PC1 typically represents the overall level of the curve.")
    print("PC2 often corresponds to the slope between short and long maturities.")
    print("PC3 usually captures the curvature (concavity) of the curve.")


if __name__ == "__main__":
    main(sys.argv)
