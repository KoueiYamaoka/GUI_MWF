"""MWF: multichannel Wiener filter."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import soundfile as sf
from numpy.random import default_rng

from functions import utils
from functions.STFT import iSTFT, mSTFT

if TYPE_CHECKING:
    from numpy.typing import NDArray


class SIGNAL:
    """Class for structure that holds the signals."""

    def __init__(self) -> None:
        """
        Signals structure.

        s: target signal
        i: interferers (noise emitted from a point source)
        n: noise
        x: mixture
        Uppercase letters: STFT representations
        """
        self.s = None
        self.i = None
        self.n = None
        self.x = None

        self.S = None
        self.I = None
        self.N = None
        self.X = None


class MWF:
    """Class: Multichannel Wiener Filter (MWF)."""

    def __init__(self) -> None:
        """Initialize."""
        self.rg = default_rng(577)
        self.mu = 1

    def load_data(self, target_path: str, interf_paths: list, snr: int = 20) -> None:
        """
        Load data.

        Parameters
        ----------
        target_path: str
            relative path to the target signal

        interf_paths: list of str
            relative paths to the interferer signals

        snr: int
            input SNR (signal-plus-interferes to noise ratio)

        """
        self.snr = snr

        # load
        raw = SIGNAL()

        # target signal
        raw.s, self.fs = sf.read(target_path)

        # interferers
        raw.i = np.zeros(raw.s.shape + (len(interf_paths),))
        for i, p in enumerate(interf_paths):
            raw.i[:, :, i], _ = sf.read(p)

        # noise and mixture
        raw.x = raw.s + np.sum(raw.i, axis=2)
        raw.n = self.rg.random(np.shape(raw.s))
        raw.n, _ = utils.set_snr(raw.x, raw.n, self.snr)

        self.raw = raw

        # prepare train and test data
        test = SIGNAL()
        train = SIGNAL()

        # train
        train.s = self.raw.s[5 * self.fs + 1 :]
        train.i = self.raw.i[5 * self.fs + 1 :]
        train.n = self.raw.n[5 * self.fs + 1 :]
        train.x = train.s + np.sum(train.i, axis=-1) + train.n

        # test
        test.s = self.raw.s[0 : 5 * self.fs]
        test.i = self.raw.i[0 : 5 * self.fs]
        test.n = self.raw.n[0 : 5 * self.fs]
        test.x = test.s + np.sum(test.i, axis=-1) + test.n

        self.train = train
        self.test = test

    def set_data_snr(self) -> None:
        """Set data SNR."""
        # load
        self.raw.n, _ = utils.set_snr(self.raw.x, self.raw.n, self.snr)

        # train
        self.train.s = self.raw.s[5 * self.fs + 1 :]
        self.train.i = self.raw.i[5 * self.fs + 1 :]
        self.train.n = self.raw.n[5 * self.fs + 1 :]
        self.train.x = self.train.s + np.sum(self.train.i, axis=-1) + self.train.n

        # test
        self.test.s = self.raw.s[0 : 5 * self.fs]
        self.test.i = self.raw.i[0 : 5 * self.fs]
        self.test.n = self.raw.n[0 : 5 * self.fs]
        self.test.x = self.test.s + np.sum(self.test.i, axis=-1) + self.test.n

    def transform(
        self,
        signal: SIGNAL,
        frlen: int = 2048,
        frsft: int | None = None,
        wnd: NDArray[np.float64] | None = None,
    ) -> None:
        """Perform STFT."""
        # parameters
        self.frlen = frlen
        self.frsft = self.frlen // 2 if frsft is None else frsft
        self.wnd = np.hamming(self.frlen) if wnd is None else wnd

        # STFT
        signal.S = mSTFT(signal.s, self.frlen, self.frsft, self.wnd).transpose(2, 0, 1)
        signal.I = np.zeros(signal.S.shape + (signal.i.shape[2],), dtype=np.complex64)
        for i in range(signal.i.shape[2]):
            signal.I[:, :, :, i] = mSTFT(
                signal.i[:, :, i], self.frlen, self.frsft, self.wnd
            ).transpose(2, 0, 1)
        signal.N = mSTFT(signal.n, self.frlen, self.frsft, self.wnd).transpose(2, 0, 1)
        signal.X = signal.S + np.sum(signal.I, axis=-1) + signal.N

    def calc_features(self) -> None:
        """
        Calculate features for filter computation.

        Features
        --------
        a: array_like (n_freq, n_ch)
            Relative transfer functions
        V: array_like (n_freq, n_ch, n_ch)
            Covariance matrix
        ss: array_like (n_freq, )
            Desired signal variance

        """
        self.a = utils.calc_rtf(self.train.S)
        self.ss = utils.calc_scm(self.train.S)[:, 0, 0]
        self.V = utils.calc_scm(self.train.X - self.train.S)

    def filter_init(self) -> None:
        """Compute numerator and denominator of MWF coefficients except for mu."""
        # aliases
        self.x = self._mod_amp(self.test.x)
        self.X = self.test.X

        # preparation
        ss = self.ss[:, None, None]
        a = self.a[:, :, None]
        ah = a.conj().swapaxes(1, 2)
        V_inv = np.linalg.inv(self.V)

        self.numrt = ss * V_inv @ a
        self.denom = ss * ah @ V_inv @ a

    def run(self, mu: int = 1) -> None:
        """
        Perform multichannel Wiener filter with given mu.

        Parameter
        ---------
        mu: int
            tradeoff factor betweeen speech distortion and noise reduction.
            mu = 1: MWF (default)
            mu = 0: MVDR

        Returns
        -------
        Y: array_like (n_freq, n_frame)
            Output
        W: float
            MWF

        """
        # main
        self.W = self.numrt / (mu + self.denom)

        # apply filter
        self.Y = self.W.conj().swapaxes(1, 2) @ self.X

        # muda na syori
        self.Y = np.squeeze(self.Y).T

    def inv_transform(self) -> None:
        """Perform inverse STFT."""
        self.y = iSTFT(self.Y, self.frsft, self.wnd)
        self.y = self._mod_amp(self.y)

    def write(self, path: str, fn: str) -> None:
        """Write input and output signals."""
        sf.write(path + "x.wav", self._mod_amp(self.x), self.fs)
        sf.write(path + fn, self._mod_amp(self.y), self.fs)

    def _mod_amp(self, x: NDArray[np.complex64]) -> NDArray[np.complex64]:
        """Naive normalization."""
        return x / np.max(np.abs(x)) / 2

    def calc_spectrogram(self) -> None:
        """Prepare spectrograms."""
        self.x_spec = 20 * np.log10(np.abs(self.X[:, 0, :]))
        self.y_spec = 20 * np.log10(np.abs(self.Y))
