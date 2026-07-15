"""Generate the illustrative complexity figure used in Chapter 4."""

from pathlib import Path
import os

os.environ.setdefault("MPLCONFIGDIR", "/tmp/codex-matplotlib")

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "figures" / "complexity-plot.pdf"


def main() -> None:
    x = np.arange(1, 101)
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(x, np.log2(x), label=r"$\log_2 n$", linewidth=2)
    ax.plot(x, x, label=r"$n$", linewidth=2)
    ax.plot(x, x * np.log2(x), label=r"$n\log_2 n$", linewidth=2)
    ax.plot(x, x**2 / 20, label=r"$n^2/20$", linewidth=2)
    ax.set_xlabel("input size n")
    ax.set_ylabel("illustrative operation growth")
    ax.set_title("Asymptotic growth is a comparison of rates")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUTPUT, metadata={"Title": "Illustrative complexity curves"})
    plt.close(fig)


if __name__ == "__main__":
    main()
