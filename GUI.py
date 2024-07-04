import wx

import MWF
from comp.mainframe import MainFrame


class AppMWF(wx.App):
    """
    Main class inherited from wx.App.

    Initialize MWF object and generate mainframe instance here.
    """

    def OnInit(self) -> None:
        target_path = "wav/dev1_female3_liverec_130ms_5cm_sim_1.wav"
        interf_paths = [
            "wav/dev1_female3_liverec_130ms_5cm_sim_2.wav",
            "wav/dev1_female3_liverec_130ms_5cm_sim_3.wav",
        ]

        # prepare MWF
        self.mwfo = MWF.MWF()
        self.mwfo.load_data(target_path, interf_paths)
        self.mwfo.transform(self.mwfo.train)
        self.mwfo.transform(self.mwfo.test)
        self.mwfo.calc_features()
        self.mwfo.filter_init()
        self.mwfo.run()
        self.mwfo.inv_transform()
        self.mwfo.calc_spectrogram()

        # generate GUI
        frame = MainFrame(self.mwfo)

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
