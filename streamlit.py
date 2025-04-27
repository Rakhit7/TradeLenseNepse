import streamlit as sl
from auth.auth_manager import validate_user, save_user  # Ensure proper imports
from stock_analysis.my_streamlit import main_dashboard, contact_form  # Import main_dashboard and contact_form

# --- SECTOR TO STOCK MAPPING ---
sector_to_stocks = {
    "Commercial Bank": {
        "Sanima": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Bank(Sanima).csv",
        "Nabil": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Bank(Nabil).csv",
        "NIMB": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Bank(NIMB).csv"
    },
    "Development Bank": {
        "GBBL": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Development Bank(GBBL).csv",
        "MNBBL": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Development Bank(MNBBL).csv",
        "SHINE": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/DevelopmentBank(SHINE).csv"
    },
    "Finance": {
        "Gurkhas Finance Limited": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Finance(GurkhasFinanceLimited).csv",
        "ICFC Finance Limited": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Finance(ICFC Finance Limited).csv",
        "Manjushree Finance Limited": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Finance(ManjushreeFinanceLimited).csv"
    },
    "Hotel & Tourism": {
        "CGH": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Hotel&Tourism(CGH).csv",
        "SHL": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Hotel&Tourism(SHL).csv",
        "TRH": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Hotel&Tourism(TRH).csv"
    },
    "Hydropower": {
        "API": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Hydropower(API).csv",
        "CHCL": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Hydropower(CHCL).csv",
        "SAHAS": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Hydropower(SAHAS).csv"
    },
    "Insurance": {
        "NLICL": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Insurance(NLICL).csv"
    },
    "Investment": {
        "CIT": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Investment(CIT).csv",
        "HIDCL": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Investment(HIDCL).csv",
        "NIFRA": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Investment(NIFRA).csv"
    },
    "Life Insurance": {
        "LICN": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Life Insurance(LICN).csv",
        "NLIC": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Life Insurance(NLIC).csv"
    },
    "Manufacturing and Processing": {
        "BNL": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Manufacturing&Processing(BNL).csv",
        "BNT": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Manufacturing&Processing(BNT).csv",
        "UNL": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Manufacturing&Processing(UNL).csv"
    },
    "Microfinance": {
        "CBBL": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Microfinance(CBBL).csv",
        "FOWAD": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Microfinance(FOWAD).csv",
        "MERO": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Microfinance(MERO).csv"
    },
    "Non-Life Insurance": {
        "SPIL": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Non_Life Insurance(SPIL).csv",
        "NIL": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Non-Life Insurance(NIL).csv",
        "RBCL": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Non-Life Insurance(RBCL).csv"
    },
    "Trading": {
        "STC": "/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/CSVNepse/Trading(STC).csv"
    }
}

# --- LOGIN PAGE ---
def login_page():
    sl.title("🔑 Login to TradeLensNepse")
    username = sl.text_input("Username")
    password = sl.text_input("Password", type="password")
    if sl.button("Login"):
        if validate_user(username, password):
            sl.success("Login successful!")
            sl.session_state.logged_in = True
            sl.session_state.username = username
        else:
            sl.error("Invalid username or password.")

# --- REGISTER PAGE ---
def register_page():
    sl.title("📝 Register for TradeLensNepse")
    username = sl.text_input("Choose a Username")
    password = sl.text_input("Choose a Password", type="password")
    confirm_password = sl.text_input("Confirm Password", type="password")
    if sl.button("Register"):
        if password == confirm_password:
            try:
                save_user(username, password)
                sl.success("Registration successful! Please log in.")
            except ValueError as e:
                sl.error(str(e))
        else:
            sl.error("Passwords do not match.")

# --- PAGE NAVIGATION ---
if "logged_in" not in sl.session_state:
    sl.session_state["logged_in"] = False

if sl.session_state["logged_in"]:
    # Redirect to the main dashboard from my_streamlit.py
    main_dashboard(sector_to_stocks)
    contact_form()
else:
    page = sl.sidebar.radio("Navigation", ["Login", "Register"])
    if page == "Login":
        login_page()
    elif page == "Register":
        register_page()