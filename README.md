# GUI for Speech Distortion Weighted Multichannel Wiener Filter

## Installation
```shell
$ poetry install
```

## Configuration
- See config.toml

## Preparation
- Place your audio files in the following directories (these paths can be modified):
  - Target signal: ./data/target
  - Interference signals: ./data/interf
- Notes:
  - Both must be multichannel signals of the same length.
  - The number of sources and microphones will be determined by the files provided.


## Usage
### GUI
```shell
$ python GUI.py
```

### Batch process
```shell
$ mkdir out
$ python batch_process
```

## Notes
- The filter is designed using true signals from a different segment than the one being enhanced.
  - Specifically, the filter is created using the latter part of the provided signals and applied to the former part.
- The SNR displayed on the GUI reflects the signal-plus-interferers to noise ratio.
