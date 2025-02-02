"""Test script of multichannel Wiener filter."""

from pathlib import Path

import MWF

if __name__ == "__main__":
    # load
    target_dir = Path("wav/target")
    interf_dir = Path("wav/interf")

    target_path = [str(f) for f in target_dir.glob("*.wav")]
    interf_paths = [str(f) for f in interf_dir.glob("*.wav")]

    # main
    stream = MWF.MWF()
    stream.load_data(target_path[0], interf_paths)
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
