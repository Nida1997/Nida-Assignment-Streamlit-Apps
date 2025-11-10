import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set the title and initial description for the app
st.title("📊 Nida Fathinah's EDA App")
st.write("Upload a CSV file to begin Exploratory Data Analysis.")

# 1. File Uploader Component
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the data into a Pandas DataFrame
    df = pd.read_csv(uploaded_file)
    
    st.header("1. Data Overview")
    st.write(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Display the first few rows
    st.subheader("First 5 Rows")
    st.dataframe(df.head())
    
    # Display Summary Statistics
    st.subheader("2. Summary Statistics")
    st.dataframe(df.describe(include='all'))

    # 3. Simple Visualization (Histogram)
    # Identify numerical columns for plotting
    numerical_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    if numerical_cols:
        st.header("3. Data Visualization")
        
        # User selects the column to plot
        selected_column = st.selectbox(
            "Select a numerical column for a Histogram:", 
            numerical_cols
        )
        
        # Create the Matplotlib plot
        fig, ax = plt.subplots()
        # Use .dropna() to handle any missing values before plotting
        ax.hist(df[selected_column].dropna(), bins=20, edgecolor='black')
        ax.set_title(f'Distribution of {selected_column}')
        ax.set_xlabel(selected_column)
        
        # Display the plot in Streamlit
        st.pyplot(fig)
    else:
        st.info("No numerical columns found for plotting distributions.")

st.markdown("---")
st.caption("Powered by Streamlit | Assignment EDA App by Nida Fathinah")