import os
import streamlit as sl
from auth.auth_manager import validate_user, save_user  # Ensure proper imports
from stock_analysis.my_streamlit import main_dashboard, contact_form  # Import main_dashboard and contact_form

# base directory for relative CSV paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "CSVNepse")

# --- SECTOR TO STOCK MAPPING ---
sector_to_stocks = {
    "Commercial Bank": {
        "Sanima": os.path.join(DATA_DIR, "Bank(Sanima).csv"),
        "Nabil": os.path.join(DATA_DIR, "Bank(Nabil).csv"),
        "NIMB": os.path.join(DATA_DIR, "Bank(NIMB).csv")
    },
    "Development Bank": {
        "GBBL": os.path.join(DATA_DIR, "Development Bank(GBBL).csv"),
        "MNBBL": os.path.join(DATA_DIR, "Development Bank(MNBBL).csv"),
        "SHINE": os.path.join(DATA_DIR, "DevelopmentBank(SHINE).csv")
    },
    "Finance": {
        "Gurkhas Finance Limited": os.path.join(DATA_DIR, "Finance(GurkhasFinanceLimited).csv"),
        "ICFC Finance Limited": os.path.join(DATA_DIR, "Finance(ICFC Finance Limited).csv"),
        "Manjushree Finance Limited": os.path.join(DATA_DIR, "Finance(ManjushreeFinanceLimited).csv")
    },
    "Hotel & Tourism": {
        "CGH": os.path.join(DATA_DIR, "Hotel&Tourism(CGH).csv"),
        "SHL": os.path.join(DATA_DIR, "Hotel&Tourism(SHL).csv"),
        "TRH": os.path.join(DATA_DIR, "Hotel&Tourism(TRH).csv")
    },
    "Hydropower": {
        "API": os.path.join(DATA_DIR, "Hydropower(API).csv"),
        "CHCL": os.path.join(DATA_DIR, "Hydropower(CHCL).csv"),
        "SAHAS": os.path.join(DATA_DIR, "Hydropower(SAHAS).csv")
    },
    "Insurance": {
        "NLICL": os.path.join(DATA_DIR, "Insurance(NLICL).csv")
    },
    "Investment": {
        "CIT": os.path.join(DATA_DIR, "Investment(CIT).csv"),
        "HIDCL": os.path.join(DATA_DIR, "Investment(HIDCL).csv"),
        "NIFRA": os.path.join(DATA_DIR, "Investment(NIFRA).csv")
    },
    "Life Insurance": {
        "LICN": os.path.join(DATA_DIR, "Life Insurance(LICN).csv"),
        "NLIC": os.path.join(DATA_DIR, "Life Insurance(NLIC).csv")
    },
    "Manufacturing and Processing": {
        "BNL": os.path.join(DATA_DIR, "Manufacturing&Processing(BNL).csv"),
        "BNT": os.path.join(DATA_DIR, "Manufacturing&Processing(BNT).csv"),
        "UNL": os.path.join(DATA_DIR, "Manufacturing&Processing(UNL).csv")
    },
    "Microfinance": {
        "CBBL": os.path.join(DATA_DIR, "Microfinance(CBBL).csv"),
        "FOWAD": os.path.join(DATA_DIR, "Microfinance(FOWAD).csv"),
        "MERO": os.path.join(DATA_DIR, "Microfinance(MERO).csv")
    },
    "Non-Life Insurance": {
        "SPIL": os.path.join(DATA_DIR, "Non_Life Insurance(SPIL).csv"),
        "NIL": os.path.join(DATA_DIR, "Non-Life Insurance(NIL).csv"),
        "RBCL": os.path.join(DATA_DIR, "Non-Life Insurance(RBCL).csv")
    },
    "Trading": {
        "STC": os.path.join(DATA_DIR, "Trading(STC).csv")
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