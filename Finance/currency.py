import matplotlib
matplotlib.use("Agg")
import requests as re
import matplotlib.pyplot as plt
from decimal import Decimal
from datetime import datetime as d
import numpy as np
from flask import Flask, redirect, url_for, render_template_string, request
import io
import base64

apikey = "8f7cc74778c6437c9fb12d63272f80c8"

image_list = []

exchange_one = "USD"
exchange_two = "MYR"

def fetch_data(symbol,interval,outputsize):
    url =  "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": apikey
    }

    res = re.get(url,params=params)
    data = dict(res.json())
    print(data)
    return data["values"]


def week():
 data = fetch_data(symbol="USD/MYR", interval="1day",outputsize=7)

 y = []
 for i in range(1,8):
    y.append(int(i))

 x = []
 for i in range(0,len(data)):
    x.append(Decimal(data[i]["close"]))

 combine = list(zip(x,y))

 x = np.array(x)
 y = np.array(y)
 print(x)
 print(y)
 print(combine)
 plt.scatter(y,x,color="red")
 plt.plot(y,x)
 plt.grid(linestyle="--",linewidth=0.3,color="green")
 plt.xlabel("Past 7 days")
 plt.ylabel("Malaysian Ringgit")
 plt.title("USD to MYR")
 plt.show()

def months(exchange_one,exchange_two):
 data = fetch_data(symbol=f'{exchange_one}/{exchange_two}', interval="1month",outputsize=12)

 y = []
 for i in range(1,13):
    y.append(int(i))

 x = []
 for i in range(0,len(data)):
    x.append(Decimal(data[i]["close"]))

 combine = list(zip(x,y))

 x = np.array(x)
 y = np.array(y)
 print(x)
 print(y)
 print(combine)
 plt.scatter(y,x,color="red")
 plt.plot(y,x)
 plt.grid(linestyle="--",linewidth=0.3,color="green")
 plt.xlabel("Past 12 months")
 plt.ylabel(f"{exchange_two}")
 """
 match symbol:
  case "AUD/MYR":
    t = "AUD to MYR"
  case "USD/MYR":
    t = "USD to MYR"
  case "SGD/MYR":
    t = "SGD to MYR"
  case "CAD/MYR":
    t = "CAD to MYR"
  """
 plt.title(f"{exchange_one} to {exchange_two}",fontsize=17.5)

 buffer = io.BytesIO()
 plt.savefig(buffer, format="png")
 buffer.seek(0)
 image = base64.b64encode(buffer.read()).decode("utf-8")
 buffer.close()

 image_list.append(image)
 plt.close()
 #plt.show()



def hours(exchange_one,exchange_two):
 data = fetch_data(symbol=f'{exchange_one}/{exchange_two}', interval="1h",outputsize=24)

 y = []
 for i in range(1,25):
    y.append(int(i))

 x = []
 for i in range(0,len(data)):
    x.append(Decimal(data[i]["close"]))

 combine = list(zip(x,y))

 x = np.array(x)
 y.reverse()
 y = np.array(y)
 print(x)
 print(y)
 print(combine)
 #plt.scatter(y,x,color="red",s=10)
 plt.plot(y,x)
 plt.grid(linestyle="--",linewidth=0.3,color="green")
 plt.xlabel("Past 1 day")
 plt.ylabel(f"{exchange_two}")
 """
 match symbol:
  case "AUD/MYR":
    t = "AUD to MYR"
  case "USD/MYR":
    t = "USD to MYR"
  case "SGD/MYR":
    t = "SGD to MYR"
  case "CAD/MYR":
    t = "CAD to MYR"
  """
 plt.title(f"{exchange_one} to {exchange_two}",fontsize=17.5)


 buffer = io.BytesIO()
 plt.savefig(buffer, format="png")
 buffer.seek(0)
 image = base64.b64encode(buffer.read()).decode("utf-8")
 buffer.close()

 image_list.append(image)
 plt.close()
 #plt.show()




