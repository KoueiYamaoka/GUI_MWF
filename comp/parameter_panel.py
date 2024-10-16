import wx

import comp.parameter_sizers as pp


class ParameterPanel(wx.Panel):
    """Parameter related panel inherited from wx.Panel."""

    def __init__(self, parent, size, mwfo) -> None:
        super().__init__(parent, wx.ID_ANY, size=size)

        # generate panels
        layout_data = pp.DataSizer(self, mwfo)
        layout_run = pp.RunSizer(self, mwfo)
        layout_param = pp.ParamSizer(self, mwfo)

        # set panels
        layout = wx.BoxSizer(wx.VERTICAL)
        bdr = 10
        layout.Add(
            layout_data,
            flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
            border=bdr,
        )
        layout.Add(
            layout_run,
            flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
            border=bdr,
        )
        layout.Add(
            layout_param,
            flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
            border=bdr,
        )

        # set sizer
        self.SetSizer(layout)
