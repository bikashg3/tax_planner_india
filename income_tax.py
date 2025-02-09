import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Income Tax Planner - India",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Updated Engaging Modern Light Theme CSS
st.markdown(
    """
    <style>
        /* Main theme colors */
        :root {
            --primary-color: #007BFF;
            --secondary-color: #6C757D;
            --background-light: #f8f9fa;
            --card-bg: #ffffff;
            --text-color: #212529;
        }
        
        /* Global styles */
        .stApp {
            background-color: var(--background-light);
            color: var(--text-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        # /* Custom card container */
        # .custom-card {
        #     background-color: var(--card-bg);
        #     padding: 2rem;
        #     border-radius: 1rem;
        #     box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        #     margin: 1rem 0;
        #     transition: transform 0.3s ease, box-shadow 0.3s ease;
        # }
        # .custom-card:hover {
        #     transform: translateY(-5px);
        #     box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        # }

        .custom-card {
            background-color: var(--card-bg);
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;

            /* Font styling */
            font-size: 1.75rem; /* h3 size */
            text-align: center; /* Center align text */
            font-weight: bold; /* Match h3 weight */
            color: #1585fc; /* Default Streamlit blue */
        }

        .custom-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        }

        
        /* Input fields */
        .stNumberInput input {
            background-color: #fff;
            color: var(--text-color);
            border: 1px solid #ced4da;
            border-radius: 0.375rem;
            font-size: 1rem;
            padding: 0.375rem 0.75rem;
            transition: border-color 0.3s ease;
        }
        .stNumberInput input:focus {
            border-color: var(--primary-color);
        }
        
        /* Radio buttons */
        .stRadio label {
            color: var(--text-color) !important;
            font-size: 1rem;
        }
        
        /* Metrics */
        .metric-card {
            background-color: var(--card-bg);
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid var(--primary-color);
            margin: 0.5rem 0;
        }
        
        /* Headers and text */
        h1, h2, h3 {
            color: var(--primary-color) !important;
            font-weight: 600;
        }
        
        /* Table styling */
        .dataframe {
            background-color: var(--card-bg) !important;
            border-radius: 0.5rem;
        }
        .dataframe th {
            background-color: var(--primary-color) !important;
            color: #fff !important;
            padding: 0.75rem;
        }
        .dataframe td {
            padding: 0.75rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def format_currency(amount):
    """Format amount in Indian currency format"""
    return f"₹{amount:,.2f}"

def calculate_tax_breakdown(income, category):
    """
    Calculate the tax breakdown using the new tax regime rules.
    Salaried individuals benefit from a higher basic exemption threshold.
    """
    # Basic exemption threshold based on employment category
    basic_exemption = 1275000 if category == "Salaried" else 1200000

    # Tax slabs definition
    slabs = [
        (0, 400000, 0),
        (400000, 800000, 0.05),
        (800000, 1200000, 0.10),
        (1200000, 1600000, 0.15),
        (1600000, 2000000, 0.20),
        (2000000, 2400000, 0.25),
        (2400000, float("inf"), 0.30),
    ]

    # Income within the basic exemption threshold is tax-free
    if income <= basic_exemption:
        return 0, []

    breakdown = []
    total_tax = 0
    remaining_income = income
    taxable_income = income - basic_exemption

    # Calculate tax for each applicable slab
    for lower, upper, rate in slabs:
        if remaining_income <= 0:
            break

        # Determine income falling within the current slab range
        slab_income = min(remaining_income, upper - lower)
        if slab_income > 0:
            slab_tax = slab_income * rate
            total_tax += slab_tax
            breakdown.append({
                "Income Range": f"₹{lower:,} - {'∞' if upper == float('inf') else f'₹{upper:,}'}",
                "Rate": f"{rate*100}%",
                "Taxable Amount": slab_income,
                "Tax": slab_tax,
            })
            remaining_income -= slab_income

    # The total tax is limited to the taxable income (income above the exemption)
    return min(total_tax, taxable_income), breakdown

# Main Header
st.markdown(
    """
    <div style='text-align: center; padding: 2rem 0;'>
        <h1>Income Tax Planner - India</h1>
        <h3 style='color: var(--secondary-color);'>Strategize Your Tax Liability for FY 2025-26 (AY 2026-27)</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

# Layout: Two Columns
col1, col2 = st.columns([1, 2])

# Input Section
with col1:
    st.markdown("<div class='custom-card'>Enter Your Annual Income Details", unsafe_allow_html=True)
    #st.subheader("Enter Your Annual Income Details")

    income = st.number_input(
        "Annual Income (₹)",
        min_value=0,
        value=1200000,
        step=10000,
        format="%d",
        help="Enter your total annual income (before deductions).",
    )

    category = st.radio(
        "Employment Category",
        ["Salaried", "Others"],
        horizontal=True,
        help="Salaried individuals benefit from a higher basic exemption threshold (up to ₹12.75 Lakhs).",
    )

    exemption_limit = "₹12.75 Lakhs" if category == "Salaried" else "₹12 Lakhs"
    st.markdown(
        f"""
        <div style='background-color: #e9ecef; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;'>
            <p style='margin: 0;'><strong>Note:</strong> Enjoy a tax exemption up to {exemption_limit}.</p>
            <p style='margin: 5px 0 0 0; font-size: 0.9em; color: var(--secondary-color);'>
                This benefit applies under the new tax regime for FY 2025-26.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Calculate Tax Details
tax, tax_breakdown = calculate_tax_breakdown(income, category)
health_education_cess = tax * 0.04
total_tax = tax + health_education_cess
disposable_income = income - total_tax
monthly_takeaway = disposable_income / 12 if income > 0 else 0
effective_tax_rate = (total_tax / income) * 100 if income > 0 else 0

# Results Section
with col2:
    st.markdown("<div class='custom-card'>Tax Summary & Analysis", unsafe_allow_html=True)
    #st.subheader("Tax Summary & Analysis")

    # Display Key Metrics in two columns
    metrics_col1, metrics_col2 = st.columns(2)

    with metrics_col1:
        st.metric("Total Tax Payable", format_currency(total_tax))
        st.metric("Basic Tax Amount", format_currency(tax))
        st.metric("Health & Education Cess (4%)", format_currency(health_education_cess))

    with metrics_col2:
        st.metric("Net Disposable Income", format_currency(disposable_income))
        st.metric("Monthly Takeaway Income", format_currency(monthly_takeaway))
        st.metric("Effective Tax Rate", f"{effective_tax_rate:.2f}%")

    # Tax Breakdown Table
    if tax_breakdown:
        st.subheader("Detailed Tax Breakdown")
        df = pd.DataFrame(tax_breakdown)
        st.table(df)

    st.markdown("</div>", unsafe_allow_html=True)

# Important Information & Disclaimers Section
st.markdown("<div class='custom-card'>Important Information & Disclaimers", unsafe_allow_html=True)
#st.subheader("Important Information & Disclaimers")
st.markdown(
    """
- **Overview:** This tax planner is designed to provide an estimate of your tax liability under the new tax regime for FY 2025-26. The tool assumes a basic exemption threshold of **₹12.75 Lakhs** for salaried individuals and **₹12 Lakhs** for others. Income up to these limits remains tax-free.
  
- **Tax Slab Structure:** For income exceeding the exemption threshold, the following progressive tax rates are applied:
  - **Up to ₹4,00,000:** 0%
  - **₹4,00,001 to ₹8,00,000:** 5%
  - **₹8,00,001 to ₹12,00,000:** 10%
  - **₹12,00,001 to ₹16,00,000:** 15%
  - **₹16,00,001 to ₹20,00,000:** 20%
  - **₹20,00,001 to ₹24,00,000:** 25%
  - **Above ₹24,00,000:** 30%
  
- **Additional Cess:** A **4% Health & Education Cess** is levied on the computed tax amount.

- **Usage Note:** This tool does not account for other deductions, exemptions, or specific individual circumstances. It is intended solely for preliminary tax planning purposes.

- **Disclaimer:** For personalized advice and detailed tax planning, please consult a certified tax professional.
    """
)
st.markdown("</div>", unsafe_allow_html=True)
