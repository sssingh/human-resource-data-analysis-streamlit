"""Summary tab rendering functionality"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit
import streamlit_nested_layout  # unofficial package for nested layout

import data
import plots
import utils
from config import app_config


###
### render the summary page
###
def render(df: pd.DataFrame):
    # Show sample data in a dataframe
    __show_sample_data(df)
    # Show KPI cards section
    __build_kpi_cards(df)
    # Show plots
    __build_age_plots(df)
    __build_dept_plots(df)
    __build_exp_plots(df)


###
### module's internal functions
###
def __show_sample_data(df: pd.DataFrame):
    """Display sample data as pandas DataFrame"""
    with streamlit.expander("View sample data | Download dataset..."):
        streamlit.markdown("#### Top 5 rows")
        streamlit.dataframe(df.head(5))
        streamlit.markdown("#### Bottom 5 rows")
        streamlit.dataframe(df.tail(5))
        # read the file again and then download
        csv = data.df_to_csv(app_config.data_file)
        utils.download_file(
            btn_label="Download As CSV",
            data=csv,
            file_name="hr_data_downloaded.csv",
            mime_type="text/csv",
        )


def __build_kpi_cards(df: pd.DataFrame):
    """display total, male, female employees cards"""
    with streamlit.expander("View Gender Stats...", expanded=True):
        ## List questions/objectives
        utils.show_questions(
            [
                "* Do we have a balanced workforce in terms of gender?",
            ]
        )

        # total and gender wise emp count
        __show_emp_count_card(df)

        ## List insights drawn wrt to objectives/questions
        with streamlit.expander("View insights..."):
            utils.show_insights(
                [
                    "* No vast disparity exists between the 'Male' and 'Female' employee populations. "
                    + "However, there is a scope to increase the hiring of female employees.",
                ]
            )


def __show_emp_count_card(df):
    (
        tot_emp_cnt,
        male_emp_cnt,
        female_emp_cnt,
        male_pct,
        female_pct,
    ) = data.get_gender_count(df)

    with streamlit.container():
        g_col1, g_col2, g_col3 = streamlit.columns(3)
        with g_col1:
            utils.render_card(
                key="tot_card",
                title="Total<br>Employees",
                value=tot_emp_cnt,
                icon="fa-sharp fa-solid fa-venus-mars fa-xs",
            )
        with g_col2:
            utils.render_card(
                key="male_card",
                title="Males",
                value=male_emp_cnt,
                secondary_text=f" ({male_pct})%",
                icon="fa-sharp fa-solid fa-mars fa-xs",
                progress_value=int(male_pct),
                progress_color="#186ee8",
            )
        with g_col3:
            utils.render_card(
                key="female_card",
                title="Females",
                value=female_emp_cnt,
                secondary_text=f" ({female_pct})%",
                icon="fa-sharp fa-light fa-venus fa-xs",
                progress_value=int(female_pct),
                progress_color="#ff6d6d",
            )


def __build_age_plots(df: pd.DataFrame):
    ### age distribution
    with streamlit.expander("Analysis: Age & Marital Status...", expanded=True):
        utils.show_questions(
            [
                "* Are we an ageing or young organization?",
                "* Do we need to recruit more young or more experienced people?",
                "* Should we target recruiting employees for a particular age group and gender?",
                "* Do we have a balanced distribution of employees by their marital status?",
            ]
        )

        (
            age_dist_col1,
            age_dist_col2,
        ) = streamlit.columns(2)
        with age_dist_col1:
            fig_age_hist = plots.plot_age_hist(df)
            streamlit.plotly_chart(fig_age_hist, use_container_width=True)
        with age_dist_col2:
            fig_age_box = plots.plot_age_gender_box(df)
            streamlit.plotly_chart(fig_age_box, use_container_width=True)
        with age_dist_col1:
            fig_age_box = plots.plot_age_marital_status_pie(df)
            streamlit.plotly_chart(fig_age_box, use_container_width=True)
        with age_dist_col2:
            fig_age_box = plots.plot_age_marital_status_box(df)
            streamlit.plotly_chart(fig_age_box, use_container_width=True)
        ### List insights drawn wrt to objectives/questions
        with streamlit.expander("View insights...", expanded=True):
            utils.show_insights(
                [
                    "* The median employee age is 36 yrs, where the minimum is 18 yrs, "
                    + "and the maximum is 60. 25% of employees (Q1) are below 30 yrs, "
                    + "50% are between 30 yrs and 43 yrs, remaining 25% are above 43 yrs. "
                    + "This shows the company is neither ageing nor a very young organization. "
                    + "The age is somewhat normally distributed with a long right tail. "
                    + "The addition of new employees with ages below 30 yrs is advisable.",
                    "* The median female age is 36 yrs, and the median male age is 35 yrs. "
                    + "50% of the female population is between 31 and 44 yrs, while 50% of "
                    + "males are between  30 and 42 yrs. Therefore, the gender-wise workforce "
                    + "is quite balanced, and there is no need to target age-specific hiring "
                    + "for a given gender",
                    "* 45% are married, and 32% are single. 50% of married employees are "
                    + "between 31 and 44, while 50% of singles are 29 to 41; this pattern "
                    + "seems normal. There are 22% divorced, with 50% between 25 to 43; "
                    + "this appears to be a bit unusual, and HR should note it.",
                ]
            )


def __build_dept_plots(df: pd.DataFrame):
    ### department stats
    with streamlit.expander("Analysis: Departments...", expanded=True):
        utils.show_questions(
            [
                "* Which department is the largest employer? ",
                "* Do we have balanced gender distribution in each department? ",
                "* In which department do people stick to their manager longest? ",
                "* In which department do people tend to do more overtime? ",
                "* Which department is the best paymaster? ",
            ]
        )
        fig_dept_gender_count = plots.plot_dept_gender_count_sunburst(df)
        streamlit.plotly_chart(fig_dept_gender_count, use_container_width=True)
        with streamlit.container():
            ## department stats table
            utils.sep()
            streamlit.markdown("###### Department Stats")
            df_dept_stats = data.get_dept_stats_df(df)
            streamlit.dataframe(
                df_dept_stats.style.background_gradient(cmap="Oranges"),
                use_container_width=True,
            )
            ## yrs with curr manager
            utils.sep()
            fig_dept_curr_mgr = plots.plot_dept_curr_mgr_scatter(df)
            streamlit.plotly_chart(fig_dept_curr_mgr, use_container_width=True)
        with streamlit.expander("View insights..."):
            utils.show_insights(
                [
                    "* By far, R&D is the largest department, employing 65% of the workforce, "
                    + "then sales (30%) and HR (4%).",
                    "There is a considerable gender imbalance in each department, and each "
                    + "department has 15% more male employees than females. The disparity is "
                    + "more severe in R&D and HR.",
                    "* In Sales, employees tend to stick to their manager longer despite the "
                    "R&D being twice the size of Sales",
                    "* Even though R&D has double the workforce compared to Sales, twice as "
                    + "many R&D employees are doing overtime compared to sales employees. "
                    + "Are they still short in the workforce, or is there another "
                    + "underlying reason?",
                    "* On average Sales, the department is the best paymaster while the "
                    + "salary hike in R&D is slightly better than Sales.",
                ]
            )


def __build_exp_plots(df: pd.DataFrame):
    ### experience stat
    with streamlit.expander("Analysis: Work experience...", expanded=True):
        utils.show_questions(
            [
                "* Do we have a balanced distribution of employees based on their work experience? ",
                "* Do we need targeted hiring for a particular work experience range? ",
                "* Do employees prefer to work with our company for most of their working life? ",
            ]
        )
        exp_stat_col1, exp_stat_col2 = streamlit.columns(2)
        with exp_stat_col1:
            # Total work experience
            fig_plot_tot_work_exp = plots.plot_tot_work_exp_bar(df)
            streamlit.plotly_chart(fig_plot_tot_work_exp, use_container_width=True)
        # Total experience Vs experience in our company
        with exp_stat_col2:
            # Total work experience
            pct_at_cmp = data.get_pct_at_cmp(df)
            annot_text = __get_pct_at_cmp_annot_text(pct_at_cmp)
            fig_plot_cmp_work_exp = plots.plot_cmp_work_exp_scatter(df, annot_text)
            streamlit.plotly_chart(fig_plot_cmp_work_exp, use_container_width=True)
        with streamlit.expander("View insights...", expanded=True):
            utils.show_insights(
                [
                    "* There is a good mix of experience, however around 75 percent of workforce "
                    + "is with experience 15 years or less, company should look to ramp-up "
                    + " experienced hiring bit more. ",
                    "* The relation between total-work-experience to years-at-company is "
                    + "linear, large percentage of employee have spent most of their working life "
                    + "with the company. Over 52% of employee have spent > 76% of their career "
                    " at our company which is a good sign",
                ]
            )


def __get_pct_at_cmp_annot_text(pct_at_cmp):
    annot_text = "Employee % by yrs work for company [in %] <br>"
    annot_text += "-----------------------------------------<br>"
    for key, value in pct_at_cmp.items():
        annot_text += key + "\t: " + f"{value * 100:.2f}%<br>"
    return annot_text
