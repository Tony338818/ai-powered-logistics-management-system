import numpy as np
import pandas as pd
from tensorflow.keras import models
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# Load the data
data = pd.read_csv(r"C:\Users\Dell\Downloads\delivery time prediction dataset\Food_Delivery_Times.csv",
                   encoding='ISO-8859-1')

# Drop Order_ID as it's not useful for training
data = data.drop(columns=['Order_ID'])

data = data.dropna()


# Preprocess categorical features with LabelEncoder
Le = LabelEncoder()
data['Weather'] = Le.fit_transform(data['Weather'])
data['Traffic_Level'] = Le.fit_transform(data['Traffic_Level'])
data['Time_of_Day'] = Le.fit_transform(data['Time_of_Day'])
data['Vehicle_Type'] = Le.fit_transform(data['Vehicle_Type'])

# Feature scaling for numerical columns
scaler = StandardScaler()
numerical_columns = ['Distance_km', 'Preparation_Time_min', 'Courier_Experience_yrs']  # numerical columns
data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

# Splitting the data into features (X) and target (y)
X = data.drop('Delivery_Time_min', axis=1)
y = data['Delivery_Time_min']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Reshape the data for LSTM (batch_size, timesteps, features)
timesteps = 1  # Since we don't have sequential data, use 1 timestep
X_train = np.reshape(X_train.values, (X_train.shape[0], timesteps, X_train.shape[1]))
X_test = np.reshape(X_test.values, (X_test.shape[0], timesteps, X_test.shape[1]))

# Building the LSTM model
model = models.Sequential([
    LSTM(units=120, return_sequences=True, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])),
    Dropout(0.2),
    Dense(1)  # Output layer
])

# Compiling the model
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

# Training the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the model
loss = model.evaluate(X_test, y_test)
print(f"Mean Squared Error: {loss}")
