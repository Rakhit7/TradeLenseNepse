from pathlib import Path
import pandas as pd
import streamlit as sl
import json
from stock_analysis.stock_analyzer import analyze_stock  # Importing analyze_stock
from streamlit_lottie import st_lottie  # For animations
import requests
import yagmail  # Import yagmail for email functionality
import plotly.express as px  # Import Plotly for interactive charts

# --- Load Config ---
def load_config():
    """Load the configuration file."""
    config_path = Path("/Users/rakhit/Desktop/YEAR 3/TradeLenseNepse/stock_analysis/config.json")
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        sl.error(f"Config file not found at {config_path}")
        return None
    except json.JSONDecodeError as e:
        sl.error(f"Error parsing config file: {e}")
        return None

# --- LOTTIE ANIMATION LOADER ---
def load_lottie_url(url: str):
    """Load Lottie animation from a URL."""
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# --- MAIN DASHBOARD ---
def main_dashboard(sector_to_stocks):
    # Header Animation
    lottie_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_0yfsb3a1.json")
    if lottie_animation:
        st_lottie(lottie_animation, height=200, key="header-animation")

    sl.title("📈 TradeLensNepse - NEPSE Stock Prediction")
    sl.markdown("## A Predictive Model for the Nepal Stock Exchange")
    sl.markdown("---")

    # --- USER PREFERENCES IN SIDEBAR ---
    sl.sidebar.subheader("User Preferences")
    sector = sl.sidebar.selectbox("🏦 Select Your Investment Sector:", options=list(sector_to_stocks.keys()), index=0)
    company_options = list(sector_to_stocks[sector].keys())
    companies = sl.sidebar.multiselect("📊 Choose your preferred companies:", company_options)

    # --- DATE FILTERING OPTIONS ---
    sl.sidebar.subheader("Date Filtering")
    start_date = sl.sidebar.date_input("Start Date")
    end_date = sl.sidebar.date_input("End Date")

    if sl.sidebar.button("Submit Preferences"):
        if len(companies) == 1:
            selected_company = companies[0]
            sl.success(f"Preferences submitted successfully for {selected_company}!")

            # Get the CSV file path
            stock_file_path = sector_to_stocks[sector][selected_company]

            # Load and display the CSV file
            try:
                stock_data = pd.read_csv(stock_file_path, header=0)
                stock_data['Date'] = pd.to_datetime(stock_data['Date'], dayfirst=True)  # Specify dayfirst=True

                # Apply date filtering
                filtered_data = stock_data[
                    (stock_data['Date'] >= pd.to_datetime(start_date)) &
                    (stock_data['Date'] <= pd.to_datetime(end_date))
                ]

                sl.dataframe(filtered_data)  # Display the filtered data

                # --- PLOTLY CHART ---
                fig = px.line(filtered_data, x='Date', y='Close', title='Stock Prices Over Time')
                sl.plotly_chart(fig)  # Display the interactive Plotly chart

                # Call analyze_stock and display the graphs and metrics
                fig1, fig2, fig3, fig4, fig5, decision_message, mae, rmse, r2 = analyze_stock(stock_file_path)
                sl.plotly_chart(fig1)  # Display the first graph
                sl.plotly_chart(fig2)  # Display the second graph
                sl.plotly_chart(fig3)  # Display the third graph
                sl.plotly_chart(fig4)  # Display the fourth graph
                sl.plotly_chart(fig5)  # Display the fifth graph

                # Display the investment decision
                sl.markdown(f"### Investment Decision")
                sl.info(decision_message)

                # Display model evaluation metrics
                sl.markdown("### Model Evaluation Metrics")
                sl.write(f"Mean Absolute Error (MAE): {mae:.2f}")
                sl.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
                sl.write(f"R-squared (R2): {r2:.2f}")

            except FileNotFoundError:
                sl.error(f"File not found: {stock_file_path}")
            except Exception as e:
                sl.error(f"Error loading file: {e}")
        elif len(companies) > 1:
            sl.error("Please select only one company to view its graphs.")
        else:
            sl.error("No company selected. Please select one company to proceed.")

    # --- FOOTER ---
    sl.markdown("---")
    sl.caption("📌 Powered by TradeLensNepse | Stock Prediction for NEPSE")

# --- CONTACT FORM IN SIDEBAR ---
def contact_form():
    with sl.sidebar.expander("📞 Contact Us"):
        sl.markdown("We'd love to hear from you! Please fill out the form below to get in touch.")

        with sl.form("contact_form"):
            name = sl.text_input("Your Name")
            email = sl.text_input("Your Email")
            message = sl.text_area("Your Message")
            submitted = sl.form_submit_button("Submit")

            if submitted:
                # Send the message via email
                try:
                    # Initialize yagmail with your email and app password
                    yag = yagmail.SMTP("rakhitthapa@gmail.com", "riik ojec zqzl bvaq")
                    
                    # Send the email using the user's email from the form
                    yag.send(
                        to=email,  # Use the email provided in the form
                        subject=f"New Contact Form Submission from {name}",
                        contents=f"""
                        Name: {name}
                        Email: {email}
                        Message: {message}
                        """
                    )
                    sl.success(f"Thank you, {name}! Your message has been sent successfully.")
                except Exception as e:
                    sl.error(f"Failed to send your message. Error: {e}")

# --- GLOBAL STYLES ---
sl.markdown("""
    <style>
        /* General Layout */
        .main { background-color: #1e1e1e; }
        .stButton>button { background-color: #4CAF50; color: white; border-radius: 5px; }
        .stMetric { background-color: #333; border: 1px solid #ddd; border-radius: 5px; padding: 10px; }
        .stMarkdown h1, h2, h3 { color: #ffffff; }

        /* Graph Styling */
        .stPlotlyChart { border: 1px solid #ddd; border-radius: 5px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)