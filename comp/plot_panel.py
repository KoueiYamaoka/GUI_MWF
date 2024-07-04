import matplotlib as mpl
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg

mpl.interactive(True)
mpl.use("WXAgg")


class PlotPanel(wx.Panel):
    """Panel for displaying spectrograms inherited from wx.Panel."""

    def __init__(self, parent, size, mwfo) -> None:
        super().__init__(parent, wx.ID_ANY, size=size)
        self.fps = 5  # frame per second
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
        self.draw()

        # set timer for figures update
        self.timer = wx.Timer(self)
        self.timer.Start(1000 // self.fps)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

    def update(self, evt) -> None:
        """Routine for figures update."""
        self.mwfo.calc_spectrogram()
        self.draw(evt)

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
        self.subplot1.set_title("Observation")
        self.subplot1.set_xlabel("Time")
        self.subplot1.set_ylabel("Frequency")

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
        self.subplot2.set_xlabel("Time")
        self.subplot2.set_ylabel("Frequency")

        self.canvas.draw()
