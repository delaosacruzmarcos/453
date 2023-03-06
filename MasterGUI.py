import tkinter
import tkinter.messagebox
import customtkinter
import os
from PIL import Image

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("University at Buffalo Rocket Launcher")
        self.geometry(f"{1100}x{580}")


        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # load and display logo image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.Rocket_logo = customtkinter.CTkImage(Image.open(os.path.join( image_path,"rocket_logo_c.png")),
                                               size=(200,200))
        # Program title
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Rocket Launcher", image = self.Rocket_logo, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=0, pady=(20, 0))

 
        # create radiobutton frame
        self.state_var = tkinter.IntVar(value=0)
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


        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

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
        self.Load_textbox = customtkinter.CTkTextbox(self.tabview.tab("Load Stage"), width=250)
        self.Load_textbox.grid(row=1,rowspan=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        

        #Aim
        self.Aim_textbox = customtkinter.CTkTextbox(self.tabview.tab("Aim Stage"), width=250)
        self.Aim_textbox.grid(row=0,rowspan=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        #Pressurization
        self.Pressurization_textbox = customtkinter.CTkTextbox(self.tabview.tab("Pressurization"), width=250)
        self.Pressurization_textbox.grid(row=0,rowspan=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        #Launch
        self.Launch_textbox = customtkinter.CTkTextbox(self.tabview.tab("Launch Stage"), width=250)
        self.Launch_textbox.grid(row=0,rowspan=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Left Rocket information
        self.Left_Rocket_frame = customtkinter.CTkFrame(self)
        self.Left_Rocket_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.Left_Rocket_label_group = customtkinter.CTkLabel(master=self.Left_Rocket_frame, text="Left Rocket information")
        self.Left_Rocket_label_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")

        # Right Rocket information
        self.Right_Rocket_frame = customtkinter.CTkFrame(self)
        self.Right_Rocket_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.Right_Rocket_label_group = customtkinter.CTkLabel(master=self.Right_Rocket_frame, text="Right Rocket information")
        self.Right_Rocket_label_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")


        # set default values
        self.scaling_optionemenu.set("100%")
        self.Load_textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def change_state(self, state):
        if (state >= 0 and state < 4):
            self.state_var = state
            if(self.state_var == 0): #Load
                self.load_state_button.configure(state="enabled")
                self.aim_state_button.configure(state="disabled")
                self.pressurize_state_button.configure(state="disabled")
                self.launch_state_button.configure(state="disabled")
            elif(self.state_var == 1): #Aim
                self.load_state_button.configure(state="disabled")
                self.aim_state_button.configure(state="enabled")
                self.pressurize_state_button.configure(state="disabled")
                self.launch_state_button.configure(state="disabled")
            elif(self.state_var == 2): #Pressurize
                self.load_state_button.configure(state="disabled")
                self.aim_state_button.configure(state="disabled")
                self.pressurize_state_button.configure(state="enabled")
                self.launch_state_button.configure(state="disabled")
            elif(self.state_var == 3): #Launch
                self.load_state_button.configure(state="disabled")
                self.aim_state_button.configure(state="disabled")
                self.pressurize_state_button.configure(state="disabled")
                self.launch_state_button.configure(state="enabled")




        

if __name__ == "__main__":
    app = App()
    app.mainloop()
