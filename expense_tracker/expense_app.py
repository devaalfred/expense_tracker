import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

st.title('💸EXPENSE TRACKER📱')
st.header('Welcome to EXPENSE TRACKER💸')
st.write("Built by Deva🤖")
st.markdown("___")

#setting page config
st.set_page_config(page_title="EXPENSE TRACKER",page_icon="💸",layout="centered")

#File for storing the data
file_path="expenses.csv"
#if the file doesn't exist we want to create it
if not os.path.exists(file_path):#if not means if the file wasn't created for the 1st time
    df = pd.DataFrame(columns=['Date','Category','Description','Amount'])
    df.to_csv(file_path, index=False)
#load the data
df = pd.read_csv(file_path)

st.sidebar.title('NAVIGATION')  #creating a sidebar,radio created clickable options
page= st.sidebar.radio("GO TO",["ADD EXPENSE","VIEW EXPENSE","ANALYTICS"])#it stores selected options

#add new expense
if page == "ADD EXPENSE":
    st.header("➕ADD NEW EXPENSE")
    date = st.date_input("DATE")
    category = st.selectbox('CATEGORY', ["FOOD🍔", "TRAVEL✈️", "SHOPPING👜", "BILLS💴", "OTHER"])
    description = st.text_input("DESCRIPTION")
    amount = st.number_input("AMOUNT", min_value=0.0, format="%.2f")  # format shows all values with decimal places
    # after entering the expenses i provided a button 'add expense' when that is clicked the expense will be added to the dataframe

    if st.button("ADD EXPENSE"):
        new_expense = pd.DataFrame({'Date': [date],
                                    'Category': [category],
                                    'Description': [description],
                                    'Amount': [amount]})
        df = pd.concat([df, new_expense], ignore_index=True)  # add the new expense to the existing data
        df.to_csv(file_path, index=False)  # that ignore index for ignoring the old index and maintaining proprly
        st.success("EXPENSE ADDED SUCCESSFULLY✅")
        st.markdown("___")

# show existing data
elif page == "VIEW EXPENSE":
    st.header("📋ALL EXPENSES")
    st.dataframe(df)

    st.write("💰TOTAL SPENDINGS= RS", df["Amount"].sum())
    st.markdown("___")

elif page=="ANALYTICS":
    if not df.empty:
        st.header("📊EXPENSES BY CATEGORY")
        category_summary = df.groupby("Category")["Amount"].sum()
        # bar chart present in streamlit so making use of it
        st.subheader("BAR CHART📊")
        st.bar_chart(category_summary)
        # for pie chart im using matplotlib

        st.subheader("💹PIE CHART")
        fig, ax = plt.subplots(figsize=(4,2))  # it creates a matplotlib figure
        ax.pie(category_summary,  # creates a pie chart
               labels=category_summary.index,  # name of each pie
               autopct='%1.1f%%',
               textprops={'fontsize':3})  # shows percentage of the chart
        ax.set_title("EXPENSES BY CATEGORY",fontsize=5)  # giving a title
        st.pyplot(fig)

    else:  # if there is no data im telling to add the data
        st.info("ADD SOME EXPENSES TO SEE THE ANALYTICS!")
        st.markdown("___")

