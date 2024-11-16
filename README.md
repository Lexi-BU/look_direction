# look_direction
Repository for the real-time look direction values for LEXI

## Description
This repository contains the code for the real-time look direction values for LEXI. The code is
written in python3 and uses the tkinter library for the GUI and matplotlib for plotting the look
direction values.

The code uses a lookup table to retrieve the look direction values for a given time. The lookup
table is a csv file that contains the look direction values for a given time. The csv file is
located in the look_direction/data directory.

The code reads the csv file and stores the look direction values in a pandas dataframe. The code
then uses the pandas dataframe to retrieve the look direction values for a given time.

Once it is opened, it looks like this:
![Look Direction Viewer](../figures/lexi_look_direction_viewer.png)

## Installation


### Using python3

- Navigate to the directory where you want to clone the repository.

- Clone the repository using the following command:
```bash
git clone https://github.com/Lexi-BU/look_direction.git
```
- cd into the look_direction/codes directory:
```bash
cd look_direction/codes
```

- Create a virtual environment using python3 and activate it using the following commands:
```bash
python3 -m venv lexi_look_direction
source lexi_look_direction/bin/activate
```

- Install the following required packages:
```bash
pip install pandas>=2.2.3
pip install tk
pip install matplotlib=3.5.1
```

- Run the following command:
```bash
python3 main.py
```