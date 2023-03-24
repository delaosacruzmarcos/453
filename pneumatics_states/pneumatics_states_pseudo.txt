# CSE-453: Rocket Launcher
# Pneumatics state patterns pseudocode

# Boolean Flags for setting current state pattern;
# set either via GPIO or other parts of the program
ROCKET_A = True/False # connected to a switch that can be disabled at any time for safety
ROCKET_B = True/False # ^^^
LOADING = 0
PRESSURIZATION = 0
LAUNCH_STATE = 0
LAUNCH_WAITING = 1 # changes when launch button pressed

# GPIO INPUTS
PRESSURE  # Pressure sensor reading
PRESSURE_TARGET
LAUCH_GO # launch button

# Solenoid Control Signals (will be set to GPIO OUTPUTS)
# All solenoids are normally-open, so setting these to
# zero will open them, one will close them.
SOLENOID_A = 0 # solenoid for rocket A
SOLENOID_B = 0 # solenoid for rocket B
SOLENOID_P = 0 # solenoid for controlling system pressure
LATCH_A    = 0 # solenoid for latching rocket A to the base
LATCH_B    = 0 # solenoid for latching rocket B to the base
COMPRESSOR = 0 # compressor on (1) and off (0) control signal

# All Solenoids are Normally-Open, which here means they are
# physically open to the atmosphere, i.e. system won't pressurize

# NOTE: ALL CODE IS INTENDED TO BE IMPLEMENTED INSIDE AN
#       INFINITE SUPER-LOOP OR SEPARATE THREAD; SOME VARIABLES
#       WILL NEED TO BE SHARED WITH OTHER THREADS OR PARTS OF
#       THE CONTROL PROGRAMS


# This code handles all possible state patterns:
# 1) Launching Rocket A only
# 2) Launching Rocket B only
# 3) Launching A & B together
# The whole procedure is divided into 3 primary stages:
# 1) Loading, 2) Pressurization, and 3) Launch
# The entire process is divided into 10 stages, per the original states
# described in the presentation. Each stage is labelled in the code

# LOADING STAGE
while LOADING and not PRESSURIZATION and not LAUNCH_STATE:
    # Stages correspond to Stage numbering from Final Presentation

    # Stage 0: ensure that system is safe
    SOLENOID_A = SOLENOID_B = SOLENOID_P = 0

    # Stage 1: Close off rockets for loading
    SOLENOID_A = SOLENOID_B = 1
    Sleep(1) # sleep 1 second to give things time to set

    # Stage 2: Latch rocket to base
    if ROCKET_A or ROCKET_B:
        if ROCKET_A:
            LATCH_A = 1
        if ROCKET_B:
            LATCH_B = 1
    else:
        Abort() # should never get here unless there is an error
    Sleep(1)

    # Stage 3: Open solenoid value to rocket
    if ROCKET_A or ROCKET_B:
        if ROCKET_A:
            SOLENOID_A = 0
        if ROCKET_B:
            SOLENOID_B = 0
    else:
        Abort() # should only hit this if there is an error
    Sleep(1)

    # READY TO MOVE FROM LOADING TO PRESSURIZATION STATE
    LOADING = 0
    PRESSURIZATION = 1

# PRESSURIZATION STAGE
while PRESSURIZATION and not LAUNCH_STATE and not LOADING:
    # Stage 4: Prepare system for pressurization
    SOLENOID_P = 1
    Sleep(1)

    # Stage 5 & 6: Pressurize System
    PREV_PRESSURE = PRESSURE
    COMPRESSOR = 1
    while PRESSURIZATION and PRESSURE < PRESSURE_TARGET:
        if PREV_PRESSURE > PRESSURE:
            PRESSURIZATION = 0 # unset for safety?
            HANDLE_LEAK() # paceholder; function could just open all solenoids or w/e
            Abort()
        Sleep(0.5) # sleep briefly to avoid consuming too much CPU
    
    COMPRESSOR = 0 # if we break out of loop w/o error, we should be @ pressure

    # Stage 7: Seal off pressurized rockets
    if ROCKET_A or ROCKET_B:
        if ROCKET_A:
            SOLENOID_A = 1
        if ROCKET_B:
            SOLENOID_B = 1
    else:
        Abort()
    Sleep(1)

    # Stage 8: Vent system (except rocket to be launched)
    SOLENOID_P = 0
    PRESSURIZATION = LOADING = 0
    LAUNCH_STATE = 1

while LAUNCH_STATE and not PRESSURIZATION and not LOADING: # extra carefule guard statement
    countdown = 10
    while LAUNCH_WAITING:
        Sleep(0.1) # brief nap while waiting for someone to hit the launch button

    # Stage 9: Launch initiated
    Sleep(countdown)
    if ROCKET_A or ROCKET_B:
        if ROCKET_A and ROCKET_B:
            LATCH_A = LATCH_B = 0
        else if ROCKET_A:
            LATCH_A = 0
        else if ROCKET_B:
            LATCH_B = 0
    else:
        Abort()
    Sleep(1)

    # NOTE: Current code cannot pressurize BOTH rockets AND THEN launch each
    #       individually. If that functionality is desired, then stage 9 code
    #       needs to be modified to not siply go directly to stage 10 after
    #       launch, but instead wait and monitor state. The reason I excluded
    #       this functionality is safety, so they don't have a pressurized
    #       rocket just sitting there; plus launch of one rocket could shake
    #       the platform and potentially dislodge the second pressurized rocket
    #       While unlikely, it is proabaly undesirable to risk an accidental
    #       launch of the secodn rocket?

    # Stage 10: Launch complete, reset everything to safe
    SOLENOID_A = SOLENOID_B = SOLENOID_P = 0
    LATCH_A = LATCH_B = 0
    LAUNCH_STATE = PRESSURIZATION = LOADING = 0

# SAFETY STATE: code falls back to this loop if nothing is happening
# so other parts of the code/ system can do other things
while not LOADING and not PRESSURIZATION and not LAUNCH_STATE:
    Sleep(1) # just wait