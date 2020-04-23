# SlideCapture
SlideCapture is a simple script that analyze a video and extract the slides rafigured in it. In order to avoid that every frame of the video is saved, the scipt calculate the difference between the frames and save the slide only when there are enough changes.

This is a very simple animation that explains how the scripts works.

![Simple toy animation](https://github.com/vittoriopippi/SlideCapture/blob/master/images/simple_explanation.gif?raw=true)

## How to install
To use this script you have to install the requirements executing the command:
`pip install -r requirements.txt`

## Quick start
Given the path of the video that you want to analyze is `C:\Desktop\video_lession.mp4`, what you have to do is run the following command:

> `python3 SlideCapture.py --input C:\Desktop\video_lession.mp4`

After that, basically you have to follow the instruction that appear in the console.

#### Define the slide region
Will be showed you a frame of the video and asked you to click on the top-left corner of the slide. In the console you will see the coordinates of the point selected. If you want to define the the coordinates manually use the command `--manual`. 

Than you have to click on the bottom-right corner of the slide in order to define the region that will be captured.

```
In the image please select with the mouse the top-left corner of the rectangle
Found point (0, 189)

Now please select the bottom-right corner of the rectangle
Found point (1440, 994)

Found this coordinates ((0, 189), (1440, 994)) do you want to continue [y/n/cancel]?y
```

#### Define some excluding regions
After that will be asked you if you want to define some regions where the changes are not detected.

Thats because in the Google Meet room sometimes in the bottom left part of the presentation a popup appear when someone leave the call.

```
Do you want to add some excluding area [y/n]?y
In the image please select with the mouse the top-left corner of the rectangle
Found point (0, 666)

Now please select the bottom-right corner of the rectangle
Found point (1526, 1075)

Found this coordinates ((0, 666), (1526, 1075)) do you want to continue [y/n/cancel]?y

Do you want to add some excluding area [y/n]?n
```

#### Run
Once all regions are defined the script will be run and the video will be analyzed. Every time a new slide is detected it wil be stored in a folder in the same position of the video.

```
Start reading the video
SAVED   video_time=0:00:00      perc=0.00%      Diff_val=21442.78       video_lession_slide_0001.png
        video_time=0:00:02      perc=0.03%      Diff_val=00000.15
SAVED   video_time=0:00:04      perc=0.06%      Diff_val=20847.43       video_lession_slide_0002.png
SAVED   video_time=0:00:06      perc=0.08%      Diff_val=00765.10       video_lession_slide_0003.png
SAVED   video_time=0:00:08      perc=0.11%      Diff_val=14265.05       video_lession_slide_0004.png
        video_time=0:00:10      perc=0.14%      Diff_val=00000.45
        video_time=0:00:12      perc=0.17%      Diff_val=00000.76
        video_time=0:00:14      perc=0.19%      Diff_val=00000.17
        video_time=0:00:16      perc=0.22%      Diff_val=00000.75
...
```

Where the `video_time` is at wich time of the video is analyzing and the `perc` value is the percentage of the video done.  

## How to use it
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
