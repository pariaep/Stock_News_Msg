import requests
from datetime import datetime, timedelta
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
FUNCTION = "TIME_SERIES_DAILY"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_APIKEY = "NEW_API_KEY"
STOCK_APIKEY = "YOUR_API_KEY"
account_sid = "YOUR_SID"
auth_token = "AUTH_TOKEN"

parameters = {
    "function": FUNCTION,
    "symbol": STOCK,
    "apikey": STOCK_APIKEY
}
news_prams = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_APIKEY,
    "language": "en"
}
today = datetime.today()
yesterday = (str(today - timedelta(1)).split())[0]
day_before_y = (str(today - timedelta(2)).split())[0]

response = requests.get(url=STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()
daily_data = data["Time Series (Daily)"]

yesterday_closing = float(daily_data[yesterday]['4. close'])
day_before_y_closing = float(daily_data[day_before_y]['4. close'])
difference = yesterday_closing - day_before_y_closing
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
diff_percent = round((difference / yesterday_closing) * 100)
if abs(diff_percent) >= 1:
    news_data = requests.get(url=NEWS_ENDPOINT, params=news_prams)
    news_data.raise_for_status()
    news = news_data.json()["articles"]
    three_news = news[:3]
    news_list = [f"{STOCK}: {up_down}{diff_percent}% \nHeadlines: {article['title']}. \nBrief: {article['description']}"
                 for article in three_news]
    client = Client(account_sid, auth_token)
    for news_article in news_list:
        message = client.messages \
            .create(
                from_='+NUmber',
                body=news_article,
                to='YOUR_NUMBER'
            )
