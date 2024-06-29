import json
import requests
import key
# import datetime as dt

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": key.STOCK_NAME,
    "outputsize": "compact",
    "apikey": key.AD_STOCK_KEY,
}

news_params = {
    "q": key.NA_COMPANY_NAME,
    # "from": dt.datetime.now(),
    "sortBy": "popularity",
    "apikey": key.NA_API_KEY,
}

# read file else create file with data collected
try:
    with open("response.json") as resp_file:
        data_j = json.load(resp_file)
except FileNotFoundError:
    response = requests.get(key.STOCK_URL, params=stock_params)
    response.raise_for_status()
    data = response.json()
    with open("response.json", "w") as resp_file:
        json.dump(data, resp_file)

dates = [key for (key, value) in data_j["Time Series (Daily)"].items()]

stock_price_on_day = data_j["Time Series (Daily)"][dates[0]]["4. close"]
stock_price_day_before = data_j["Time Series (Daily)"][dates[1]]["4. close"]

difference = round(abs(float(stock_price_on_day)
                       - float(stock_price_day_before)), 2)

percentual_change = round((difference / float(stock_price_day_before)) * 100, 2)

if percentual_change > 5:
    try:
        with open("news.json") as resp_file:
            news_j = json.load(resp_file)
    except FileNotFoundError:
        news = requests.get(key.NA_URL, params=news_params)
        news.raise_for_status()
        datan = news.json()
        with open("news.json", "w") as resp_file:
            json.dump(datan, resp_file)

news_slice = news_j["articles"][0:3]
for i in range(0, len(news_slice)):
    print(news_slice[i]["title"])

# STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

# TODO 9. - Send each article as a separate message via Twilio.


# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
