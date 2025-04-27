import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from keras.models import Sequential
from keras.layers import LSTM, Dense
import math

def analyze_stock(csv_path, forecast_days=180, lookback=30):
    """Analyze stock and generate graphs."""
    # Load and preprocess
    data = pd.read_csv(csv_path, header=0)
    data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)
    data.sort_values('Date', inplace=True)

    # Scaling
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data[['Close']])

    # Dataset creation
    def create_rnn_dataset(data, lookback):
        x, y = [], []
        for i in range(len(data) - lookback - 1):
            x.append(data[i:(i + lookback), 0])
            y.append(data[i + lookback, 0])
        return np.array(x), np.array(y)

    train_size = int(len(scaled_data) * 0.8)
    train_data = scaled_data[:train_size]
    test_data = scaled_data[train_size - lookback:]

    train_x, train_y = create_rnn_dataset(train_data, lookback)
    test_x, test_y = create_rnn_dataset(test_data, lookback)

    train_x = np.reshape(train_x, (train_x.shape[0], 1, train_x.shape[1]))
    test_x = np.reshape(test_x, (test_x.shape[0], 1, test_x.shape[1]))

    # LSTM model
    model = Sequential()
    model.add(LSTM(256, input_shape=(1, lookback)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])
    model.fit(train_x, train_y, epochs=20, batch_size=16, verbose=1)

    # Predictions
    train_pred = scaler.inverse_transform(model.predict(train_x))
    test_pred = scaler.inverse_transform(model.predict(test_x))

    # Forecast
    current_input = test_x[-1, :].flatten()
    predictions_future = []

    for _ in range(forecast_days):
        input_data = current_input[-lookback:].reshape((1, 1, lookback))
        prediction = model.predict(input_data)
        predictions_future.append(prediction[0, 0])
        current_input = np.append(current_input, prediction[0, 0])

    predictions_future = np.array(predictions_future).reshape(-1, 1)
    predictions_future = scaler.inverse_transform(predictions_future)

    future_dates = pd.date_range(start=data['Date'].iloc[-1], periods=forecast_days+1, freq='D')[1:]

    # --- GRAPH 1: Stock Prices Over Time ---
    fig1 = px.line(data, x='Date', y='Close', title='Stock Prices Over Time', template='plotly_dark')
    fig1.update_traces(line=dict(color="#4CAF50"))

    # --- GRAPH 2: Forecast ---
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Actual', line=dict(color="#4CAF50")))
    fig2.add_trace(go.Scatter(x=data['Date'][lookback:lookback + len(train_pred)], y=train_pred.flatten(), mode='lines', name='Train', line=dict(color="#FF5722")))
    fig2.add_trace(go.Scatter(x=data['Date'][train_size:train_size + len(test_pred)], y=test_pred.flatten(), mode='lines', name='Test', line=dict(color="#2196F3")))
    fig2.add_trace(go.Scatter(x=future_dates, y=predictions_future.flatten(), mode='lines', name='Forecast', line=dict(color="#FFC107")))
    fig2.update_layout(title='Stock Price Forecast', template='plotly_dark')

    # --- GRAPH 3: Moving Averages Comparison ---
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close Price', line=dict(color="#4CAF50")))
    fig3.add_trace(go.Scatter(x=data['Date'], y=data['SMA_50'], mode='lines', name='50-Day SMA', line=dict(color="#FF5722")))
    fig3.add_trace(go.Scatter(x=data['Date'], y=data['SMA_200'], mode='lines', name='200-Day SMA', line=dict(color="#2196F3")))
    fig3.update_layout(title='Moving Averages Comparison', template='plotly_dark')

    # --- GRAPH 4: Volatility Over Time ---
    data['Returns'] = data['Close'].pct_change()
    data['Volatility_30'] = data['Returns'].rolling(window=30).std()
    fig4 = px.line(data, x='Date', y='Volatility_30', title='Volatility Over Time', template='plotly_dark')
    fig4.update_traces(line=dict(color="#FFC107"))

    # --- GRAPH 5: Returns Distribution ---
    fig5 = px.histogram(data, x='Returns', nbins=50, title='Returns Distribution', template='plotly_dark')
    fig5.update_traces(marker=dict(color="#4CAF50"))

    # Model Evaluation Metrics
    mae = mean_absolute_error(test_y, test_pred)
    rmse = math.sqrt(mean_squared_error(test_y, test_pred))
    r2 = r2_score(test_y, test_pred)

    # Decision Logic
    mean_volatility = data['Volatility_30'].mean()
    trend = "Bullish" if data['SMA_50'].iloc[-1] > data['SMA_200'].iloc[-1] else "Bearish"
    risk = "Low Risk" if data['Volatility_30'].iloc[-1] < mean_volatility else "High Risk"

    first_30_avg = np.mean(predictions_future[:30])
    last_30_avg = np.mean(predictions_future[-30:])
    forecast_trend = "Upward" if last_30_avg > first_30_avg else "Downward"

    current_price = data['Close'].iloc[-1]
    last_predicted_price = predictions_future[-1, 0]
    price_gain = (last_predicted_price - current_price) / current_price * 100

    if trend == "Bullish" and risk == "Low Risk" and forecast_trend == "Upward" and price_gain >= 5:
        decision_message = "✅ This stock is likely a good investment (Bullish trend, Low risk, upward forecast)."
    else:
        decision_message = "⚠️ Investment not recommended based on current trend, risk, or forecast reliability."

    # Return graphs and evaluation metrics
    return fig1, fig2, fig3, fig4, fig5, decision_message, mae, rmse, r2