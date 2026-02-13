import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")

uploaded_file = st.file_uploader("Upload file", type=["xlsx", "xls", "csv"])

if st.button("Run"):
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df2 = df[
            (
                df["current_Gratuity"]
                + df["current_Bonus"]
                + df["current_Leave"]
                + df["current_holiday"]
                + df["Stats_Holiday"]
                + df["current_Ex_Gratia"]
            )
            == 0
        ]

        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="YourData", index=False)
            df2.to_excel(writer, sheet_name="Filtered", index=False)

        output.seek(0)

        st.download_button(
            label="Download Output",
            data=output,
            file_name="output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.warning("Please upload a file.")
