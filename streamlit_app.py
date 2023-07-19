import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def load_data(tickers):
    # Fetch data on the specified tickers
    data = yf.download(tickers, start='2018-02-01')
    return data

# Load data
data_googl = load_data('GOOGL')
data_indices = load_data(['^IXIC', '^DJI', '^GSPC'])

# Assuming ensemble_df is loaded from a CSV file
ensemble_df = pd.read_csv('C:/Users/arobe/Documents/ensemble_df.csv')
ensemble_df = ensemble_df.rename(columns={'Ensemble_Predictions': 'Close'})
ensemble_df['Date'] = pd.to_datetime(ensemble_df['Date'])

# Plot the data
st.title('Google Stock Price & Prediction')

# Slider to select the last N days to display
days_to_display = st.slider('Days to display', min_value=1, max_value=len(data_googl), value=len(data_googl))

# Truncate data to the last N days
data_googl_displayed = data_googl.iloc[-days_to_display:]
data_indices_displayed = data_indices['Close'].iloc[-days_to_display:]

st.write(f'Displaying the "Open" and "Close" prices for Google for the last {days_to_display} days.')

# Plot Google data
trace1 = go.Scatter(
    x=data_googl_displayed.index,
    y=data_googl_displayed['Open'],
    mode='lines',
    name='GOOGL Open'
)
trace2 = go.Scatter(
    x=data_googl_displayed.index,
    y=data_googl_displayed['Close'],
    mode='lines',
    name='GOOGL Close'
)
data = [trace1, trace2]
layout = go.Layout(
    title='Google Stock Price',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Stock Price'),
)
fig = go.Figure(data=data, layout=layout)
st.plotly_chart(fig)

# Display raw data (most recent first)
st.write('Displaying raw data.')
st.dataframe(data_googl.sort_index(ascending=False))

st.write(f'Displaying the "Close" prices for NASDAQ, DOW, and S&P 500 for the last {days_to_display} days.')

# Plot index data
trace1 = go.Scatter(
    x=data_indices_displayed.index,
    y=data_indices_displayed['^IXIC'],
    mode='lines',
    name='NASDAQ',
    hovertemplate='Date: %{x}<br>NASDAQ: %{y:,.0f}<extra></extra>'
)
trace2 = go.Scatter(
    x=data_indices_displayed.index,
    y=data_indices_displayed['^DJI'],
    mode='lines',
    name='DOW',
    hovertemplate='Date: %{x}<br>DOW: %{y:,.0f}<extra></extra>'
)
trace3 = go.Scatter(
    x=data_indices_displayed.index,
    y=data_indices_displayed['^GSPC'],
    mode='lines',
    name='S&P 500',
    hovertemplate='Date: %{x}<br>S&P 500: %{y:,.0f}<extra></extra>'
)
data = [trace1, trace2, trace3]
layout = go.Layout(
    title='Index Prices',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Index Price'),
)
fig = go.Figure(data=data, layout=layout)
st.plotly_chart(fig)


# Create a new graph for ensemble predictions
st.title('Google Stock Price Predictions')

# Create two traces for the 'Ensemble Prediction' before and after the date
mask = ensemble_df['Date'] >= pd.to_datetime('2023-07-18')
trace1 = go.Scatter(
    x=ensemble_df.loc[~mask, 'Date'],
    y=ensemble_df.loc[~mask, 'Close'],
    mode='lines',
    name='Hisotrical Google Data',
    line=dict(color='blue')
)
trace2 = go.Scatter(
    x=ensemble_df.loc[mask, 'Date'],
    y=ensemble_df.loc[mask, 'Close'],
    mode='lines',
    name='Google Stock Prediction',
    line=dict(color='red')
)
data = [trace1, trace2]
layout = go.Layout(
    xaxis=dict(title='Date'),
    yaxis=dict(title='Stock Price'),
)
fig = go.Figure(data=data, layout=layout)
st.plotly_chart(fig)
