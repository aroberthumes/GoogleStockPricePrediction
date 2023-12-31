from operator import index
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.preprocessing.sequence import TimeseriesGenerator
from keras_tuner import RandomSearch
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import nltk
nltk.download('vader_lexicon')
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from urllib.request import urlopen, Request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from xgboost import XGBRegressor
import os

# Get the current date
current_date = datetime.today()
end_date = current_date

# Format the end_date in 'YYYY-MM-DD' format
end_date_str = end_date.strftime('%Y-%m-%d')

# Get Google stock data
data = yf.download('GOOGL', start='2013-07-14', end=end_date_str)

# Reset index to make 'Date' a column
data.reset_index(inplace=True)

# Rename the columns to match the existing script
df = data.rename(columns={"Date": "Date", "Close": "Price"})

# We'll normalize the 'Price' column
scaler = MinMaxScaler()
df['Price'] = scaler.fit_transform(np.array(df['Price']).reshape(-1,1))

# Define the lookback period and split point for train and test data
lookback = 60  # assuming data is in daily frequency
split_point = int(len(df) * 0.8)

# Create training and test data
train = df['Price'].iloc[:split_point]
test = df['Price'].iloc[split_point:]

# Generate time series for training and test data
train_data_generator = TimeseriesGenerator(train, train, length=lookback, batch_size=20)
test_data_generator = TimeseriesGenerator(df['Price'], df['Price'], length=lookback, batch_size=1, start_index=split_point)

# Defining the optimal number of units as determined by hyperparameter tuning
optimal_units = 480

