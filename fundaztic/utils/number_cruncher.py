import calendar
import pandas as pd
from constants import FilePaths, FileNames

# Global variables.
today = pd.Timestamp.today()
current_year = today.year
current_month = today.month
current_day = today.day
max_days_current_month = calendar.monthrange(current_year, current_month)[1]
max_days_previous_month = calendar.monthrange(
    current_year, current_month - 1 if current_month > 1 else 12
)[1]
normalized_day = int(current_day / max_days_current_month * max_days_previous_month)


# Helper function to sum columns for a given year-month
def _sum_for_month(df, year, month, normalized=False):
    if normalized:
        mask = (
            (df["Distribution Date"].dt.year == year)
            & (df["Distribution Date"].dt.month == month)
            & (df["Distribution Date"].dt.day <= normalized_day)
        )
    else:
        mask = (df["Distribution Date"].dt.year == year) & (
            df["Distribution Date"].dt.month == month
        )
    subset = df.loc[mask]
    net_interest = subset["Net Interest (RM)"].sum()
    principal = subset["Principal (RM)"].sum()
    fees = subset["Platform Fee (RM)"].sum() + subset["SST (RM)"].sum()
    return net_interest, principal, fees


def aggregate_received_distribution():
    file = f"{FilePaths.download_dir}/{FileNames.received_distribution_xls}"
    df = pd.read_excel(file, skiprows=4)

    df["Distribution Date"] = pd.to_datetime(df["Distribution Date"], dayfirst=True)
    df["Net Interest (RM)"] = df["Interest (RM)"] - df["Platform Fee (RM)"]

    # Current month (MTD)
    mtd_net_interest, mtd_principal, mtd_fees = _sum_for_month(
        df, current_year, current_month
    )

    # Previous month Normalized.
    prev_month = today - pd.DateOffset(months=1)
    prev_net_interest, prev_principal, prev_fees = _sum_for_month(
        df, prev_month.year, prev_month.month, normalized=True
    )

    # m1, m2, m3 - 1, 2, and 3 months ago (full months)
    m1 = today - pd.DateOffset(months=1)
    m2 = today - pd.DateOffset(months=2)
    m3 = today - pd.DateOffset(months=3)

    m1_net_interest, m1_principal, m1_fees = _sum_for_month(df, m1.year, m1.month)
    m2_net_interest, m2_principal, m2_fees = _sum_for_month(df, m2.year, m2.month)
    m3_net_interest, m3_principal, m3_fees = _sum_for_month(df, m3.year, m3.month)

    # Format as strings with 2 decimal places
    result = {
        "mtd_net_interest": f"{mtd_net_interest:.2f}",
        "mtd_principal": f"{mtd_principal:.2f}",
        "mtd_fees": f"{mtd_fees:.2f}",
        "prev_net_interest": f"{prev_net_interest:.2f}",
        "prev_principal": f"{prev_principal:.2f}",
        "prev_fees": f"{prev_fees:.2f}",
        "m1_net_interest": f"{m1_net_interest:.2f}",
        "m1_principal": f"{m1_principal:.2f}",
        "m1_fees": f"{m1_fees:.2f}",
        "m2_net_interest": f"{m2_net_interest:.2f}",
        "m2_principal": f"{m2_principal:.2f}",
        "m2_fees": f"{m2_fees:.2f}",
        "m3_net_interest": f"{m3_net_interest:.2f}",
        "m3_principal": f"{m3_principal:.2f}",
        "m3_fees": f"{m3_fees:.2f}",
    }

    return result
