import wx

from comp.parameter_panel import ParameterPanel
from comp.plot_panel import PlotPanel


class MainFrame(wx.Frame):
    """Main frame inherited from wx.Panel."""

    def __init__(self, mwfo) -> None:
        # size
        self.width = 1080 + 460
        self.height = 1080
        self.fs = 16

        # size calculation
        self.r_width = self.width - self.height

        # initialization
        super().__init__(
            None,
            wx.ID_ANY,
            "Speech Distortion Weighted Multichannel Weiner Filter",
            size=(self.width, self.height),
        )

        # icon
        # path_to_icon = "./icon/hoge.png"
        # self.SetIcon(wx.Icon(path_to_icon, wx.BITMAP_TYPE_PNG))

        # main panel
        p_main = wx.Panel(self, wx.ID_ANY)

        # child panels under the main panel
        p_plot = PlotPanel(p_main, (self.height, self.height), self.fs, mwfo)
        p_param = ParameterPanel(p_main, (self.r_width, self.height), mwfo)

        # layout of child panels
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(p_plot, proportion=1, flag=wx.EXPAND)
        layout.Add(p_param, proportion=0, flag=wx.EXPAND)

        p_main.SetSizer(layout)
