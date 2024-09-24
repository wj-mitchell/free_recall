"""
free_recall.example
=====================
"""

__author__ = ["Billy Mitchell"]
__license__ = "GNU v3"

import functions
import os
from datetime import datetime
from psychopy import visual

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
    "You may start speaking when this symbol appears.\n\nWhen you have finished, please say 'I'm done' and we will stop recording."
]

# Recording PID and record duration
pid, dur = functions.dialogue_box()
filename = 'recall_' + pid + '_' + today_string + '.wav'
print('file will be saved as: ' + filename)

# Setting the window settings
win = visual.Window(fullscr=True,  
                    winType='pyglet', 
                    allowGUI=True, 
                    allowStencil=False,
                    color=[0,0,0], 
                    colorSpace='rgb',
                    blendMode='avg', 
                    useFBO=True)

for TEXT in instructions:
    functions.text_display(win, text = TEXT, duration = '0')

functions.free_recall(win, 
                     image_size = (win.size[0]/(win.size[1] * 2.5), win.size[1]/win.size[1]),
                     output_file = filename,
                     fixation_duration = 30,
                     record_duration = dur)

functions.show_fixation(duration = '0')
