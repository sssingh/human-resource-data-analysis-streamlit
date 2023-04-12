"""All app-specific plots are implemented here"""

import plotly.express as px
import plotly.io as io
from pandas import DataFrame
from plotly.graph_objects import Figure
from config import plot_config


# setup app-wide plotly theme
io.templates.default = plot_config.theme


###
### Summary tab plots
###
def plot_age_hist(df: DataFrame) -> Figure:
    fig = px.histogram(
        data_frame=df,
        x="Age",
        marginal="violin",
        title="Employee's age distribution overall",
        color_discrete_sequence=plot_config.cat_color_map,
    )
    return fig


def plot_age_marital_status_pie(df: DataFrame) -> Figure:
    df_group = (
        df.groupby("MaritalStatus", as_index=False)
        .size()
        .sort_values(by="size", ascending=True)
    )
    fig = px.pie(
        data_frame=df_group,
        names="MaritalStatus",
        values="size",
        color="MaritalStatus",
        hole=0.7,
        title="Employee count by marital-status",
        color_discrete_sequence=plot_config.cat_color_map,
    ).update_traces(textfont_color="white")
    return fig


def plot_age_marital_status_box(df: DataFrame) -> Figure:
    fig = px.box(
        data_frame=df,
        x="MaritalStatus",
        y="Age",
        color="MaritalStatus",
        title="Employee's age distribution by marital-status",
        color_discrete_sequence=plot_config.cat_color_map,
    )
    return fig


def plot_age_gender_box(df: DataFrame) -> Figure:
    fig = px.box(
        data_frame=df,
        x="Gender",
        y="Age",
        color="Gender",
        title="Employee's age distribution by gender",
        color_discrete_sequence=plot_config.cat_color_map,
    )
    return fig


def plot_dept_gender_count_sunburst(df: DataFrame) -> Figure:
    df_group = (
        df.groupby(["Department", "Gender"], as_index=False)
        .size()
        .assign(Top="Company")
    )
    fig = px.sunburst(
        data_frame=df_group,
        path=["Top", "Department", "Gender"],
        values="size",
        color_discrete_sequence=px.colors.qualitative.T10,
        title="Employee count in each department<br>segmented by gender",
    )
    fig.update_traces(
        textfont_color="white",
        textinfo="label+percent parent",
        textfont_size=18,
    )
    fig.update_layout(
        margin=dict(t=20, l=0, r=0, b=0),
        autosize=False,
        height=700,
    )

    return fig


def plot_dept_curr_mgr_scatter(df: DataFrame) -> Figure:
    df_group = (
        df.groupby("Department")["YearsWithCurrManager"]
        .mean()
        .to_frame()
        .reset_index()
        .sort_values(by="YearsWithCurrManager", ascending=False)
    )
    fig = px.scatter(
        data_frame=df_group,
        x="YearsWithCurrManager",
        y="Department",
        color="Department",
        size="YearsWithCurrManager",
        title="Avg number of years with current manager",
    )
    return fig


def plot_tot_work_exp_bar(df):
    tot_emp = len(df)
    df_group = df.groupby("WorkExperience", as_index=False).size()
    df_group["size"] = df_group["size"] / tot_emp * 100
    fig = px.bar(
        data_frame=df_group.sort_values(by="size", ascending=False),
        x="size",
        y="WorkExperience",
        color="WorkExperience",
        color_discrete_sequence=plot_config.cat_color_map,
    ).update_traces(
        text="size",
        texttemplate="%{x:.1f}%",
        textposition="auto",
        textfont_color="white",
    )
    return fig


def plot_cmp_work_exp_scatter(df, annot_text):
    fig = px.scatter(
        data_frame=df,
        x="TotalWorkingYears",
        y="YearsAtCompany",
        size="PctAtCompany",
        color="PctAtCompany",
        opacity=0.6,
        color_continuous_scale=plot_config.cont_color_map,
    )
    fig.add_annotation(
        x=0.1,
        y=35,
        xref="paper",
        yref="y",
        text=annot_text,
        align="left",
        showarrow=False,
        font=dict(family="Arial", size=14, color="#ffffff"),
        bordercolor="#4c78a8",
        borderwidth=1,
        borderpad=4,
        bgcolor="#4c78a8",
        opacity=0.7,
    )

    return fig


###
### Capacity tab plots
###
def plot_promotion_donut(df):
    df_group = (
        df["ToBePromoted"]
        .value_counts()
        .to_frame()
        .reset_index()
        .rename({"ToBePromoted": "Count", "index": "Promotion"}, axis=1)
    )
    fig = px.pie(
        df_group,
        names="Promotion",
        values="Count",
        hole=0.6,
        color_discrete_sequence=plot_config.cat_color_map,
        title="Company wide promotion",
    )
    fig.update_layout(
        legend_title_text="Promotion?",
        margin=dict(t=45, l=0, r=0, b=0),
    )
    fig.update_traces(pull=[0.1, 0])
    return fig


def plot_retrench_donut(df):
    df_group = (
        df["ToBeRetrenched"]
        .value_counts()
        .to_frame()
        .reset_index()
        .rename({"ToBeRetrenched": "Count", "index": "Retrench"}, axis=1)
    )
    fig = px.pie(
        df_group,
        names="Retrench",
        values="Count",
        hole=0.6,
        color_discrete_sequence=plot_config.cat_color_map_r,
        title="Company wide retrenchment",
    )
    fig.update_layout(
        legend_title_text="Retrench?",
        margin=dict(t=45, l=0, r=0, b=0),
    )
    fig.update_traces(pull=[0.1, 0])
    return fig


def plot_dept_promo_bar(df):
    fig = px.bar(
        data_frame=df,
        x="Department",
        y="PromotePct",
        color="ToBePromoted",
        barmode="group",
        color_discrete_sequence=plot_config.cat_color_map,
        title="To be promoted<br>in each department",
    )
    fig.update_traces(
        texttemplate="%{y:.1f}%",
        textposition="auto",
        textfont_color="white",
    )
    return fig


def plot_dept_retrench_bar(df):
    df_group = df
    fig = px.bar(
        data_frame=df_group,
        x="Department",
        y="RetrenchPct",
        color="ToBeRetrenched",
        barmode="group",
        color_discrete_sequence=plot_config.cat_color_map_r,
        title="To be retrenched<br>in each department",
    )
    fig.update_traces(
        texttemplate="%{y:.1f}%",
        textposition="auto",
        textfont_color="white",
    )
    return fig
