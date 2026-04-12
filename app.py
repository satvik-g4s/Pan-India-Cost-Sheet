import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")

# =========================
# HEADER
# =========================
st.title("📊 Finance Reconciliation Tool")
st.markdown("---")

# =========================
# FILE UPLOAD SECTION (TOP)
# =========================
st.header("📁 Upload Input File")

uploaded_file = st.file_uploader("Upload file", type=["xlsx", "xls", "csv"])
st.caption(
    "Required columns: hub, locn_no, cust_no, cust_name, wage_code, std_wage_code, "
    "position_code, assignment_id, rank_designation, current_Gratuity, current_Bonus, "
    "current_Leave, current_holiday, Stats_Holiday, current_Ex_Gratia"
)

st.markdown("---")

# =========================
# RUN BUTTON
# =========================
run = st.button("▶️ Run Processing")

# =========================
# PROCESSING LOG CONTAINER
# =========================
log_container = st.container()

if run:
    if uploaded_file is not None:
        with log_container:
            st.subheader("🧾 Processing Logs")

            st.write("📥 Reading file...")

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, usecols=["hub",	"locn_no",	"cust_no",	"cust_name",	"wage_code",	"std_wage_code",	"position_code",	"assignment_id",	"rank_designation", "current_Gratuity", "current_Bonus", "current_Leave", "current_holiday", "Stats_Holiday", "current_Ex_Gratia"])
        else:
            df = pd.read_excel(uploaded_file, usecols=["hub",	"locn_no",	"cust_no",	"cust_name",	"wage_code",	"std_wage_code",	"position_code",	"assignment_id",	"rank_designation", "current_Gratuity", "current_Bonus", "current_Leave", "current_holiday", "Stats_Holiday", "current_Ex_Gratia"])

        with log_container:
            st.write("🔑 Creating unique keys...")

        df["key"] = df["locn_no"].astype(str) + df["cust_no"].astype(str)

        original=df.copy()

        with log_container:
            st.write("🧹 Structuring data...")

        df=df[["hub",	"locn_no",	"cust_no","key" ,	"cust_name",	"wage_code",	"std_wage_code",	"position_code",	"assignment_id",	"rank_designation", "current_Gratuity", "current_Bonus", "current_Leave", "current_holiday", "Stats_Holiday", "current_Ex_Gratia"]]

        with log_container:
            st.write("📊 Filtering records based on financial conditions...")

        df1 = df[(df["current_Gratuity"])== 0]
        df2 = df[(df["current_Bonus"])== 0]
        df3 = df[(df["current_Leave"])== 0]
        df4 = df[(df["current_holiday"])== 0]
        df5 = df[( df["Stats_Holiday"])== 0]
        df6 = df[(df["current_Ex_Gratia"])== 0]

        with log_container:
            st.write("📦 Preparing Excel output...")

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

        with log_container:
            st.success("✅ Processing completed successfully!")

            st.download_button(
                label="📥 Download Reconciliation Report",
                data=output,
                file_name="output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    else:
        with log_container:
            st.warning("⚠️ Please upload a file before running.")

st.markdown("---")

# =========================
# DOCUMENTATION SECTION
# =========================

# 1. WHAT THIS TOOL DOES
with st.expander("📌 What This Tool Does"):
    st.write("""
This tool analyzes financial components across assignments and identifies records where specific payout components are zero.

It helps finance teams quickly detect:
- Missing payouts
- Potential under-processing
- Exceptions requiring investigation

The tool generates structured Excel outputs for detailed review.
""")

# 2. HOW TO USE
with st.expander("🧭 How to Use"):
    st.write("""
1. Upload the input file (CSV or Excel format)
2. Ensure all required columns are present
3. Click **Run Processing**
4. Wait for logs to confirm completion
5. Download the reconciliation report

No manual calculations are required.
""")

# 3. OUTPUT DETAILS
with st.expander("📊 Output Details"):
    st.write("""
The output Excel file contains multiple sheets:

- **YourData** → Complete dataset
- **current_Gratuity** → Records where gratuity = 0
- **current_Bonus** → Records where bonus = 0
- **current_Leave** → Records where leave = 0
- **current_holiday** → Records where holiday pay = 0
- **Stats_Holiday** → Records where statutory holiday = 0
- **current_Ex_Gratia** → Records where ex-gratia = 0

Each sheet helps isolate specific financial gaps.
""")

# 4. FINANCIAL LOGIC
with st.expander("💰 Financial Logic"):
    st.write("""
This tool follows a rule-based financial filtering approach.

Key Concept:
Records are segmented where specific payout components equal zero.

Typical Interpretation:
- Zero value → Missing or unpaid component
- Non-zero → Processed normally

Variance Concept (General Finance Reference):
Variance = Billed Hours − Performed Hours

Interpretation:
- Positive → Overbilling
- Negative → Underbilling

Special Handling Considerations:
- Missing payout components flagged automatically
- Each financial head evaluated independently
- No aggregation or modification applied

Classification Structure:
Data is organized across:
HUB → Location → Customer → Assignment

This enables structured financial review at multiple levels.

Output Purpose:
- Identify gaps quickly
- Support audit checks
- Assist in reconciliation workflows
""")
