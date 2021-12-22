# Introduction
This is a project under development

Note that the Docker implementation is not yet ready.
## Install virtual environment
I use python version 3.8.7, but any version that supports pygame 2.0 should work. In order to be able to run the code you need a virtual environment with all required dependencies. Here is how to install it, after you have cloned the repository:
1. Open a terminal in the repo and run the following commands
2. python -m venv .env
3. source .env/bin/activate
4. pip install --upgrade pip
5. pip install -r requirements.txt

## Run game with manual controls
Make sure to have your virtual environment activated and run
python game.py

To change start location of vehicle or parking spot, use the following flags:
--parking_pos or -pp for parking position
--car_pos or -cp for car initial position

note that both flags take two integers as input, x position and y position in pixels.

Example:
python game.py -pp 1000 200 -cp 200 500
