"""
free_recall.functions
=====================
"""

__author__ = ["Billy Mitchell"]
__license__ = "GNU v3"

import os
import time
import sounddevice as sd
import numpy as np
from psychopy import visual, gui, core, event, prefs
from psychopy.hardware import keyboard
prefs.hardware['audioLib'] = ['PTB']
from psychopy import sound  # Import sound after setting preferences
from scipy.io import wavfile
import datetime

# ----- CHECK FOR ESCAPE -----
def check_for_escape(win):
    """
    check_for_escape waits for escape to be pressed and then closes the task. 
    
    Args:

    Returns:
    """
    if 'escape' in event.getKeys():
        win.close()
        core.quit()

# ----- DIALOGUE BOX -----
def dialogue_box():
    
    """
    dialogue_box presents a dialogue box in which to enter subject ID or modify the recording duration. 
    
    Args:

    Returns:
        subject ID: string
        duration: integer
    """
    
    subjDlg = gui.Dlg(title='free_recall') # Denoting the task title
    subjDlg.addField('Enter Subject ID: ', 'DD-')  # Denoting the Subject ID
    subjDlg.addField('Duration (s):', 1200) # Denoting maximum recording time
    subjDlg.addField('Save Local:', initial= True) # Whether to save locally
    subjDlg.show() # Present the GUI
    if subjDlg.OK == False:
        core.quit()

    return subjDlg.data[0], subjDlg.data[1], subjDlg.data[2]

# ----- KEY_OR_TIME ----
def key_or_time(win, duration, keyboard):

    """
    key_or_time simplifies the mechanism which determines when many task functions should end. It accepts either a key string or an integer and filters and changes how the task progresses depending upon the duration type. 
    
    Args:
        duration: Either an integer or the name of a key; for how long or until what 
        text: a PsychoPy.visual.TextStim() object
        keyboard: a PsychoPy.hardware.keyboard.keyboard() object

    Returns:

    """
        # If duration is an integer ...
    if isinstance(duration, int) or isinstance(duration, float):
        
        # Wait out the duration 
        start_time = time.time()

        while time.time() - start_time < duration:
        
            # If escape is pressed 
            if keyboard.getKeys(keyList=["escape"]):
                
                # End the experiment
                core.quit()

    # If duration is a string ...
    elif isinstance(duration, str):

        # Set a variable to track key presses
        key_pressed = False
        response = {'keys': None, 'rt': None}

        # ... and while that variable is false
        while not key_pressed:

            # Save any key presses that do occur
            keys = keyboard.getKeys(keyList=[duration])

            # If key presses have been registered
            if keys:

                # Change that tracking variable to true
                key_pressed = True

                # Save which keys were pressed
                response['keys'] = keys[-1].name

                # Save the response time of key presses
                response['rt'] = keys[-1].rt

            # However, if the escape key is pressed
            elif keyboard.getKeys(keyList=["escape"]):

                # End the experiment
                core.quit()

            # Otherwise ...
            else:

                # Flip the window
                win.flip()

        return response

# ----- TEXT_DISPLAY -----
def text_display(win, text, duration, image_path=None, text_color = 'white', text_height = 0.11, wrap_width = 1.45):

    """
    text_display draws text on the window. If duration is an integer, it will appear for a number of seconds equal to that integer. If duration is the name of a recognized key, the fixation will appear until that key is pressed 
    
    Args:
        win: Defining the window to use
        text: The text that you'd like to appear in your instructions
        duration: Either an integer or the name of a key; for how long or until what condition is met should the fixation be apparent 
        image_path: Path to the image file (.png) to display below the text (optional)
        text_color: The color of the fixation
        text_height: The height of the fixation cross
        wrap_width: How long before text should break and wrap to the next line
    Returns:

    """
    
    # Notes on Future Improvements:
    # + Add QAs and warnings

    # Start the clock
    ts_start = datetime.datetime.now()

    # Define our text object
    text = visual.TextStim(win=win, text=text, pos=[0,0], height=text_height, wrapWidth=wrap_width, color=text_color, autoDraw = True)
    
    # If an image path is provided, define an ImageStim object
    if image_path is not None:
        image_stim = visual.ImageStim(win=win, image=image_path, pos=[0, -0.6], size = [0.4, 0.65])
        image_stim.autoDraw = True
    else:
        image_stim = None

    # Flipping the window
    win.flip()

    # Initializing keyboard
    kb = keyboard.Keyboard()

    # If duration is an integer ...
    if isinstance(duration, int) or isinstance(duration, float):
        
        # Custom utility function to progress the event
        key_or_time(win = win, duration = duration, keyboard = kb)
    
    # If duration is a string ...
    elif isinstance(duration, str):
        
        # Custom utility function to progress the event
        response = key_or_time(win = win, duration = duration, keyboard = kb)

    # Stop drawing the text
    text.setAutoDraw(False)
    if image_stim is not None:
        image_stim.setAutoDraw(False)

    # Flip the window
    win.flip()
    
    # Check for escape key after each instruction display
    check_for_escape(win)

    # Stop the clock
    ts_end = datetime.datetime.now()

