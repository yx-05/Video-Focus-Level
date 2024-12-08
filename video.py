from moviepy.editor import VideoFileClip
import pandas as pd

def play_video():
    clip = VideoFileClip("VideoSource/tuto.mp4")
    
    # Calculate the actual end time (it shouldn't exceed the video duration)
    end_time = 5*60
    # Subclip from start_time to the adjusted end_time
    clip = clip.subclip(0, end_time)
    print("Playing Video")
    resize_clip = clip.resize(newsize=(1280, 720))
    resize_clip.preview()

play_video()