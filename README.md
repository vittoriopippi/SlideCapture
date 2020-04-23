# SlideCapture
SlideCapture is a simple script that analyze a video and extract the slides rafigured in it. In order to avoid that every frame of the video is saved, the scipt calculate the difference between the frames and save the slide only when there are enough changes.

This is a very simple animation that explains how the scripts works.
![Simple toy animation](https://github.com/vittoriopippi/SlideCapture/blob/master/images/simple_explanation.gif?raw=true)

### How to install
To use this script you have to install the requirements executing the command:
`pip install -r requirements.txt`

### How to use it
The script accepts differents parameters:

| Parameter | Description                    |Default|
| ---------------------------- | ------------------------------ | ------------------------------ |
| `-i` or `--input` | path of the video that will be analyzed | required |
| `-o` or `--output` | path of the folder where the slides will be saved | see output |
| `--start-at` | at which seconds start analyzing the video | 0 |
| `-s` or `--step` | every how many seconds the video il be analyzed | 2 |
| `--sample-heigth` | height of the samples that will be compared | 100 |
| `-s` or `--step` | every how many seconds the video il be analyzed | 2 |
| `-s` or `--step` | every how many seconds the video il be analyzed | 2 |
