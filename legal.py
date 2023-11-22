import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
import base64
import datetime

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("Invalid Credentials")
        return False
    else:
        # Password correct.
        return True

if check_password():

    # Define your Google Sheets credentials JSON file (replace with your own)
    credentials_path = 'legal-corporate-019720d30928.json'
        
    # Authenticate with Google Sheets using the credentials
    credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://spreadsheets.google.com/feeds'])
        
    # Authenticate with Google Sheets using gspread
    gc = gspread.authorize(credentials)
        
    # Your Google Sheets URL
    url = "https://docs.google.com/spreadsheets/d/1OGtNQnciAJLJiOmKlfvuZWar0zFwCjA77GwvBe5BF9Q/edit#gid=0"
        
    # Open the Google Sheets spreadsheet
    worksheet = gc.open_by_url(url).worksheet("legal")
    worksheet2 = gc.open_by_url(url).worksheet("maturity")


    # Add a sidebar
    st.sidebar.image('corplogo.PNG', use_column_width=True)
    st.sidebar.markdown("Navigation Pane")
    
    # Main Streamlit app code
    def main():
    
        # Create a sidebar to switch between views
        view = st.sidebar.radio("Select", ["New Update", "Records"])
    
        if view == "New Update":
                # Add the dashboard elements here
            st.subheader("AUCTIONEERS TRACKER & APPROVAL SHEET")
        
            # Create form fields for user input   
            proclamation_date = st.date_input("Date Proclamation Received") 
        
            negotiation_initiated = st.date_input("Date Negotiating Initiated")
        
            decretal_amount = st.number_input("Decretal Amount")
        
            auctioneer_fee = st.number_input("Auctioneer Fees")       
                   
            persons_negotiating = st.selectbox("Officers Negotiating:",["Samuel Kangi", "Augustus Kioko"])
        
            final_negotiated_amount = st.number_input("Final Negotiated Amount")
        
            negotiation_date_concluded = st.date_input("Date Negotiation Concluded In Legal")  
        
            checked_by = st.selectbox("Checked By:",["Samuel Kangi", "Augustus Kioko"])
        
            approved_by = st.selectbox("Approved By:",["Samuel Kangi", "Augustus Kioko"])
        
            payment_processed_date = st.date_input("Date Payment Processed and Passed to Finance")  
        
        
        
                # Check if the user has entered data and submitted the form
            if st.button("Submit"):
                
                # Create a new row of data to add to the Google Sheets spreadsheet
                new_data = [proclamation_date, negotiation_initiated, decretal_amount, auctioneer_fee, persons_negotiating, final_negotiated_amount, negotiation_date_concluded, checked_by, approved_by, payment_processed_date]
        
                # Append the new row of data to the worksheet
                worksheet.append_row(new_data) 
        
                st.success("Data submitted successfully!")
        
        
        elif view == "Records":
            # Show the saved DataFrame here
            data = worksheet.get_all_values()
            headers = data[0]
            data = data[1:]
            df = pd.DataFrame(data, columns=headers)  # Convert data to a DataFrame
            st.subheader("RECORDS")
        
        
            edited_df = st.data_editor(df)
        
            # Add a button to update Google Sheets with the changes
            if st.button("Update Google Sheets"):
                worksheet.clear()  # Clear the existing data in the worksheet
                worksheet.update([edited_df.columns.tolist()] + edited_df.values.tolist())
        
            # Add a button to download the filtered data as a CSV
            if st.button("Download CSV"):
                csv_data = edited_df.to_csv(index=False, encoding='utf-8')
                b64 = base64.b64encode(csv_data.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="auctioneer_report.csv">Download CSV</a>'
                st.markdown(href, unsafe_allow_html=True)  

        elif view == "Maturity":
            data = worksheet2.get_all_values()
            headers = data[0]
            data = data[1:]
    
            df3 = pd.DataFrame(data, columns = headers)

            unique_year = df['Year'].unique()
    
            # Create a dropdown to select a month with "All Payments" option
            selected_year = st.selectbox("Filter by Year:", ["All Payments"] + list(unique_year))
             
             # Get the unique reviewer names from the DataFrame
            unique_month = df['Month Name'].unique()
    
            # Create a dropdown to select a month with "All Payments" option
            selected_month = st.selectbox("Filter by Month:", ["All Payments"] + list(unique_month))

            # Create two columns
            col1, col2 = st.beta_columns(2)
            
            # Dropdown for Year selection
            with col1:
                selected_year = st.selectbox("Filter by Year:", ["All Payments"] + list(unique_year))
            
            # Dropdown for Month selection
            with col2:
                selected_month = st.selectbox("Filter by Month:", ["All Payments"] + list(unique_month))
            
            # Apply filters to the DataFrame
            filtered_df = df.copy()
            
            if selected_year != "All Payments":
                filtered_df = filtered_df[filtered_df['Year'] == int(selected_year)]
            
            if selected_month != "All Payments":
                filtered_df = filtered_df[filtered_df['Month Name'] == selected_month]
            
            # Display the filtered DataFrame
            st.write("Filtered DataFrame:")
            st.write(filtered_df)

            
    
                

    

        
             








             

    if __name__ == "__main__":
        main()







