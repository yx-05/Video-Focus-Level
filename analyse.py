import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing

focus_data=pd.read_csv("focus_intervals.csv")

#Convert time columns to datetime
focus_data['Start Time'] = pd.to_datetime(focus_data['Start Time'])
focus_data['End Time'] = pd.to_datetime(focus_data['End Time'])

recorded_time=10
#Calculate total duration in seconds for each minute
focus_durations = [0] * recorded_time  #Initialize list for 10 minutes
start_time = focus_data['Start Time'].min()  #Start of the recording

# Aggregate durations into minute
for _, row in focus_data.iterrows():
    interval_start = row['Start Time']
    interval_end = row['End Time']
    duration = row['Duration (seconds)']

    #Split the interval in minute boundaries if necessary
    while interval_start < interval_end:
        current_minute = (interval_start - start_time).seconds // 60
        if current_minute >= len(focus_durations):
            focus_durations.extend([0] * (current_minute + 1 - len(focus_durations)))

        next_minute_start = (start_time + timedelta(minutes=current_minute + 1))
        effective_end = min(interval_end, next_minute_start)
        effective_duration = (effective_end - interval_start).total_seconds()

        focus_durations[current_minute] += effective_duration
        interval_start = effective_end

#Normalize focus durations to seconds per minute (convert to proportion of 60 seconds)
focus_durations = [min(60, d) for d in focus_durations]  #Ensure max is 60 seconds per minute
focus_durations = focus_durations[:recorded_time]

#Predict focus duration for the 11th minute

#By mean perspective
predicted_focus_duration1 = np.mean(focus_durations)

#By ARIMA perspective
model1 = ARIMA(focus_durations, order=(1, 1, 1))  # ARIMA model with example order (1, 1, 1)
model_fit1 = model1.fit()
predicted_focus_duration2 = model_fit1.forecast(steps=1)[0]

#By STL perspective
model2 = ExponentialSmoothing(focus_durations, trend="add", seasonal=None, seasonal_periods=None)
model_fit2 = model2.fit()
predicted_focus_duration3 = model_fit2.forecast(steps=1)[0]

#By LSTM perspective
focus_durations_LSTM = np.array(focus_durations).reshape(-1, 1)

#Normalize data
scaler = MinMaxScaler(feature_range=(0, 1))
focus_durations_scaled = scaler.fit_transform(focus_durations_LSTM)

#Prepare the dataset for LSTM
X, y = [], []
for i in range(len(focus_durations_scaled) - 1):  #Use previous steps to predict the next
    X.append(focus_durations_scaled[i])
    y.append(focus_durations_scaled[i + 1])

X, y = np.array(X), np.array(y)
X = X.reshape(X.shape[0], 1, X.shape[1])  #Reshape to [samples, timesteps, features]

#Define the LSTM model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(X.shape[1], X.shape[2])))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

#Train the model
model.fit(X, y, epochs=200, batch_size=1, verbose=0)

#Predict the 11th minute focus duration
last_value = focus_durations_scaled[-1].reshape(1, 1, 1)
predicted_scaled = model.predict(last_value, verbose=0)
predicted_focus_duration4 = scaler.inverse_transform(predicted_scaled)[0, 0]

predicted_focus_duration=min(60,max(0,(predicted_focus_duration1+predicted_focus_duration2+predicted_focus_duration3+predicted_focus_duration3)/4))

#Add the prediction to the data for plotting
minutes = list(range(1, len(focus_durations)+2))  #1st to 11th minute
focus_durations.append(predicted_focus_duration)

#predictive data of all model
print(predicted_focus_duration1)
print(predicted_focus_duration2)
print(predicted_focus_duration3)

#Plot the results
plt.figure(figsize=(10, 6))
plt.plot(minutes, focus_durations, marker='o', label='Focus Duration')
plt.axvline(x=recorded_time+1, color='red', linestyle='--', label='Prediction Point')
plt.text(10.5, predicted_focus_duration, f'Prediction: {predicted_focus_duration:.2f}s', color='blue')
plt.title('Focus Duration vs Time (Minutes)')
plt.xlabel('Time (Minutes)')
plt.ylabel('Focus Duration (Seconds)')
plt.xticks(range(1, 12))
plt.ylim(0, 70)
plt.grid(True)
plt.legend()
plt.show()

#Save the prediction result in a new CSV file
prediction_data = {
    'Minute': minutes, 
    'Focus Duration (seconds)': focus_durations
}
prediction_df = pd.DataFrame(prediction_data)

#Save to CSV
output_file_path = 'prediction.csv'
prediction_df.to_csv(output_file_path, index=False)

#Print the prediction value for the 11th minute
print(f"Predicted focus duration for the 11th minute: {predicted_focus_duration:.2f} seconds")
print(f"The focus durations with prediction have been saved to {output_file_path}")
