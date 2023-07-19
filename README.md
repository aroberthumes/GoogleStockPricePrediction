# GoogleStockPricePrediction

# Stock Analysis & Prediction with LSTM and XGBoost

This project implements a Stock Analysis and Prediction application using Streamlit, yfinance, Plotly, LSTM networks, XGBoost regressor, VADER sentiment analyzer, and the Fear & Greed index. 

The application fetches historical stock price data of Google, NASDAQ, DOW, and S&P 500 from the Yahoo Finance platform and displays the "Open" and "Close" prices in interactive graphs. Sentiment analysis on Google news headlines and Fear & Greed index data are also used for predictions.

## Features

1. Fetch and display historical stock data.
2. Provide an interactive UI element to select the number of past days to display.
3. Display raw data of stock prices.
4. Perform predictions using LSTM networks and XGBoost regressor based on stock prices, sentiment analysis scores, and Fear & Greed index data.
5. Display ensemble predictions of Google's future stock prices.

## Prerequisites

- Python 3.6+
- Numpy
- Pandas
- Matplotlib
- Scikit-learn
- Keras
- TensorFlow
- XGBoost
- NLTK
- VADER Sentiment
- Requests
- BeautifulSoup
- Streamlit
- yfinance
- Plotly

## Installation

1. **Python**: You can download and install Python from the official website: https://www.python.org/. Ensure you have Python 3.6 or later installed.

2. **Python Libraries**: Once Python is installed, you can use pip to install the necessary Python libraries:

```
pip install numpy pandas matplotlib scikit-learn keras tensorflow xgboost nltk vaderSentiment requests beautifulsoup4 streamlit yfinance plotly
```

3. **NLTK Data**: After installing the nltk package, you need to download the necessary nltk data:

```
python -m nltk.downloader all
```

4. **Project Cloning**: You can clone the repository to your local machine for usage and development by using the following command:

```
git clone https://github.com/<your_username>/stock-market-prediction.git
```

After installation, navigate to the project directory and run the Python scripts or Jupyter notebooks in your preferred order.

*Please replace <your_username> with your actual GitHub username.*

## Project Workflow

1. **Fetching Historical Stock Data**: The application uses Yahoo Finance data to fetch historical stock prices for Google, DOW, NASDAQ, and S&P 500 indices.

2. **Stock Data Visualization**: It then provides an interactive UI to select the number of past days to display for each stock/index. 

3. **LSTM Stock Price Prediction**: LSTM models are trained on this data and used to predict future stock prices.

4. **Sentiment Analysis and Fear & Greed Index**: The application also performs sentiment analysis on Google news headlines using the VADER sentiment analyzer and fetches the Fear and Greed index data, which are used as features for the ensemble model.

5. **Ensemble Prediction with XGBoost**: Lastly, an XGBoost model is trained on the stock prices, sentiment scores, and Fear and Greed index data. The application combines LSTM and XGBoost predictions to form an ensemble prediction model, which is displayed in an interactive graph.

## Output

The application displays an interactive plot of historical and predicted Google stock prices. The raw data of the stocks and indices for the selected number of days is also shown. 

The final output of the project is a CSV file containing the predicted Google stock prices for the next 365 days, which includes the predictions from both the LSTM and XGBoost models.

## Note

This project is for educational purposes and should not be used for actual trading. Please do your own research before making any investment decisions.

The ensemble learning model that produces the predictions has been exported to a CSV and is uploaded to the Streamlit web app portion.

## License

This project is licensed under the terms of the MIT license.