def build_optimized_model():
    model = Sequential()
    model.add(LSTM(units=optimal_units, activation='relu', return_sequences=True, input_shape=(lookback, 1)))
    model.add(LSTM(units=optimal_units, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

# Build the model with the optimal hyperparameters
model = build_optimized_model()

model.fit(train_data_generator, epochs=10)

# Predict the next 365 days
x_input = np.array(test[-lookback:]).reshape((1, lookback, 1))

future_forecast = []

for i in range(365):  # for the next 365 days
    yhat = model.predict(x_input, verbose=0)
    future_forecast.append(yhat[0])

    # append the prediction into x_input and drop the first value
    x_input = np.append(x_input[0][1:], [yhat])
    x_input = x_input.reshape((1, lookback, 1))

# Invert the scaling of predictions
future_forecast = scaler.inverse_transform(np.array(future_forecast).reshape(-1,1))

# Prepare the dataframe for the next 365 days prediction
future_dates = pd.date_range(start=df['Date'].iloc[-1] + pd.DateOffset(days=1), periods=365)

google_prediction = pd.DataFrame()
google_prediction['Date'] = future_dates
google_prediction['Price'] = future_forecast

print(google_prediction)

# Unnormalize 'Price' column in df
df['Price'] = scaler.inverse_transform(np.array(df['Price']).reshape(-1,1))

# Select the last 3650 days
last_3650_days = df.tail(3650)

# Concatenate google_prediction dataframe to last_3650_days dataframe
google_df_with_prediction = pd.concat([last_3650_days, google_prediction])

# If 'Google_Predicted_Price' column is present, drop it
if 'Google_Predicted_Price' in google_df_with_prediction.columns:
    google_df_with_prediction = google_df_with_prediction.drop(['Google_Predicted_Price'], axis=1)

google_df_with_prediction = google_df_with_prediction[['Date', 'Price']]

print(google_df_with_prediction)

##############################################################################

# Get the current date and subtract one day
current_date = datetime.today()
end_date = current_date

# Format the end_date in 'YYYY-MM-DD' format
end_date_str = end_date.strftime('%Y-%m-%d')

# Get NASDAQ stock data
data = yf.download('^IXIC', start='2013-07-14', end=end_date_str)

# Reset index to make 'Date' a column
data.reset_index(inplace=True)

# Rename the columns to match the existing script
df = data.rename(columns={"Date": "Date", "Close": "Price"})

# We'll normalize the 'Price' column
scaler = MinMaxScaler()
df['Price'] = scaler.fit_transform(np.array(df['Price']).reshape(-1,1))

# Define the lookback period and split point for train and test data
lookback = 60  # assuming data is in daily frequency
split_point = int(len(df) * 0.8)

# Create training and test data
train = df['Price'].iloc[:split_point]
test = df['Price'].iloc[split_point:]

# Generate time series for training and test data
train_data_generator = TimeseriesGenerator(train, train, length=lookback, batch_size=20)
test_data_generator = TimeseriesGenerator(df['Price'], df['Price'], length=lookback, batch_size=1, start_index=split_point)

# Defining the optimal number of units as determined by hyperparameter tuning
optimal_units = 512

def build_optimized_model():
    model = Sequential()
    model.add(LSTM(units=optimal_units, activation='relu', return_sequences=True, input_shape=(lookback, 1)))
    model.add(LSTM(units=optimal_units, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

# Build the model with the optimal hyperparameters
model = build_optimized_model()

model.fit(train_data_generator, epochs=10)

# Predict the next 365 days
x_input = np.array(test[-lookback:]).reshape((1, lookback, 1))

future_forecast = []

for i in range(365):  # for the next 365 days
    yhat = model.predict(x_input, verbose=0)
    future_forecast.append(yhat[0])

    # append the prediction into x_input and drop the first value
    x_input = np.append(x_input[0][1:], [yhat])
    x_input = x_input.reshape((1, lookback, 1))

# Invert the scaling of predictions
future_forecast = scaler.inverse_transform(np.array(future_forecast).reshape(-1,1))

# Prepare the dataframe for the next 365 days prediction
future_dates = pd.date_range(start=df['Date'].iloc[-1] + pd.DateOffset(days=1), periods=365)

nasdaq_prediction = pd.DataFrame()
nasdaq_prediction['Date'] = future_dates
nasdaq_prediction['Price'] = future_forecast

print(nasdaq_prediction)

# Unnormalize 'Price' column in df
df['Price'] = scaler.inverse_transform(np.array(df['Price']).reshape(-1,1))

# Select the last 3650 days
last_3650_days = df.tail(3650)

# Concatenate nasdaq_prediction dataframe to last_3650_days dataframe
nasdaq_df_with_prediction = pd.concat([last_3650_days, nasdaq_prediction])

# If 'NASDAQ_Predicted_Price' column is present, drop it
if 'NASDAQ_Predicted_Price' in nasdaq_df_with_prediction.columns:
    nasdaq_df_with_prediction = nasdaq_df_with_prediction.drop(['NASDAQ_Predicted_Price'], axis=1)

nasdaq_df_with_prediction = nasdaq_df_with_prediction[['Date', 'Price']]

print(nasdaq_df_with_prediction)

####################################################################################

# Get the current date and subtract one day
current_date = datetime.today()
end_date = current_date

# Format the end_date in 'YYYY-MM-DD' format
end_date_str = end_date.strftime('%Y-%m-%d')

# Get DOW stock data
data = yf.download('^DJI', start='2013-07-14', end=end_date_str)

# Reset index to make 'Date' a column
data.reset_index(inplace=True)

# Rename the columns to match the existing script
df = data.rename(columns={"Date": "Date", "Close": "Price"})

# We'll normalize the 'Price' column
scaler = MinMaxScaler()
df['Price'] = scaler.fit_transform(np.array(df['Price']).reshape(-1,1))

# Define the lookback period and split point for train and test data
lookback = 60  # assuming data is in daily frequency
split_point = int(len(df) * 0.8)

# Create training and test data
train = df['Price'].iloc[:split_point]
test = df['Price'].iloc[split_point:]

# Generate time series for training and test data
train_data_generator = TimeseriesGenerator(train, train, length=lookback, batch_size=20)
test_data_generator = TimeseriesGenerator(df['Price'], df['Price'], length=lookback, batch_size=1, start_index=split_point)

def build_model():
    model = Sequential()
    model.add(LSTM(units=384, activation='relu', return_sequences=True, input_shape=(lookback, 1)))
    model.add(LSTM(units=384, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

model = build_model()

model.fit(train_data_generator, epochs=10)

# Predict the next 365 days
x_input = np.array(test[-lookback:]).reshape((1, lookback, 1))

future_forecast = []

for i in range(365):  # for the next 365 days
    yhat = model.predict(x_input, verbose=0)
    future_forecast.append(yhat[0])

    # append the prediction into x_input and drop the first value
    x_input = np.append(x_input[0][1:], [yhat])
    x_input = x_input.reshape((1, lookback, 1))

# Invert the scaling of predictions
future_forecast = scaler.inverse_transform(np.array(future_forecast).reshape(-1,1))

# Prepare the dataframe for the next 365 days prediction
future_dates = pd.date_range(start=df['Date'].iloc[-1] + pd.DateOffset(days=1), periods=365)

dow_prediction = pd.DataFrame()
dow_prediction['Date'] = future_dates
dow_prediction['Price'] = future_forecast

print(dow_prediction)

# Unnormalize 'Price' column in df
df['Price'] = scaler.inverse_transform(np.array(df['Price']).reshape(-1,1))

# Select the last 3650 days
last_3650_days = df.tail(3650)

# Concatenate dow_prediction dataframe to last_3650_days dataframe
dow_df_with_prediction = pd.concat([last_3650_days, dow_prediction])

# If 'Google_Predicted_Price' column is present, drop it
if 'Google_Predicted_Price' in dow_df_with_prediction.columns:
    dow_df_with_prediction = dow_df_with_prediction.drop(['Google_Predicted_Price'], axis=1)

dow_df_with_prediction = dow_df_with_prediction[['Date', 'Price']]

print(dow_df_with_prediction)

############################################################################
# Get the current date and subtract one day
current_date = datetime.today()
end_date = current_date

# Format the end_date in 'YYYY-MM-DD' format
end_date_str = end_date.strftime('%Y-%m-%d')

# Get SP500 stock data
data = yf.download('^GSPC', start='2013-07-14', end=end_date_str)

# Reset index to make 'Date' a column
data.reset_index(inplace=True)

# Rename the columns to match the existing script
df = data.rename(columns={"Date": "Date", "Close": "Price"})

# We'll normalize the 'Price' column
scaler = MinMaxScaler()
df['Price'] = scaler.fit_transform(np.array(df['Price']).reshape(-1,1))

# Define the lookback period and split point for train and test data
lookback = 60  # assuming data is in daily frequency
split_point = int(len(df) * 0.8)

# Create training and test data
train = df['Price'].iloc[:split_point]
test = df['Price'].iloc[split_point:]

# Generate time series for training and test data
train_data_generator = TimeseriesGenerator(train, train, length=lookback, batch_size=20)
test_data_generator = TimeseriesGenerator(df['Price'], df['Price'], length=lookback, batch_size=1, start_index=split_point)

def build_model():
    model = Sequential()
    model.add(LSTM(units=512, activation='relu', return_sequences=True, input_shape=(lookback, 1)))
    model.add(LSTM(units=512, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

model = build_model()

model.fit(train_data_generator, epochs=10)

# Predict the next 365 days
x_input = np.array(test[-lookback:]).reshape((1, lookback, 1))

future_forecast = []

for i in range(365):  # for the next 365 days
    yhat = model.predict(x_input, verbose=0)
    future_forecast.append(yhat[0])

    # append the prediction into x_input and drop the first value
    x_input = np.append(x_input[0][1:], [yhat])
    x_input = x_input.reshape((1, lookback, 1))

# Invert the scaling of predictions
future_forecast = scaler.inverse_transform(np.array(future_forecast).reshape(-1,1))

# Prepare the dataframe for the next 365 days prediction
future_dates = pd.date_range(start=df['Date'].iloc[-1] + pd.DateOffset(days=1), periods=365)

sp500_prediction = pd.DataFrame()
sp500_prediction['Date'] = future_dates
sp500_prediction['Price'] = future_forecast

print(sp500_prediction)

# Unnormalize 'Price' column in df
df['Price'] = scaler.inverse_transform(np.array(df['Price']).reshape(-1,1))

# Select the last 3650 days
last_3650_days = df.tail(3650)

# Concatenate sp500_prediction dataframe to last_3650_days dataframe
sp500_df_with_prediction = pd.concat([last_3650_days, sp500_prediction])

# If 'Google_Predicted_Price' column is present, drop it
if 'Google_Predicted_Price' in sp500_df_with_prediction.columns:
    sp500_df_with_prediction = sp500_df_with_prediction.drop(['Google_Predicted_Price'], axis=1)

sp500_df_with_prediction = sp500_df_with_prediction[['Date', 'Price']]

print(sp500_df_with_prediction)

##############################################################################

# Parameters 
n = 3 #the # of article headlines displayed per ticker
tickers = ['GOOGL']

# Get Data
finwiz_url = 'https://finviz.com/quote.ashx?t='
news_tables = {}

for ticker in tickers:
    url = finwiz_url + ticker
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urlopen(req)    
    html = BeautifulSoup(resp, features="lxml")
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

try:
    for ticker in tickers:
        df = news_tables[ticker]
        df_tr = df.findAll('tr')
    
        print ('\n')
        print ('Recent News Headlines for {}: '.format(ticker))
        
        for i, table_row in enumerate(df_tr):
            a_text = table_row.a.text
            td_text = table_row.td.text
            td_text = td_text.strip()
            print(a_text,'(',td_text,')')
            if i == n-1:
                break
except KeyError:
    pass

# Iterate through the news
parsed_news = []
for file_name, news_table in news_tables.items():
    for x in news_table.findAll('tr'):
        if x.a is not None:  # Check if x.a is not None
            text = x.a.get_text() 
            date_scrape = x.td.text.split()

            if len(date_scrape) == 1:
                time = date_scrape[0]

            else:
                date = date_scrape[0]
                time = date_scrape[1]

            ticker = file_name.split('_')[0]

            parsed_news.append([ticker, date, time, text])

# Sentiment Analysis
analyzer = SentimentIntensityAnalyzer()

columns = ['Ticker', 'Date', 'Time', 'Headline']
news = pd.DataFrame(parsed_news, columns=columns)
scores = news['Headline'].apply(analyzer.polarity_scores).tolist()

df_scores = pd.DataFrame(scores)
news = news.join(df_scores, rsuffix='_right')

# View Data 
news['Date'] = pd.to_datetime(news.Date).dt.date

unique_ticker = news['Ticker'].unique().tolist()
news_dict = {name: news.loc[news['Ticker'] == name] for name in unique_ticker}

values = []
for ticker in tickers: 
    dataframe = news_dict[ticker]
    dataframe = dataframe.set_index('Ticker')
    dataframe = dataframe.drop(columns = ['Headline'])
    print ('\n')
    print (dataframe.head())
    
    mean = round(dataframe['compound'].mean(), 2)
    values.append(mean)
    
df = pd.DataFrame(list(zip(tickers, values)), columns =['Ticker', 'Mean Sentiment']) 
df = df.set_index('Ticker')
df = df.sort_values('Mean Sentiment', ascending=False)
print ('\n')
print (df)

# Calculate the daily mean sentiment score and store it in 'googl_sent'
googl_sent = news.groupby(['Ticker', 'Date'])['compound'].mean()

# Reset the index to make 'Ticker' and 'Date' into columns again
googl_sent = googl_sent.reset_index()

# Rename the columns
googl_sent = googl_sent.rename(columns={"Ticker": "Ticker", "Date": "Date", "compound": "Sentiment"})

# Remove the 'Ticker' column
googl_sent = googl_sent.drop(columns=["Ticker"])

# Print the daily mean sentiment score
print(googl_sent)


###################################################################################

import pandas as pd
import requests

# Fetch Fear Greed Index data from alternative.me API
response = requests.get('https://api.alternative.me/fng/?limit=3650')
data = response.json()

# Extract relevant data from the API response
fgi_data = data['data']

# Create a list of dictionaries to store the data
fgi_list = []

# Iterate over the API data and store it in the list
for item in fgi_data:
    fgi_dict = {
        'Date': pd.to_datetime(item['timestamp'], unit='s').date(),
        'Fear Greed Index': item['value'],
        'Index Value': item['value_classification']
    }
    fgi_list.append(fgi_dict)

# Create a DataFrame from the list of dictionaries
fear_greed = pd.DataFrame(fgi_list)

# Print the DataFrame
print(fear_greed)

#####################################################################################

# Ensure 'Date' column is in datetime format for all dataframes
dow_df_with_prediction['Date'] = pd.to_datetime(dow_df_with_prediction['Date'])
nasdaq_df_with_prediction['Date'] = pd.to_datetime(nasdaq_df_with_prediction['Date'])
dow_df_with_prediction['Date'] = pd.to_datetime(dow_df_with_prediction['Date'])
sp500_df_with_prediction['Date'] = pd.to_datetime(sp500_df_with_prediction['Date'])
googl_sent['Date'] = pd.to_datetime(googl_sent['Date'])
fear_greed['Date'] = pd.to_datetime(fear_greed['Date'])

# Now you can merge your dataframes
merged_data = google_df_with_prediction.merge(nasdaq_df_with_prediction, on='Date', how='outer', suffixes=('_google', '_nasdaq'))
merged_data = merged_data.merge(dow_df_with_prediction, on='Date', how='outer', suffixes=('', '_dow'))
merged_data = merged_data.merge(sp500_df_with_prediction, on='Date', how='outer', suffixes=('', '_sp500'))
merged_data = merged_data.merge(googl_sent, on='Date', how='outer', suffixes=('', '_googl_sent'))
merged_data = merged_data.merge(fear_greed, on='Date', how='outer', suffixes=('', '_fear_greed'))
merged_data.rename(columns={'Price': 'Price_dow'}, inplace=True)

stock_data = merged_data

#####################################################################################

# Load the data
data = stock_data

data['Fear Greed Index'] = pd.to_numeric(data['Fear Greed Index'], errors='coerce')

# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Filter data after 2018-02-01
data = data[data['Date'] >= '2018-02-01']

# Drop the 'Index Value' column
data = data.drop('Index Value', axis=1)

# Forward fill the missing values
data = data.fillna(method='ffill')

# If there are still any missing values (e.g. at the start of the dataset), fill them with backward fill
data = data.fillna(method='bfill')

# Split the data into training and testing sets based on the provided date
train = data[data['Date'] < '2023-07-18']
test = data[data['Date'] >= '2023-07-18']

# Prepare the features and target variable
X_train = train.drop(['Date', 'Price_google'], axis=1)
y_train = train['Price_google']

X_test = test.drop(['Date', 'Price_google'], axis=1)
y_test = test['Price_google']

# Train the XGBoost model
xgb = XGBRegressor(random_state=42)
xgb.fit(X_train, y_train)

# Make predictions on the test set
xgb_predictions = xgb.predict(X_test)

# Ensure predictions are positive (since stock prices can't be negative)
xgb_predictions = np.maximum(xgb_predictions, 0)

# Calculate the ensemble predictions as the average of the XGBoost and LSTM predictions
ensemble_predictions = (xgb_predictions + y_test) / 2

# Create a DataFrame to hold the ensemble predictions
ensemble_df = pd.DataFrame({
    'Date': test['Date'],
    'Ensemble_Predictions': ensemble_predictions
})

# Display the ensemble predictions for the next 365 days
print(ensemble_df)

################################################################################


# Get the current date
current_date = datetime.today()
end_date = current_date

# Format the end_date in 'YYYY-MM-DD' format
end_date_str = end_date.strftime('%Y-%m-%d')

# Get Google stock data
data = yf.download('GOOGL', start='2013-07-14', end=end_date_str)

# Reset index to make 'Date' a column
data.reset_index(inplace=True)

# Load the first dataframe
df1 = data

# Reduce the dataframe to just the 'Date' and 'Close' columns
df1_reduced = df1[['Date', 'Close']]

# Load the second dataframe
df2 = ensemble_df

# Rename the 'Ensemble_Predictions' column to 'Close' in df2
df2.rename(columns={'Ensemble_Predictions': 'Close'}, inplace=True)

# Combine the dataframes so they follow on from each other
ensemble_df = pd.concat([df1_reduced, df2], ignore_index=True)

# Display the combined dataframe
print(ensemble_df)
