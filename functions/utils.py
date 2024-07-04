"""utlis: utility functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


def set_snr(si: NDArray[np.float64], ni: NDArray[np.float64], snr: float) -> tuple(
    NDArray[np.float64], float
):
    """
    Set signal-to-noise ratio (SNR) to desired value.

    Parameters
    ----------
    si: array_like (n_samples, n_ch)
        Signal
    ni: array_like (n_samples, n_ch)
        Noise
    snr: int or float
        Desired SNR

    Return
    ----------
    no: array_like (n_samples, n_ch)
        Amplitude-modified noise
    coef: float
        Coefficient used for amplitude modification

    """
    n_samples, n_ch = si.shape

    # Check shape
    transposed_input = False
    if n_ch > n_samples:
        transposed_input = True
        si = si.T
        ni = ni.T
        n_samples, n_ch = si.shape

    # main
    ss_s, ss_n = 0, 0
    for c in range(n_ch):
        ss_s += si[:, c].T @ si[:, c]
        ss_n += ni[:, c].T @ ni[:, c]

    in_snr = 10 * np.log10(ss_s / ss_n)
    coef = 10 ** ((in_snr - snr) / 20)

    # out
    no = ni * coef
    if transposed_input:
        no = no.T

    return no, coef


def calc_scm(X: NDArray[np.complex64]) -> NDArray[np.complex64]:
    """Compute spatial covariance matrix."""
    V = X @ X.conj().swapaxes(1, 2)
    return V / X.shape[2]


def calc_rtf(X: NDArray[np.complex64]) -> NDArray[np.complex64]:
    """Compute relative transfer functions."""
    n_freq, n_ch, n_frame = X.shape
    V = calc_scm(X)

    # Transfer function
    a = np.zeros([n_freq, n_ch], dtype="complex64")
    for f in range(n_freq):
        val, vec = np.linalg.eig(np.squeeze(V[f, :, :]))
        idx = val.argsort()[-1]
        a[f, :] = vec[:, idx]

    # Relative transfer function
    a[:, 0] += (a[:, 0] == 0) * 0.001
    a /= a[:, 0, np.newaxis]

    return a
