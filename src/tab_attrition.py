"""Attrition tab rendering functionality"""

import pandas as pd
import streamlit
import utils
import data
import plots


###
### render the capacity page
###
def render(df: pd.DataFrame):
    # Show KPI & plots
    __build_attrition_plots(df)


###
### module's internal functions
###
def __build_attrition_plots(df):
    with streamlit.expander("Analysis: Employee Attrition...", expanded=True):
        utils.show_questions(
            [
                "* Do we have attrition rate higher than 10%?",
                "* What are the factors directly contributes to attrition?",
            ]
        )
        utils.sep()
        ### gather attrition statistics
        attrition_stats = data.get_attrition_stats(df)

        ### overall, male and female attrition rates
        with streamlit.container():
            (
                c1_col1,
                c1_col2,
                c1_col3,
            ) = streamlit.columns(3)
            with c1_col1:
                attr_tot = attrition_stats["CompanyWide"]["Total Attrition"]
                attr_pct = attrition_stats["CompanyWide"]["Attrition Rate"]
                utils.render_card(
                    key="attrition_card1",
                    title="Overall<br>Attrition",
                    value=attr_tot,
                    secondary_text=f" ({attr_pct})%",
                    icon="fa-sharp fa-solid fa-venus-mars fa-xs",
                    progress_value=int(attr_pct),
                    progress_color="red",
                )
            with c1_col2:
                male_attr_tot = attrition_stats.get("Male", {}).get(
                    "Total Attrition", 0
                )
                male_attr_pct = attrition_stats.get("Male", {}).get("Attrition Rate", 0)
                utils.render_card(
                    key="attrition_card2",
                    title="Male<br>Attrition",
                    value=male_attr_tot,
                    secondary_text=f" ({male_attr_pct})%",
                    icon="fa-sharp fa-solid fa-mars fa-xs",
                    progress_value=int(male_attr_pct),
                    progress_color="red",
                )
            with c1_col3:
                female_attr_tot = attrition_stats.get("Female", {}).get(
                    "Total Attrition", 0
                )
                female_attr_pct = attrition_stats.get("Female", {}).get(
                    "Attrition Rate", 0
                )
                utils.render_card(
                    key="attrition_card3",
                    title="Female<br>Attrition",
                    value=female_attr_tot,
                    secondary_text=f" ({female_attr_pct})%",
                    icon="fa-sharp fa-solid fa-venus fa-xs",
                    progress_value=int(female_attr_pct),
                    progress_color="red",
                )
        utils.sep()

        ### attrition by department & job role
        with streamlit.container():
            (
                c2_col1,
                c2_col2,
            ) = streamlit.columns(2)
            with c2_col1:
                streamlit.plotly_chart(
                    plots.plot_dept_attrition(attrition_stats["Department"]),
                    use_container_width=True,
                )
            with c2_col2:
                streamlit.plotly_chart(
                    plots.plot_jobrole_attrition(attrition_stats["JobRole"]),
                    use_container_width=True,
                )
        utils.sep()

        ### attrition by distance to work & job satisfaction
        with streamlit.container():
            (
                c3_col1,
                c3_col2,
            ) = streamlit.columns(2)
            with c3_col1:
                streamlit.plotly_chart(
                    plots.plot_dist_attrition(attrition_stats["WorkplaceProximity"]),
                    use_container_width=True,
                )
            with c3_col2:
                streamlit.plotly_chart(
                    plots.plot_satis_attrition(attrition_stats["JobSatisfaction"]),
                    use_container_width=True,
                )
        utils.sep()

        ### attrition by age & work-experience
        with streamlit.container():
            (
                c4_col1,
                c4_col2,
            ) = streamlit.columns(2)
            with c4_col1:
                streamlit.plotly_chart(
                    plots.plot_ages_attrition(attrition_stats["Ages"]),
                    use_container_width=True,
                )
            with c4_col2:
                # attrition by work exp buckets - horizontal bar
                streamlit.plotly_chart(
                    plots.plot_exp_attrition(attrition_stats["WorkExperience"]),
                    use_container_width=True,
                )
        utils.sep()

        with streamlit.expander("View Insights..."):
            utils.show_insights(
                [
                    "* Overall attrition rate is > 16%, well above the stipulated max"
                    " rate (10%). Company needs to act upon it quickly",
                    "* R&D and Sales are biggest departments by head-count and "
                    "proportionately attrition rate are highest among them which is "
                    "expected",
                    "* Attrition is rising exponentially for non-director and "
                    "non-manager level employees. This may indicate junior level "
                    "employees do not prefer to stick around for some reason",
                    "* Its also evident that most of the people leaving the company "
                    "living far off, is traveling distance/cost is driving this "
                    "this behavior? what action company can take to remedy this issue?"
                    "* Over 58% of dissatisfied employees leave, company needs to "
                    "have closer look at satisfaction survey and try to pin point "
                    "the root cause and then fix it",
                    "* Over 76% people leaving the company have work experience <= 10 "
                    "years. This is not a good sign, this means people in early phase "
                    "of their career do not find company attractive, why?",
                    "Over 57% of people leaning are between age 25 to 38 years, "
                    "why this particular age group does not prefer to stay longer?",
                ]
            )
