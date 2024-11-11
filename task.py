"""
free_recall.example
=====================
"""

__author__ = ["Billy Mitchell"]
__license__ = "GNU v3"

import functions
import os
from datetime import datetime
from psychopy import visual, core, event 

# Set the directory to where the script is located (or any other desired directory)
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory where the script is located
os.chdir(script_dir)  # Change the current working directory to the script directory
print(f"Current working directory: {os.getcwd()}")  # Print the current working directory

# Get today's date
today_date = datetime.today()

# Convert to string in the format YYYY-MM-DD
today_string = today_date.strftime('%Y-%m-%d')

# Denoting the instructions
instructions = [
    "For this scan, please describe everything you can remember from the episode in as much detail as possible.\n\nInclude everything you can remember, even if you don't think it's important.", 
    "Try to remember the events in chronological order, but if at any point you realize you missed something, go back and describe it.",
    "Please speak for at least 10 minutes if you can, but even longer is better. We cannot display a timer for this task.\n\nRemember to try to stay as still as you can as you talk.",
    "A bar on the right side of the screen will give you feedback as to how loud you are talking. Please try to speak loud enough so that the bar reaches the red target lines.",    
    "You may start speaking when this symbol appears.\n\nWhen you have finished, please say 'I'm done' and we will stop recording.",
    "Before the next task begins, we will run a very quick scan. You will see a fixation cross appear on the screen. Please just relax while this scan runs."
]

# Recording PID and record duration
pid, dur, save_local = functions.dialogue_box()

# Checking if directories exist
target_dir = 'S:/Helion_Group/studies/Dynamic_Decisions/Data/Audio'
filename = 'Recall_' + pid + '_' + today_string + '.wav'
if os.path.exists(target_dir) and save_local is False:
    filepath = target_dir + "/" + filename 
else:
    filepath = filename
    
# Printing save location to the terminal
print('file will be saved as: ' + filepath)

# Setting the window settings
win = visual.Window(fullscr=True,  
                    winType='pyglet', 
                    allowGUI=True, 
                    allowStencil=False,
                    color=[0,0,0], 
                    colorSpace='rgb',
                    blendMode='avg', 
                    useFBO=True)

tracker = 0
for TEXT in instructions: 
    tracker += 1   
    # Display instructions
    if tracker != len(instructions) - 1:
        functions.text_display(win, text=TEXT, duration='0')
    else:
        functions.text_display(win, text=TEXT, image_path='record.png', duration='0')

# Show fixation cross
functions.show_fixation(win, duration='0')

# Start the free recall task
functions.free_recall(win, 
                     image_size=(win.size[0]/(win.size[1] * 2.5), win.size[1]/win.size[1]),
                     output_file=filepath,
                     fixation_duration=30,
                     record_duration=dur)

# Show fixation cross
functions.show_fixation(win, duration='0')

# Check for 'Esc' key before closing the window
functions.check_for_escape(win)

# Close the PsychoPy window
win.close()

# Stop the PsychoPy core and exit
core.quit()
