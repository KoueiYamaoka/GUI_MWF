"""Test script of multichannel Wiener filter."""

import MWF

if __name__ == "__main__":
    # initialization

    # load
    target_path = "wav/dev1_female3_liverec_130ms_5cm_sim_1.wav"
    interf_paths = [
        "wav/dev1_female3_liverec_130ms_5cm_sim_2.wav",
        "wav/dev1_female3_liverec_130ms_5cm_sim_3.wav",
    ]

    stream = MWF.MWF()
    stream.load_data(target_path, interf_paths)
    stream.transform(stream.train)
    stream.transform(stream.test)
    stream.calc_features()
    stream.filter_init()

    stream.run(mu=0)
    stream.inv_transform()
    stream.write("out/", "y0.wav")

    stream.run(mu=1)
    stream.inv_transform()
    stream.write("out/", "y1.wav")

    stream.run(mu=10)
    stream.inv_transform()
    stream.write("out/", "y10.wav")

    stream.run(mu=100)
    stream.inv_transform()
    stream.write("out/", "y100.wav")

    print("done")
