"""All app-specific data and disk-IO related functionality implemented here"""

import pandas as pd
import streamlit as st
from pandas import DataFrame


@st.cache_data
def load_transform(file) -> DataFrame:
    """Load the raw data and prepare/transform it"""
    ###
    ### Read raw data
    ###

    df = pd.read_csv(file)

    ###
    ### Handle missing data (None in this case)
    ###

    ###
    ### Feature Engineering
    ###
    ## Create a new column - ToBePromoted
    # if yrs since last promotion >= 10 yrs and performance rating is > 2
    # then promote else not to be promoted
    df.loc[
        (
            (df["YearsSinceLastPromotion"] >= 10) & (df["PerformanceRating"] > 2),
            "ToBePromoted",
        )
    ] = "Yes"
    df["ToBePromoted"].fillna("No", inplace=True)

    ## Create a new column - ToBeRetrenched
    # 1) If years in current-role is between 3 to 10 years and performance-rating == 1
    # 2) If years in current-role is >= 10 years and performance-rating < 3
    # 3) Not-to-be-promoted or left the company
    df.loc[
        df.query(
            "(YearsInCurrentRole >= 10 and PerformanceRating < 3) or "
            + "(2 < YearsInCurrentRole < 10 and PerformanceRating == 1) "
            + "and Attrition=='No' and ToBePromoted=='No'"
        ).index,
        "ToBeRetrenched",
    ] = "Yes"
    df["ToBeRetrenched"].fillna("No", inplace=True)

    ## Create a new column - AgeBuckets
    # to divide TotalWorkExperience into bins, to be used in viz
    df["WorkExperience"] = pd.cut(
        df["TotalWorkingYears"],
        bins=8,
        labels=[
            "5 Yrs",
            "10 Yrs",
            "15 Yrs",
            "20 Yrs",
            "25 Yrs",
            "30 Yrs",
            "35 Yrs",
            "40 Yrs",
        ],
    )

    ## Create a new column - %YrsAtCompany
    df["PctAtCompany"] = (df["YearsAtCompany"] / df["TotalWorkingYears"]).fillna(
        0
    ) * 100

    return df


@st.cache_data
def get_dept_stats_df(df: DataFrame):
    """Calculate various stats for each department and returns results in a DataFrame"""
    # Prepare a df with department as index and mean MonthlyIncome, mean PercentSalaryHike,
    # mean TotalWorkingYears, mean YearsAtCompany, mean TrainingTimesLastYear
    df_dept = (
        df.groupby("Department")[
            [
                "MonthlyIncome",
                "PercentSalaryHike",
                "TotalWorkingYears",
                "YearsAtCompany",
                "TrainingTimesLastYear",
            ]
        ]
        .mean()
        .round(2)
    )
    # Prepare a df with department as index and total count of OverTime (Yes) for each dept
    df_ot = (
        df.query("OverTime == 'Yes'")
        .groupby("Department")["OverTime"]
        .count()
        .to_frame()
    )
    # Join both df to create a single df --> this to be shown with pandas gradients
    df_dept_stat = df_dept.join(df_ot, how="inner").reset_index()
    return df_dept_stat


@st.cache_data
def get_gender_count(df: DataFrame):
    """Calculates employee total count and for each gender,
    returns count and percentage as result"""
    df_gender = df.groupby("Gender").size()
    male_emp_cnt = df_gender["Male"]
    female_emp_cnt = df_gender["Female"]
    tot_emp_cnt = male_emp_cnt + female_emp_cnt
    male_pct = round((male_emp_cnt / tot_emp_cnt) * 100, 2)
    female_pct = round((female_emp_cnt / tot_emp_cnt) * 100, 2)
    return tot_emp_cnt, male_emp_cnt, female_emp_cnt, male_pct, female_pct


@st.cache_data
def get_promo_count(df: DataFrame):
    """Calculates number of employees due for promotion,
    returns count and percentage as result"""
    df_promo = df.groupby("ToBePromoted").size()
    promo_cnt = df_promo["Yes"]
    not_promo_cnt = df_promo["No"]
    tot_emp_cnt, _, _, _, _ = get_gender_count(df)
    promo_pct = round((promo_cnt / tot_emp_cnt) * 100, 2)
    not_promo_pct = round((not_promo_cnt / tot_emp_cnt) * 100, 2)
    return promo_cnt, not_promo_cnt, promo_pct, not_promo_pct


@st.cache_data
def get_retrench_count(df: DataFrame):
    """Calculates number of employees due for retrenchment,
    returns count and percentage as result"""
    df_retrench = df.groupby("ToBeRetrenched").size()
    retrench_cnt = df_retrench["Yes"]
    not_retrench_cnt = df_retrench["No"]
    tot_emp_cnt, _, _, _, _ = get_gender_count(df)
    retrench_pct = round((retrench_cnt / tot_emp_cnt) * 100, 2)
    not_retrench_pct = round((not_retrench_cnt / tot_emp_cnt) * 100, 2)
    return retrench_cnt, not_retrench_cnt, retrench_pct, not_retrench_pct


@st.cache_data
def get_pct_at_cmp(df):
    pct_at_cmp = {
        "between 0-25%": len(df.query("PctAtCompany <= 25")) / len(df),
        "between 26-50%": len(df.query("PctAtCompany > 25 and PctAtCompany <= 50"))
        / len(df),
        "between 51-75%": len(df.query("PctAtCompany > 50 and PctAtCompany <= 75"))
        / len(df),
        "between 76-100%": len(df.query("PctAtCompany > 75 and PctAtCompany <= 100"))
        / len(df),
    }
    return pct_at_cmp


# do not cache, need to read file from disk
def df_to_csv(file: str) -> bytes:
    """Read file again and return as as a csv"""
    df = pd.read_csv(file)
    return df.to_csv(index=False).encode("utf-8")
