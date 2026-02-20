import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")

uploaded_file = st.file_uploader("Upload file", type=["xlsx", "xls", "csv"], usecols=["hub",	"locn_no",	"cust_no",	"cust_name",	"wage_code",	"std_wage_code",	"position_code",	"assignment_id",	"rank_designation", "current_Gratuity", "current_Bonus", "current_Leave", "current_holiday", "Stats_Holiday", "current_Ex_Gratia"])

if uploaded_file is not None:
    if st.button("Run"):
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, usecols=["hub",	"locn_no",	"cust_no",	"cust_name",	"wage_code",	"std_wage_code",	"position_code",	"assignment_id",	"rank_designation", "current_Gratuity", "current_Bonus", "current_Leave", "current_holiday", "Stats_Holiday", "current_Ex_Gratia"])
        else:
            df = pd.read_excel(uploaded_file, usecols=["hub",	"locn_no",	"cust_no",	"cust_name",	"wage_code",	"std_wage_code",	"position_code",	"assignment_id",	"rank_designation", "current_Gratuity", "current_Bonus", "current_Leave", "current_holiday", "Stats_Holiday", "current_Ex_Gratia"])

        df["key"] = df["locn_no"].astype(str) + df["cust_no"].astype(str)
        original=df.copy()
        #df=df[[]]
        df1 = df[(df["current_Gratuity"])== 0]
        df2 = df[(df["current_Bonus"])== 0]
        df3 = df[(df["current_Leave"])== 0]
        df4 = df[(df["current_holiday"])== 0]
        df5 = df[( df["Stats_Holiday"])== 0]
        df6 = df[(df["current_Ex_Gratia"])== 0]

        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            original.to_excel(writer, sheet_name="YourData", index=False)
            df1.to_excel(writer, sheet_name="current_Gratuity", index=False)
            df2.to_excel(writer, sheet_name="current_Bonus", index=False)
            df3.to_excel(writer, sheet_name="current_Leave", index=False)
            df4.to_excel(writer, sheet_name="current_holiday", index=False)
            df5.to_excel(writer, sheet_name="Stats_Holiday", index=False)
            df6.to_excel(writer, sheet_name="current_Ex_Gratia", index=False)

        output.seek(0)

        st.download_button(
            label="Download Output",
            data=output,
            file_name="output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.warning("Please upload a file.")
