#--------------------------#
# CSE 453: Rocket Launcher Team
# Author: Marcos
# Date: 03/7/2023
# Boot the arduino with code from this repository. That way when, raspberry pi
# boots on power up we deploy again to our arduino
#--------------------------#

from everywhereml.arduino import Sketch, Ino, H

"""
Create a sketch object.
A sketch is defined by:
 - a name (required)
 - a folder (optional)

If you leave the folder empty, the current working directory will be used.
You can use the special name ':system:' to use the default Arduino sketches folder
(as reported by the command `arduino-cli config dump`)
"""

sketch = Sketch(name="PyDuino", folder=":system:")

"""
Then you can add files to the project (either the .ino main file or
C++ header files)
"""
sketch += Ino("""
    #include "hello.h"


    void setup() {
        Serial.begin(115200);
    }

    void loop() {
        hello();
        delay(1000);
    }
""")

sketch += H("hello.h", """
    void hello() {
        Serial.println("hello");
    }
"""