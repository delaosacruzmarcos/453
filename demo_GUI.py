# --------------- #
# Team Rocket 2023
# Author Marcos De La Osa Cruz
# User displayed GUI, walks the user through the launching 
# Displays launch information to the user (rocket angle and rotation)
# Count down to launch 

#-----Imports----#
import tkinter
import tkinter.messagebox
import customtkinter
import os
from LaunchDrum import *
import UserText
from demo_pattern import *
from pinout import *
from Joysticks import *
from Switches import *



customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



class App(customtkinter.CTk):
        #----------Event handling---------#
    def testEvent(self,event):
        print('hello world')
        self.user_state.presentState()

    # Handles the left switch event 
    def leftSwitchToggle(self,event):
        # tie this to the state machine
        print("left switch")
        self.user_state.leftSwitchToggle()

    
    # Handles the right switch event
    def rightSwitchToggle(self,event):
        # tie this to the state machine
        print("right switch toggled")
        self.user_state.rightSwitchToggle()

    def __init__(self, rightLaunchDrum, leftLaunchDrum, Launcher: Launcher, pinout: Pinout, switch: Switch):
        super().__init__()

        #Launch Drum controllersl
        self.rDrum = rightLaunchDrum
        self.lDrum = leftLaunchDrum
        self.user_state = Launcher
        self.pinout = pinout
        self.switch = switch

        # configure window
        self.title("University at Buffalo Rocket Launcher Software")
        self.geometry(f"{1100}x{580}")


        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

         #----------Left Frame----------#
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # Program title
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Rocket Launcher", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=0, pady=(20, 0))
 
        # create radiobutton frame
        self.state_var = tkinter.IntVar(value=10) #We start the in the loading state
        self.label_radio_group = customtkinter.CTkLabel(self.sidebar_frame, text="Current Stage of Launch:")
        self.label_radio_group.grid(row=1, column=0, columnspan=1, padx=10, pady=10, sticky="")
        self.load_state_button = customtkinter.CTkRadioButton(self.sidebar_frame, variable=self.state_var, value=0, text="Load")
        self.load_state_button.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.aim_state_button = customtkinter.CTkRadioButton(self.sidebar_frame, variable=self.state_var, value=1, text="Aim")
        self.aim_state_button.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        self.pressurize_state_button = customtkinter.CTkRadioButton(self.sidebar_frame, variable=self.state_var, value=2, text="Pressurizing")
        self.pressurize_state_button.grid(row=4, column=0, pady=10, padx=20, sticky="n")
        self.launch_state_button = customtkinter.CTkRadioButton(self.sidebar_frame, variable=self.state_var, value=3, text="Launch")
        self.launch_state_button.grid(row=5, column=0, pady=10, padx=20, sticky="n")



        #----------Middle Frame----------#GPIOPINS0, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")





        # Stages 
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0,rowspan=2, column=1,columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Load Stage")
        self.tabview.add("Aim Stage")
        self.tabview.add("Pressurization")
        self.tabview.add("Launch Stage")
        self.tabview.tab("Load Stage").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Aim Stage").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Pressurization").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Launch Stage").grid_columnconfigure(0, weight=1)

        #Progress bar
        self.launch_progressbar = customtkinter.CTkProgressBar(self.tabview)
        self.launch_progressbar.grid(row=0, column=0, padx=(20, 20), pady=(10, 10), sticky="ew")

        #Load
        self.Load_textbox = customtkinter.CTkTextbox(self.tabview.tab("Load Stage"), width=250, height=350)
        self.Load_textbox.grid(row=1,rowspan=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        

        #Aim
        self.Aim_textbox = customtkinter.CTkTextbox(self.tabview.tab("Aim Stage"), width=250, height=350)
        self.Aim_textbox.grid(row=0,rowspan=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        #Pressurization
        self.Pressurization_textbox = customtkinter.CTkTextbox(self.tabview.tab("Pressurization"), width=250, height=350)
        self.Pressurization_textbox.grid(row=0,rowspan=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        #Launch
        self.Launch_textbox = customtkinter.CTkTextbox(self.tabview.tab("Launch Stage"), width=250, height=350)
        self.Launch_textbox.grid(row=0,rowspan=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")


        #----------Right Frame----------#
        # Left Rocket information
        self.Left_Rocket_frame = customtkinter.CTkFrame(self)
        self.Left_Rocket_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.Left_Rocket_label_group = customtkinter.CTkLabel(master=self.Left_Rocket_frame, text="Left Rocket Information:")
        self.Left_Rocket_label_group.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky="")
        self.Left_Rocket_textbox = customtkinter.CTkTextbox(master=self.Left_Rocket_frame, width=200, height=150)
        self.Left_Rocket_textbox.grid(row=1, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew")


        # Right Rocket information
        self.Right_Rocket_frame = customtkinter.CTkFrame(self)
        self.Right_Rocket_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.Right_Rocket_label_group = customtkinter.CTkLabel(master=self.Right_Rocket_frame, text="Right Rocket Information:")
        self.Right_Rocket_label_group.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky="")
        self.Right_Rocket_textbox = customtkinter.CTkTextbox(master=self.Right_Rocket_frame, width=200, height=150)
        self.Right_Rocket_textbox.grid(row=1, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew")


        #----------Event Handling----------#


    # updates the GUI when a state change occurs using States.py
    def change_state(self, state):
        self.user_state.changeState(state)


    # Initialize all the function call backs
    def eventInit(self):

        self.event_add('<<left-switch>>','<l>')
        self.bind('<<left-switch>>',self.leftSwitchToggle)


    # Update launch drums on screen  
    def updateLaunchDrumInformation(self):
        rHeight = rDrum.getHeight()
        lHeight = lDrum.getHeight()
        rRotate = rDrum.getRotation()
        lRotate = lDrum.getRotation()
        rActive = rDrum.getActivationStatus()
        lActive = lDrum.getActivationStatus()
        self.Left_Rocket_textbox.insert("0.0","Activation status: "+str(lActive)+"\nHeight: "+str(lHeight)+"\nRotation: "+str(lRotate))
        self.Right_Rocket_textbox.insert("0.0","Activation status: "+str(rActive)+"\nHeight: "+str(rHeight)+"\nRotation: "+str(rRotate))

    def updateUserText(self):
        boxes = [self.Load_textbox, self.Launch_textbox, self.Aim_textbox, self.Pressurization_textbox]
        for box in boxes:
            text = UserText.getText(self.user_state.userTextPhony())
            box.insert("0.0",text)


if __name__ == "__main__":
    rDrum = LaunchDrum("hello")
    lDrum = LaunchDrum("hello")
    launcher = Launcher(Load())
    pins = Pinout()
    sw = Switch(pins)
    app = App(rDrum,lDrum, launcher, pins, Switch)
    app.eventInit()
    app.updateLaunchDrumInformation()
    app.updateUserText()
    app.mainloop()