"""
list_currency = ["AUD/MYR","USD/MYR","SGD/MYR","CAD/MYR"]
list_title = ["AUD to MYR","USD to MYR","SGD to MYR","CAD to MYR"]

for x in list_currency:
  months(x)
  hours(x)
"""

currency_codes = [
    "USD",  # United States Dollar
    "EUR",  # Eurozone (Germany, France, etc.)
    "GBP",  # United Kingdom Pound Sterling
    "JPY",  # Japanese Yen
    "CAD",  # Canadian Dollar
    "AUD",  # Australian Dollar
    "NZD",  # New Zealand Dollar
    "CHF",  # Swiss Franc
    "SGD",  # Singapore Dollar
    "MYR",  # Malaysian Ringgit
    "CNY",  # Chinese Yuan Renminbi
    "INR",  # Indian Rupee
    "KRW",  # South Korean Won
    "IDR",  # Indonesian Rupiah
    "THB",  # Thai Baht
    "PHP",  # Philippine Peso
    "VND",  # Vietnamese Dong
    "BRL",  # Brazilian Real
    "MXN",  # Mexican Peso
    "ZAR",  # South African Rand
    "RUB",  # Russian Ruble
    "SAR",  # Saudi Riyal
    "AED",  # UAE Dirham
    "EGP",  # Egyptian Pound
    "TRY",  # Turkish Lira
    "PKR",  # Pakistani Rupee
    "BDT",  # Bangladeshi Taka
    "NGN",  # Nigerian Naira
    "KES",  # Kenyan Shilling
    "ARS",  # Argentine Peso
    "ILS",  # Israeli New Shekel
    "HKD",  # Hong Kong Dollar
    "TWD",  # New Taiwan Dollar
    "NOK",  # Norwegian Krone
    "SEK",  # Swedish Krona
    "DKK",  # Danish Krone
    "PLN",  # Polish Zloty
    "HUF",  # Hungarian Forint
    "CZK",  # Czech Koruna
    "CLP",  # Chilean Peso
    "COP",  # Colombian Peso
]

months(exchange_one,exchange_two)
hours(exchange_one,exchange_two)

app = Flask(__name__)
@app.route("/", methods=["GET","POST"])
def index():
  if request.method == "POST":
    image_list.clear()
    exchange_one = request.form.get("one")
    exchange_two = request.form.get("two")
    if exchange_one == exchange_two: 
      return "Do not put both of the currency symbol the same"
    else:
     months(exchange_one,exchange_two)
     hours(exchange_one,exchange_two)
     return redirect(url_for("index"))

  return render_template_string("""
    <html>
    <meta name="viewport" content="width=device-width , initial-scale=1.0"/>
    <body>
    <form method="POST">
    <fieldset>
      <div>
        <select name="one">
      {% for x in currency_codes %}
      <option value={{x}}>{{x}}</option>
      {% endfor %}
    </select>
        <h4>Change to</h4>
    <select name="two">
      {% for x in currency_codes %}
      <option value={{x}}>{{x}}</option>
      {% endfor %}
    </select>
    </div>
    <button>Proceed</button>
    </fieldset>
  </form>

  <style>
    fieldset {
      border: 2px solid black;
      border-radius: 10px;
      width: 100px;
      background-color: white;
    }
    body {
      background-color: rgba(78, 78, 78, 0.862);
    }
    form {
      display: flex;
      justify-content: center;
    }
    select {
      font-size: 20px;
    }
    button {
      color: balck;
      background-color: rgb(16, 208, 242);
      border: 1px;
      border-radius: 4px;
      padding: 5px;
      font-size: 14px;
      margin-top: 20px;
      margin-left: 20px;
    }
    img {
      margin-left: 60px; 
      margin-top: 60px;
    }
  </style>
   {% for x in image %}
    <img src="data:image/png;base64, {{x}}">                  
   {% endfor %}
    </body>
    </html>
""", image=image_list,currency_codes=currency_codes)

if __name__ == "__main__":
  app.run(debug=False)











