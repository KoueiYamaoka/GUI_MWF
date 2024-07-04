import sounddevice as sd
import wx

border = 8


class RunSizer(wx.StaticBoxSizer):
    """Sizer to place execution-related buttons, etc."""

    def __init__(self, parent, fontsize, mwfo) -> None:
        # prepare box
        bx = wx.StaticBox(parent, wx.ID_ANY, "Main")
        gs = wx.GridSizer(rows=2, cols=2, gap=(border, border * 2))

        # Initialization
        super().__init__(bx, wx.VERTICAL)
        self.mwfo = mwfo

        # genrerate buttons
        bt_run = wx.Button(parent, wx.ID_ANY, "Run", style=wx.RB_GROUP)
        bt_ply = wx.Button(parent, wx.ID_ANY, "Play", style=wx.RB_GROUP)

        # set font
        font = wx.Font(
            fontsize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
        )
        bx.SetFont(font)
        bt_run.SetFont(font)
        bt_ply.SetFont(font)

        # set buttons
        gs.Add(bt_run)
        gs.Add(bt_ply)
        self.Add(gs, flag=wx.LEFT, border=border)

        # set events for each button
        bt_run.Bind(wx.EVT_BUTTON, self.run)
        bt_ply.Bind(wx.EVT_BUTTON, self.ply)

    def run(self, evt) -> None:
        """Perform MWF with current mu."""
        self.mwfo.run(mu=self.mwfo.mu)
        self.mwfo.inv_transform()

    def ply(self, evt) -> None:
        """Play enahnced signal."""
        sd.play(self.mwfo.y, self.mwfo.fs)


class ParamSizer(wx.StaticBoxSizer):
    """Sizer to place parameter-related buttons, etc."""

    def __init__(self, parent, fontsize, mwfo) -> None:
        # prepare box
        bx = wx.StaticBox(parent, wx.ID_ANY, "Parameters")

        # Initialization
        super().__init__(bx, wx.VERTICAL)
        self.mwfo = mwfo

        # generate slider
        txt_mu = wx.StaticText(parent, label="mu")
        sl_mu = wx.Slider(
            parent,
            wx.ID_ANY,
            style=wx.SL_LABELS,
            value=self.mwfo.mu,
            minValue=0,
            maxValue=100,
            size=(400, 100),
        )

        # set font
        font = wx.Font(
            fontsize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
        )
        bx.SetFont(font)
        txt_mu.SetFont(font)
        sl_mu.SetFont(font)
        sl_mu.SetBackgroundColour(parent.GetBackgroundColour())

        # set slider
        self.Add(txt_mu, flag=wx.LEFT | wx.TOP, border=border)
        self.Add(sl_mu, flag=wx.LEFT | wx.TOP | wx.BOTTOM, border=border)

        # set event for slider
        sl_mu.Bind(wx.EVT_SLIDER, self.set_mu)

    def set_mu(self, evt) -> None:
        """Get mu value from the slider."""
        obj = evt.GetEventObject()
        self.mwfo.mu = obj.GetValue()
