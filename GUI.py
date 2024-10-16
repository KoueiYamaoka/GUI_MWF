"""Main file for starting the GUI."""

import tomllib
from pathlib import Path

import wx

import MWF
from comp.mainframe import MainFrame
from functions.my_exceptions import SourceNumberError


class AppMWF(wx.App):
    """
    Main class inherited from wx.App.

    Initialize MWF object and generate mainframe instance here.
    """

    def OnInit(self) -> None:
        # load
        with open("config.toml", "rb") as f:
            config = tomllib.load(f)

        target_dir = Path(config["Paths"]["target_dir"])
        interf_dir = Path(config["Paths"]["interf_dir"])

        target_path = [str(f) for f in target_dir.glob("*.wav")]
        interf_paths = [str(f) for f in interf_dir.glob("*.wav")]
        snr = config["Simulation"]["SNR"]

        if len(target_path) != 1:
            raise SourceNumberError("target", 1)

        # prepare MWF
        self.mwfo = MWF.MWF(config)
        self.mwfo.load_data(target_path[0], interf_paths)
        self.mwfo.transform(self.mwfo.train)
        self.mwfo.transform(self.mwfo.test)
        self.mwfo.calc_features()
        self.mwfo.filter_init()
        self.mwfo.run()
        self.mwfo.inv_transform()
        self.mwfo.calc_spectrogram()

        # generate GUI
        frame = MainFrame(self.mwfo, config)

        # set event
        frame.Bind(wx.EVT_CLOSE, self.ExitHandler)

        # show GUI
        frame.Show()
        return True

    def ExitHandler(self, evt) -> None:
        evt.Skip()


if __name__ == "__main__":
    app = AppMWF()
    app.MainLoop()
