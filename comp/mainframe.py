import wx

from comp.parameter_panel import ParameterPanel
from comp.plot_panel import PlotPanel


class MainFrame(wx.Frame):
    """Main frame inherited from wx.Panel."""

    def __init__(self, mwfo, config) -> None:
        # size
        self.width = config["GUI"]["width"]
        self.height = config["GUI"]["height"]

        # fonts
        fflist = [
            wx.DEFAULT,
            wx.DECORATIVE,
            wx.ROMAN,
            wx.SCRIPT,
            wx.SWISS,
            wx.MODERN,
            wx.TELETYPE,
        ]
        self.font = wx.Font(
            config["GUI"]["base_font_size"],
            fflist[config["GUI"]["font_family"]],
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
        )

        # size calculation
        self.r_width = max(300, self.width // 4)
        self.l_width = self.width - self.r_width

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
        p_main.SetFont(self.font)

        # child panels under the main panel
        p_plot = PlotPanel(p_main, (self.l_width, self.height), self.font, mwfo)
        p_param = ParameterPanel(p_main, (self.r_width, self.height), mwfo)

        # layout of child panels
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(p_plot, proportion=1, flag=wx.EXPAND)
        layout.Add(p_param, proportion=0, flag=wx.EXPAND)

        p_main.SetSizer(layout)
