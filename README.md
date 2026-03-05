##Greetings. This is a project I created as to see and analyse the accuracy of various models and to see if in fact they can make accurate prediction in real world markets. 

---

# TradeLensNepse – NEPSE Stock‑Price Predictor

A Streamlit dashboard that lets you browse historical data for Nepal Stock
Exchange (NEPSE) listed companies, see interactive charts and a 6‑month
LSTM‑based forecast, and get a simple “buy/don’t buy” recommendation.  
You can also register/login and send messages through a sidebar contact form.



![screenshot](https://github.com/Rakhit7/TradeLenseNepse/blob/1de8ff9f00b7b5977b85d8a9618b6d28f614842d/landing.png)


---

## Features

- Sector → company selector, date filters, and data preview
- Plotly charts showing price history, forecasts, moving averages,
  volatility, and returns distribution
- LSTM model built with TensorFlow/Keras for 180‑day price prediction
- Evaluation metrics (MAE, RMSE, R²) and risk/trend decision logic
- User authentication (simple JSON store)
- Contact form that sends email using `yagmail`
- Custom styles, Lottie animation, and various Streamlit widgets

---

## Prerequisites

- **macOS / Linux / Windows** with Python 3.10  
  *(project has been tested with 3.10.12; other 3.10.x versions should work)*
- `python3.10` installed (via system package manager, pyenv, Homebrew, etc.)
- Git (optional if cloning from GitHub)

---

## Setup

```bash
# clone the repository
git clone https://github.com/<your‑username>/TradeLensNepse.git
cd TradeLensNepse

# create & activate virtualenv (must be Python 3.10)
python3.10 -m venv stock_market_env
source stock_market_env/bin/activate         # macOS / Linux
# .\stock_market_env\Scripts\activate        # Windows PowerShell

# upgrade pip and install dependencies
python -m pip install --upgrade pip
python -m pip install -r [requirements.txt](http://_vscodecontentref_/0)
