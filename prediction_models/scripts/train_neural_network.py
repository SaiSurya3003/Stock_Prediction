import numpy as np
import pandas as pd
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler

# Directory containing the stock data
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
# Directory to save the trained models
model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'neural_networks')
os.makedirs(model_dir, exist_ok=True)

def create_dataset(data, look_back=100):
    X, Y = [], []  # X,Y -> input{prev 100 days}, output{stock price of 101st day}
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back), 0])
        Y.append(data[i + look_back, 0])
    return np.array(X), np.array(Y)

for file in os.listdir(data_dir):
    if file.endswith('.csv'):
        symbol = file.split('.')[0]
        print(f"Processing file for Stock {symbol}")
        data = pd.read_csv(os.path.join(data_dir, file))

    if data.empty:
        print(f"No data available for {symbol}")
        continue

    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    data.dropna(inplace=True)

    if data.empty or len(data) < 100:
        print(f"Insufficient Data for {symbol}")
        continue

    data["MA100"] = data['Close'].rolling(100).mean()
    data["MA200"] = data['Close'].rolling(200).mean()

    train_size = int(len(data)*0.8)
    train_data = data[:train_size]
    test_data = data[train_size]
    if train_data.empty or test_data.empty:
        print("Insufficient data for Processing")
        continue

    scaler = MinMaxScaler(feature_range=(0,1))
    train_scaled = scaler.fit_transform(train_data['Close'])
    test_scaled = scaler.fit_transform(test_data['Close'])

    x_train, y_train = create_dataset(train_scaled)
    x_test, y_test = create_dataset(test_scaled)

    if x_train.size == 0 or y_train.size == 0:
        print("Skipping")
        continue

        # Train the neural network model
        model = Sequential()
        model.add(Dense(100, activation='relu', input_shape=(x_train.shape[1],)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        model.fit(x_train, y_train, epochs=10, batch_size=32, verbose=0)

        # Save the trained model
        model.save(f'{model_dir}/{symbol}_nn.keras')
        print(f'Model for {symbol} saved as {symbol}_nn.keras')