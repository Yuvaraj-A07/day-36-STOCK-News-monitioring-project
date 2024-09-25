import requests
import smtplib
import html
import manager as mg

# ################# INCOMPLETE PROJECT#################

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
perc = ""
my_mail = mg.my_mail
password = mg.password

stock_api_key = mg.stock_api_key
news_api_key = mg.news_api_key
# https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=0TJOZL00PKE2H1Q5
# https://newsapi.org/v2/everything?q=tesla&from=2024-01-05&sortBy=publishedAt&apiKey=452da1273f73442b96350e071a5236c6

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api_key
}

response = requests.get(url="https://www.alphavantage.co/query?", params=parameters)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]
list_stock_data = [value for (key, value) in stock_data.items()]

date_stock_data = [key for (key, value) in stock_data.items()]

yesterday_data = list_stock_data[0]
yesterday_closing_price = float(yesterday_data["4. close"])

db_yesterday_data = list_stock_data[1]
db_yesterday_closing_price = float(db_yesterday_data["4. close"])

difference = abs(yesterday_closing_price - db_yesterday_closing_price)

diff_percent = (difference / yesterday_closing_price)*100

if diff_percent > 0.5:

    ## STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    # https://newsapi.org/v2/everything?q=tesla&from=2024-01-05&sortBy=publishedAt&apiKey=452da1273f73442b96350e071a5236c6

    news_parameter = {
        "qInTitle": COMPANY_NAME,
        # "sortBy": "publishedAt",
        # "from": date_stock_data[0],
        # "language": "en",
        "apikey": news_api_key
    }
    news_response = requests.get(url="https://newsapi.org/v2/everything?", params=news_parameter)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    three_articles = news_data[0:3]


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

    total_news = [f"Headline: {news['title']}\n\n Brief: {news['description']}" for news in three_articles]
    print(total_news)

    if yesterday_closing_price > db_yesterday_closing_price:
        perc = f"INCREASE BY {difference}%"
    else:
        perc = f"DECREASE BY {difference}%"
    for send in total_news:
        with smtplib.SMTP("smtp.gmail.com") as send_quote:
            send_quote.starttls()
            send_quote.login(user=my_mail, password=password)
            send_quote.sendmail(from_addr=my_mail,
                                to_addrs=my_mail,
                                msg=send)

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

