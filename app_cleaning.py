import streamlit as st
import pandas as pd
import numpy as np

st.title("🧹 Nida Fathinah's Data Cleaning App")
st.write("Upload a CSV file to inspect and perform cleaning operations.")

# 1. File Uploader
uploaded_file = st.file_uploader("Choose a CSV file to clean", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    original_shape = df.shape
    
    st.subheader("Original Data Preview")
    st.dataframe(df.head())

    # --- MISSING VALUES SECTION ---
    st.header("1. Handling Missing Values (NaN)")
    
    # Calculate initial missing values
    missing_count = df.isnull().sum().sum()
    
    if missing_count > 0:
        st.warning(f"Total missing values found: **{missing_count}** out of {df.size} cells.")
        
        # User selects cleaning method
        cleaning_method = st.radio(
            "Choose a method to handle NaN values:",
            ('Do Nothing', 'Drop Rows with Missing Values', 'Fill Numerical Missing Values')
        )

        if cleaning_method == 'Drop Rows with Missing Values':
            # Drop rows with any NaN values
            df_cleaned = df.dropna()
            rows_dropped = original_shape[0] - df_cleaned.shape[0]
            st.success(f"Removed **{rows_dropped}** rows with missing values.")
            df = df_cleaned.copy()
            
        elif cleaning_method == 'Fill Numerical Missing Values':
            # Target numerical columns for imputation
            numerical_cols = df.select_dtypes(include=np.number).columns
            
            fill_value_option = st.selectbox(
                "Select fill method for numerical columns:",
                ('Mean', 'Median', 'Specific Value (e.g., 0)')
            )
            
            if fill_value_option == 'Mean':
                df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].mean())
                st.success("Missing numerical values filled with the **Mean**.")
            elif fill_value_option == 'Median':
                df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())
                st.success("Missing numerical values filled with the **Median**.")
            else:
                # Allows user to input a specific value
                specific_value = st.number_input("Enter a value to fill NaN (e.g., 0):", value=0, key="fill_val")
                df[numerical_cols] = df[numerical_cols].fillna(specific_value)
                st.success(f"Missing numerical values filled with **{specific_value}**.")
    else:
        st.info("Great! No missing values detected in the initial upload.")

    # --- DUPLICATES SECTION ---
    st.header("2. Handling Duplicates")
    duplicate_rows = df.duplicated().sum()
    
    if duplicate_rows > 0:
        st.warning(f"Total duplicate rows found: **{duplicate_rows}**.")
        
        if st.checkbox("Remove all duplicate rows (keeping the first occurrence)"):
            df = df.drop_duplicates(keep='first')
            st.success(f"Successfully removed **{duplicate_rows}** duplicate rows.")
    else:
        st.info("No duplicate rows found.")

    # --- FINAL DATA ---
    st.header("3. Final Cleaned Data & Download")
    st.dataframe(df)
    
    # Download button for the processed data
    st.download_button(
        label="Download Cleaned Data as CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='cleaned_data_nida.csv',
        mime='text/csv',
    )
    
    st.info(f"Final Data Shape: {df.shape[0]} rows, {df.shape[1]} columns")

st.markdown("---")
st.caption("Powered by Streamlit | Data Cleaning App by Nida Fathinah")