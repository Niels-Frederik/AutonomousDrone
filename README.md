## AutonomousDrone
Welcome to AutonomousDrone <br/>
By **Niels-Frederik** and **Yarlermanden** <br/>

This project aims to control a drone autonomously by getting its video feed, analysing it and taking action oppon it to avoid collisions

## Requirements
**[Install necessary model](https://s3-eu-west-1.amazonaws.com/densedepth/nyu.h5)** <br/>
This is only required for DenseDepth - mode 1. <br/>
In case the link doesn't work. Go to [DenseDepth's github](https://github.com/ialhashim/DenseDepth) to hopefully find an updated link for the  "NYU Depth V2" trained model

**Drone network** <br/>
In case of running live with drone. You should connect to the drones wifi before starting the program.

**Install virtual environment** <br/>
Create a virtual environment and install packages from one of the three requirements.txt files depending on which mode you wish to run <br/>
* denseDepthRequirements.txt <br/>
requires python 3.8.5
* pydnetRequirements.txt <br/>
requires python 3.7.10
* fastDepthRequirements.txt <br/>
requires python 3.8.5

```
python3.8 -m venv ./fastDepthVenv
source fastDepthVenv/bin/activate
pip install -r fastDepthRequirements.txt
```

## Arguments
Below is the optional parameters to the main.py

**mode** <br/>
Used to determine which model and mode is used. <br/>
1 = DenseDepth, 2 = PyDNet, 3 = FastDepth
```
--mode 3 
```

**remoteView** <br/>
Used to enable remote view of the input and output images via internet
```
--remoteView False
```

**localView** <br/>
Used to choose whether to locally view the input and output images. Use --localView "" to set to false
```
--localView True
```

**debug** <br/>
Used to show extra images and print which action the drone tries to take
```
--debug False
```

**live** <br/>
Used to choose whether to run with the drone or from a preloaded video
```
--live False
```

**video** <br/>
Used to choose the path of the video used as input in case of not running live with the drone
```
--video ../Source/Video/droneVideo4.0.mp4
```

## How to run
After enabling the desired virtual environment got to the src folder <br/>
From here run the program with the desired parameters.

```
cd src/
python main.py --live True --mode 2
```
