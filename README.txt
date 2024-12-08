STEPS
1.To launch this program, please press on interface.exe
2.OPTIONAL:Press button "Play Video" to watch an example 10 minutes video while recording user's focus for the next step.
3.Press button "Start" to run gaze tracker for 10 minutes as to predict user's focus interval in the next minute
4.Press button "Cut Video" to watch video that cut into clips according to focus time of each user
5."Exit" button to close all running program(plotted predicted user's focus interval is not terminated when "Exit" pressed.
*When playing "cut video", user can take a break of 5 seconds by pressing "x-exit" button at top right corner of video

MODIFICATION
1.User should save their video to be cut into clips in VideoSource file with name "your_video.mp4"
2.User can modify video playing while waiting extraction of user's focus interval in the 10 minutes by saving favoured video into VideoSource/ with name "tuto.mp4"

DETAILS:
Video Cutter details:
If user can focus 50 seconds and above per minute, video is played for 3 minutes with increment of 1 minute to the next clip.
If user can focus 40 seconds to 49 seconds per minute, video is played for 2 minutes with increment of 45 seconds to the next clip.
If user can focus less than 40 seconds per minute, video is played for 1 minutes with increment of 30 seconds to the next clip.

Focus interval result is being recorded in focus_intervals.csv
Analyse processed result is being recorded in prediction.csv

Time Series AI Model Applied:
Time Series Analysis being applied into this program: prediction=Min(Max(0,(mean+ARIMA+ETS+LSTM)/4),60)
ARIMA=Autoregressive Integrated Moving Average model
ETS=Exponential Smoothing State Space model
LSTM=Long Short Term Memory
With LTSM improve stability of model, ETS responsible to smooth and reduce focus time, ARIMA responsible in increasing focus time in their own feature aspect that they extract
While using mean to maintain prediction to normal level
Min max to ensure interval not exceed 60 second or less than 0 second in a minute

