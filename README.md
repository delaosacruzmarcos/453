# Micro-Controller
repository for storing and managing code, to be flashed upon the launcher micro controller

### Switches.py
Creatin of a switch object that manages the states of the activate left & right launch barrel switches. The green ones on the controller. The class also is used to update features in the MasterGUI to be displayed to the user.

### Pinout.py
conatins class enum for each of the pins of the Raspberry GPIO. That way in the case you have to update what pin does what you should only have to change it in one location

### MasterGui 
responsible for the creation of the GUI displayed to the user on the controller. This GUI calls hardware modules like switches and buttons to update the itself. Please read the API for any hardware module before you change the way the commands interact with the GUI... We haven't wrote the API yet lol