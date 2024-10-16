import matplotlib as mpl
import numpy as np
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg

mpl.interactive(True)
mpl.use("WXAgg")


class PlotPanel(wx.Panel):
    """Panel for displaying spectrograms inherited from wx.Panel."""

    def __init__(self, parent, size, font, mwfo) -> None:
        super().__init__(parent, wx.ID_ANY, size=size)
        self.fps = 5  # frame per second
        self.font = font
        self.fs = font.GetPointSize()
        self.ff = font.GetFaceName()
        self.mwfo = mwfo

        # mpl figure
        self.figure = mpl.figure.Figure(None)
        self.figure.set_facecolor((0.9, 0.9, 1.0))
        self.subplot1 = self.figure.add_subplot(211)
        self.subplot2 = self.figure.add_subplot(212)

        # prepare canvas
        self.canvas = FigureCanvasWxAgg(self, -1, self.figure)
        self.canvas.SetBackgroundColour(wx.Colour(100, 255, 255))

        # set sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.draw_init()
        self.draw()

        # set timer for figures update
        self.timer = wx.Timer(self)
        self.timer.Start(1000 // self.fps)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

    def update(self, evt) -> None:
        """Routine for figures update."""
        self.mwfo.calc_spectrogram()
        self.draw(evt)

    def draw_init(self) -> None:
        self.di = dict(
            fbin=np.round(np.linspace(0, self.mwfo.X.shape[0], 9)).astype(int),
            fbin_txt=[str(i) for i in [0, 1, 2, 3, 4, 5, 6, 7, 8]],
            frm=np.linspace(0, self.mwfo.X.shape[2] - 1, 6),
            frm_txt=[str(i) for i in range(6)],
        )

        styles = {
            "font.family": self.ff,
            "font.size": self.fs + 1,
            "xtick.labelsize": self.fs - 2,
            "ytick.labelsize": self.fs - 2,
            "figure.labelsize": self.fs + 1,
            "axes.labelsize": self.fs + 1,
            "axes.labelpad": 7,
            "axes.titlesize": self.fs + 1,
        }
        mpl.pyplot.rcParams.update(styles)

    def draw(self, evt=None) -> None:
        """Routine for drawing figures."""

        # observation
        self.subplot1.cla()
        self.subplot1.imshow(
            self.mwfo.x_spec,
            aspect="auto",
            origin="lower",
            cmap="jet",
            vmin=-60,
            vmax=6,
            interpolation="antialiased",
        )

        self.subplot1.set_title("Observed signal")
        self.subplot1.set_xlabel("Time [s]")
        self.subplot1.set_ylabel("Frequency [kHz]")
        self.subplot1.set_yticks(self.di["fbin"])
        self.subplot1.set_yticklabels(self.di["fbin_txt"])
        self.subplot1.set_xticks(self.di["frm"])
        self.subplot1.set_xticklabels(self.di["frm_txt"])

        # output
        self.subplot2.cla()
        self.subplot2.imshow(
            self.mwfo.y_spec.T,
            aspect="auto",
            origin="lower",
            cmap="jet",
            vmin=-60,
            vmax=6,
            interpolation="antialiased",
        )
        self.subplot2.set_title("Enhanced signal")
        self.subplot2.set_xlabel("Time [s]")
        self.subplot2.set_ylabel("Frequency [kHz]")
        self.subplot2.set_yticks(self.di["fbin"])
        self.subplot2.set_yticklabels(self.di["fbin_txt"])
        self.subplot2.set_xticks(self.di["frm"])
        self.subplot2.set_xticklabels(self.di["frm_txt"])

        self.figure.tight_layout()

        self.canvas.draw()