# ----- SHOW_FIXATION -----
def show_fixation(win, duration = 30, text_color = 'white', text_height = 0.2):
    """
    show_fixation shows a fixation cross in the center of the screen for a number of seconds equal to duration.
    
    Required Args:
        win: Defining the window to use
        duration: The amount of time in seconds to show the fixation

    """

    # Notes on Future Improvements:
    

     # Define our text object
    fixation = visual.TextStim(win=win, text='+', pos=[0,0], height=text_height, color=text_color, autoDraw = True)

    # Flipping the window
    win.flip()
        
    # Initializing keyboard
    kb = keyboard.Keyboard()

    # If duration is an integer ...
    if isinstance(duration, int) or isinstance(duration, float):
        
        # Custom utility function to progress the event
        key_or_time(win = win, duration = duration, keyboard = kb)
    
    # If duration is a string ...
    elif isinstance(duration, str):
        
        # Custom utility function to progress the event
        response = key_or_time(win = win, duration = duration, keyboard = kb)

    # Stop drawing the text
    fixation.setAutoDraw(False)

    # Clear after continue condition is met
    win.flip()

    # Check for escape key after each instruction display
    check_for_escape(win)

# ----- FREE RECALL -----
def free_recall(win, device_info = sd.query_devices(None, 'input'), sample_rate = 'default_samplerate', output_file = 'recording.wav', image='record.png', image_size = (300,300), show_volume = True, target_volume = 50, volume_sensitivity = 50, volume_color = 'darkblue', trigger_text = "Waiting for scanner...", trigger_key = 'equal', fixation_duration = 0,  end_key = '0', record_duration = 0): 

    """
    free_recall is a modular task component which, upon receiving a trigger key, begins recording audio from the default microphone of the computer running it. It draws a live volume tracker to the right of the target image to give participants feedback regarding their speaking voices. It will record indefinitely until the end key is pressed. Once completed, it will generate a .wav formatted output file.
    
    Required Args:
        win: Defining the window to use
        device_info: A sounddevice object containing information regarding which microphone to use; will use the default microphone if not specified
        sample_rate: A string referring to the sample rate of the microphone
        output_file: Defining the name of the file that should be output to the current working directory
        image: Defining which image to draw in the center of the window while free recall is being recorded
        image_size: A list of two values representing the height and width of the image
        show_volume: Boolean value; if false, no volume tracker will be shown
        target_volume: Accepts integers between 0 and 100; draws a horizontal red bar on tracker to highlight the volume above which participants should aim to speak 
        volume_sensitivity: Defining how sensitive the volume bar should be; larger numbers are less sensitive
        volume_color: Defining the color of the volume bar; accepts the standard fillColor options that PsychoPy visual objects do
        trigger_text: A string that appears before the task begins
        trigger_key: The key that will start the process
        fixation_duration: The amount of time in seconds to show a fixation cross after the trigger and before the recording starts; to turn off, set to 0. 
        end_key: The key that will end the process
        record_duration: The amount of time in seconds to capture in the recording; to record indefinitely, set to 0. 

    Returns:
        data: (np.dataframe) data regarding this task
        recording: (.wav or .mp3 file) an audio recording of what was said

    """

    # Notes on Future Improvements:
    # + Add an agrument and code to write data (using update_log)
    # + Recode a return value
    # + Add warnings and QAs to the code 
    # + Add option to change the dimensions of the image
    # + Get .mp3 conversion to work (output_format = "wav") output_format: The format of the output audio file ('.wav' or '.mp3'). 

    # Set the directory to where the script is located (or any other desired directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory where the script is located
    os.chdir(script_dir)  # Change the current working directory to the script directory
    print(f"Current working directory: {os.getcwd()}")  # Print the current working directory
    # print(f"Current device information: {device_info.name}")

    # Capturing the time
    ts_start = datetime.datetime.now()

    # Initialize shared variables
    recording_started = False
    recording_triggered = False
    
    # Create a text stimulus for the waiting message
    waiting_text = visual.TextStim(win, text = trigger_text, pos=(0, 0), height=0.1)

    # Set up the microphone
    samplerate = int(device_info[sample_rate])

    # If we want the volume tracker visualized
    if show_volume:
        
        # Initializing volume variable
        volume_norm = [0]

        # Position the volume bar to the right
        volume_bar = visual.Rect(win, width=0.15, height=0.5, fillColor=volume_color, pos=(0.8, 0))
        volume_tray = visual.Rect(win, width=0.18, height=1.5, fillColor='lightgrey', lineColor = 'black', lineWidth=10, pos=(0.8, 0)) 
        volume_target_high = visual.Rect(win, width=0.18, height=0.01, fillColor='red', pos=(0.8, target_volume * 0.0075))
        volume_target_low = visual.Rect(win, width=0.18, height=0.01, fillColor='red', pos=(0.8, -(target_volume * 0.0075)))
    
    # Modify the audio_callback function to update the first element of the list
    def audio_callback(indata, frames, time, status):
        if recording_started:
            volume_norm[0] = np.linalg.norm(indata) * 10
            output_data.extend(indata.copy())
    
    # Load and position the image in the center of the screen
    record_image = visual.ImageStim(win, image=image, pos=(0, 0), 
                                    size = image_size)

    # Prepare to record
    output_data = []

    # Start the audio stream
    stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=samplerate)
    stream.start()

    try:
        
        # Check for escape key after each instruction display
        check_for_escape(win)

        while True:
            keys = event.getKeys()

            if not recording_triggered and trigger_key in keys:
                if fixation_duration > 0: 
                    show_fixation(win, fixation_duration) # Show fixation
                recording_triggered = True  # Set the flag to indicate that recording has been triggered
            
            if recording_triggered:
                recording_started = True  # Start recording once triggered
                record_image.draw()  # Draw the image
                
                # If we want the volume tracker visualized
                if show_volume:
                    volume_bar.height = volume_norm[0] / volume_sensitivity  # Update the visual element with the latest volume level
                    volume_tray.draw()  # Draw the volume tray
                    volume_bar.draw()  # Draw the volume bar
                     
                    # If we entered a value for the target volume
                    if target_volume > 0: 
                        volume_target_high.draw() # Draw the target volume upper limit
                        volume_target_low.draw() # Draw the target volume lower limit
                
                if end_key in keys or datetime.datetime.now() - ts_start >= datetime.timedelta(seconds=record_duration):     
                    recording_started = False
                    break

            else:
                waiting_text.draw()  # Draw the waiting text

            win.flip()

    finally:
        stream.stop()
        
        # Check if there is any recorded data
        if len(output_data) > 0:  
            output_nparray = np.concatenate(output_data, axis=0).astype('float32')
            wavfile_path = os.path.join(script_dir, output_file)  # Ensure the path is where the script is
            wavfile.write(wavfile_path, samplerate, output_nparray)  # Save the recording to a WAV file
            print(f"Recording saved to: {wavfile_path}")  # Print the path to the saved recording
            
            # # If we want the file in .mp3 format
            # if output_format == 'mp3':
            #     mp3file_path = os.path.join(script_dir, f"{output_filename}.mp3")
            #     wav_to_mp3(input = wavfile_path, output = mp3file_path)
            #     print(f"Recording converted to: {mp3file_path}")
            #     os.remove(wavfile_path)
        
        else:
            print("No data was recorded.")