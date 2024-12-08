import cv2 as cv
import threading
import numpy as np
import subprocess
import os
import signal

subprocesses = []

# Function to start the gaze tracking
def start_gaze_tracking():
    print("Gaze tracking started.")
    process = subprocess.Popen(["python", "GazeTrack.py"])
    subprocesses.append(process)

# Function to cut video
def cut_video():
    print("Video cutting started.")
    process = subprocess.Popen(["python", "VideoPlayer.py"])
    subprocesses.append(process)

def terminate_all_subprocesses():
    print("Terminating all subprocesses...")
    for process in subprocesses:
        try:
            # Send a SIGTERM signal to terminate the process
            os.kill(process.pid, signal.SIGTERM)
        except Exception as e:
            print(f"Failed to terminate subprocess {process.pid}: {e}")
    subprocesses.clear()

def play_video():
    print("Playing video.")
    process = subprocess.Popen(["python", "video.py"])
    subprocesses.append(process)

def exit_program():
    print("Exiting program.")
    terminate_all_subprocesses()
    cv.destroyAllWindows()
    exit()

# Function to draw a rounded rectangle
def draw_rounded_rectangle(image, top_left, bottom_right, color, thickness, corner_radius):
    x1, y1 = top_left
    x2, y2 = bottom_right

    # Draw filled rectangle for the center
    cv.rectangle(image, (x1 + corner_radius, y1), (x2 - corner_radius, y2), color, thickness)

    # Draw filled rectangle for the sides
    cv.rectangle(image, (x1, y1 + corner_radius), (x2, y2 - corner_radius), color, thickness)

    # Draw circles for corners
    cv.circle(image, (x1 + corner_radius, y1 + corner_radius), corner_radius, color, thickness)
    cv.circle(image, (x2 - corner_radius, y1 + corner_radius), corner_radius, color, thickness)
    cv.circle(image, (x1 + corner_radius, y2 - corner_radius), corner_radius, color, thickness)
    cv.circle(image, (x2 - corner_radius, y2 - corner_radius), corner_radius, color, thickness)

# Function to display the interface
def display_interface():
    # Create a blank image for the interface
    interface = cv.imread("download.png", 1)  # Optional background image
    if interface is None:
        interface = 255 * np.ones((400, 600, 3), dtype=np.uint8)

    # Add interface text
    cv.putText(interface, "GazerTrack Interface", (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 5, cv.LINE_AA)
    cv.putText(interface, "Select an option below:", (100, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 3, cv.LINE_AA)

    # Button coordinates
    start_button_coords = ((100, 150), (250, 200))
    play_video_button_coords = ((100, 220), (250, 270))  # New button coordinates
    cut_video_button_coords = ((100, 290), (250, 340))
    exit_button_coords = ((100, 360), (250, 410))

    # Draw formal buttons with rounded corners
    draw_rounded_rectangle(interface, start_button_coords[0], start_button_coords[1], (0, 255, 0), -1, 10)
    draw_rounded_rectangle(interface, play_video_button_coords[0], play_video_button_coords[1], (0, 0, 255), -1, 10)
    draw_rounded_rectangle(interface, cut_video_button_coords[0], cut_video_button_coords[1], (255, 165, 0), -1, 10)
    draw_rounded_rectangle(interface, exit_button_coords[0], exit_button_coords[1], (0, 0, 255), -1, 10)

    # Add text to buttons
    cv.putText(interface, "Start GazeTrack", (130, 185), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(interface, "Play Video", (110, 255), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv.LINE_AA)  # New button text
    cv.putText(interface, "Cut Video", (115, 325), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(interface, "Exit", (140, 395), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv.LINE_AA)

    # Display the interface
    cv.imshow("GazerTrack Interface", interface)

    while True:
        key = cv.waitKey(1) & 0xFF
        if key == ord("q"):  # Quit when 'q' is pressed
            exit_program()
        else:
            mouse = cv.setMouseCallback("GazerTrack Interface", on_mouse_click, 
                                        [start_button_coords, play_video_button_coords, cut_video_button_coords, exit_button_coords])

# Updated on_mouse_click function
def on_mouse_click(event, x, y, flags, param):
    start_button, play_video_button, cut_video_button, exit_button = param
    if event == cv.EVENT_LBUTTONDOWN:
        if start_button[0][0] < x < start_button[1][0] and start_button[0][1] < y < start_button[1][1]:
            threading.Thread(target=start_gaze_tracking).start()
        elif play_video_button[0][0] < x < play_video_button[1][0] and play_video_button[0][1] < y < play_video_button[1][1]:
            threading.Thread(target=play_video).start()
        elif cut_video_button[0][0] < x < cut_video_button[1][0] and cut_video_button[0][1] < y < cut_video_button[1][1]:
            threading.Thread(target=cut_video).start()
        elif exit_button[0][0] < x < exit_button[1][0] and exit_button[0][1] < y < exit_button[1][1]:
            exit_program()

# Launch the interface
if __name__ == "__main__":
    display_interface()
