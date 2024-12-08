from moviepy.editor import VideoFileClip
from moviepy.editor import ImageClip
import pandas as pd

def play_video(video_path, start_time, duration):
    clip = VideoFileClip(video_path)
    
    # Calculate the actual end time (it shouldn't exceed the video duration)
    end_time = start_time + duration
    if end_time > clip.duration:
        print(f"Adjusted duration to fit video length. Playing until {clip.duration} seconds.")
        end_time = clip.duration
        duration = end_time - start_time  # Adjust duration ato fit within the video length

    # Subclip from start_time to the adjusted end_time
    clip = clip.subclip(start_time, end_time)
    print("Playing Video")
    resize_clip = clip.resize(newsize=(1280, 720))
    resize_clip.preview()
    
    return start_time + duration

def play_rest_video(video_path, image_path, duration):

    #Notice the user for resting time
    clip = ImageClip(image_path, duration = 3)
    resize_clip = clip.resize(newsize=(1280, 720))
    resize_clip.preview()
    
    #Playing the resting clip for 5 minutes
    clip = VideoFileClip(video_path).subclip(0, duration)
    resize_clip = clip.resize(newsize=(1280, 720))
    resize_clip.preview()

def determine_video_length(min):
    #Settting the initial length and video incremenet length
    initial_length = 1
    increment_length = 1
    
    #determining the categroy based on last minutes
    if min >= 50:
        initial_length = 3*60
        increment_length = 1*60
        print("hihihih")
    elif min >= 40:
        initial_length = 2*60
        increment_length = .75*60
    else:
        initial_length = 1*60
        increment_length = .5*60
    
    return initial_length, increment_length
    

def main():
    
    csv_file_path = "prediction.csv"
    #retrieving the last minutes from the csv file
    last =  pd.read_csv(csv_file_path).tail(1)
    min = last["Focus Duration (seconds)"].iloc[0]
        

    # Paths to videos
    main_video_path = "VideoSource/your_video.mp4"  
    rest_video_path = "VideoSource/rest.mp4" 
    print(f"Video path: {main_video_path}")
    print(f"Rest video path: {rest_video_path}")
    
    #Paths to images
    rest_image_path = "ImageSource/rest.png"
    print(f"Image path: {rest_image_path}")
    
    # Initialize video durations based on the min variable at line 56
    video_duration, increment = determine_video_length(min)
    print(f"Initial Video Duration: {video_duration}")
    print(f"Increment: {increment}")

    # Initialize start time for the video (start from 0)
    current_time = 0

    try:
        while True:
            # Play the main video starting from `current_time`
            print(f"Playing main video for {video_duration} seconds, starting at {current_time}th seconds...")
            current_time = play_video(main_video_path, current_time, video_duration)

            if current_time >= VideoFileClip(main_video_path).duration:
                print("Video finished. Stopping playback.")
                break

            # Gradually increase the video length
            video_duration += increment
            print(f"Increasing next video duration to {video_duration // 60} minutes.")

            # Play the rest video
            print("Playing rest video...")
            play_rest_video(rest_video_path, rest_image_path, 5)
            

    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
