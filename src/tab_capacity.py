"""Performance tab rendering functionality"""

import pandas as pd
import streamlit
import utils
import data
import plots

# from tab_summary import show_emp_count_card

###
### render the capacity page
###
def render(df: pd.DataFrame):
    # Show KPI cards section
    __build_kpi_cards(df)
    # Show plots
    __build_promo_plots(df)
    __build_retrench_plots(df)
    __build_attrition_plots(df)


###
### module's internal functions
###
def __build_kpi_cards(df):
    with streamlit.expander("View Overall promotion & retrenchment stats..."):
        ### List questions/objectives
        utils.show_questions(
            [
                "* Questions?",
            ]
        )
        promo_col, retrench_col = streamlit.columns(2)

        ### Overall promotion stats
        with promo_col:
            __show_promotion_stats(df)
        ### Overall retrenchment stats
        with retrench_col:
            __show_retrench_stats(df)

        ## List insights drawn wrt to objectives/questions
        with streamlit.expander("View insights..."):
            utils.show_insights(
                [
                    "* Answers. " + "Answers.",
                ]
            )


def __build_promo_plots(df):
    with streamlit.expander("Analysis: Employee Promotion..."):
        utils.show_questions(
            [
                "* Question 1?",
                "* Question 2?",
                "* Question 3?",
            ]
        )

        col1, col2 = streamlit.columns(2)
        with col1:
            pass
        with col2:
            pass
        with streamlit.expander("View Employee Promotion Insights..."):
            utils.show_insights(
                [
                    "* Insight 1",
                    "* Insight 2",
                    "* Insight 3",
                ]
            )


def __build_attrition_plots(df):
    with streamlit.expander("Analysis: Employee Attrition..."):
        utils.show_questions(
            [
                "* Question 1?",
                "* Question 2?",
                "* Question 3?",
            ]
        )

        col1, col2 = streamlit.columns(2)
        with col1:
            pass
        with col2:
            pass
        with streamlit.expander("View Employee Attrition Insights..."):
            utils.show_insights(
                [
                    "* Insight 1",
                    "* Insight 2",
                    "* Insight 3",
                ]
            )


def __build_retrench_plots(df):
    with streamlit.expander("Analysis: Employee Retrenchment..."):
        utils.show_questions(
            [
                "* Question 1?",
                "* Question 2?",
                "* Question 3?",
            ]
        )

        col1, col2 = streamlit.columns(2)
        with col1:
            pass
        with col2:
            pass
        with streamlit.expander("View Employee Retrenchment Insights..."):
            utils.show_insights(
                [
                    "* Insight 1",
                    "* Insight 2",
                    "* Insight 3",
                ]
            )


def __show_promotion_stats(df):
    promo_cnt, not_promo_cnt, promo_pct, no_promo_pct = data.get_promo_count(df)
    utils.render_card(
        key="promo_card",
        title="Promote",
        value=promo_cnt,
        secondary_text=f" ({promo_pct})%",
        icon="fa-thumbs-up",
        progress_value=int(promo_pct),
        progress_color="green",
    )
    utils.render_card(
        key="no_promo_card",
        title="No promotion",
        value=not_promo_cnt,
        secondary_text=f" ({no_promo_pct})%",
        icon="fa-thumbs-down",
        progress_value=int(no_promo_pct),
        progress_color="red",
    )
    fig = plots.plot_promotion_donut(df)
    streamlit.plotly_chart(fig, use_container_width=True)


def __show_retrench_stats(df):
    (
        retrench_cnt,
        not_retrench_cnt,
        retrench_pct,
        not_retrench_pct,
    ) = data.get_retrench_count(df)
    utils.render_card(
        key="no_retrench_card",
        title="No Retrench",
        value=not_retrench_cnt,
        secondary_text=f" ({not_retrench_pct})%",
        icon="fa-thumbs-down",
        progress_value=int(not_retrench_pct),
        progress_color="green",
    )
    utils.render_card(
        key="retrench_card",
        title="Retrench",
        value=retrench_cnt,
        secondary_text=f" ({retrench_pct})%",
        icon="fa-thumbs-up",
        progress_value=int(retrench_pct),
        progress_color="red",
    )
    fig = plots.plot_retrench_donut(df)
    streamlit.plotly_chart(fig, use_container_width=True)
