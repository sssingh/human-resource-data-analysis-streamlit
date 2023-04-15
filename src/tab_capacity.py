"""Capacity tab rendering functionality"""

import pandas as pd
import streamlit
import utils
import data
import plots


###
### render the capacity page
###
def render(df: pd.DataFrame):
    # Show KPI cards section
    __build_kpi_cards(df)
    # Show plots
    __build_dept_promo_retrench_plots(df)


###
### module's internal functions
###
def __build_kpi_cards(df):
    with streamlit.expander("Overall promotion & retrenchment stats...", expanded=True):
        ### List questions/objectives
        utils.show_questions(
            [
                "* Do we have a healthy promotion rate (min 10%)?",
                "* Are we above or below performance-based retrenchment rate (max 5%)?",
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
                    "* Rate of promotion is way short of the stipulated minimum "
                    + "promotion rate target. Company need to have a deeper look at it "
                    + "and take corrective action.",
                    "* Retrenchment rate is more than double the stipulated maximum "
                    + "retrenchment rate, this is alarming and immediate corrective "
                    + "action should be taken.",
                ]
            )


def __show_promotion_stats(df):
    promo_cnt, not_promo_cnt, promo_pct, no_promo_pct = data.get_promo_count(df)
    utils.render_card(
        key="promo_card",
        title="Promote",
        value=promo_cnt,
        secondary_text=f" ({promo_pct})%",
        icon="fa-sharp fa-solid fa-user-check fa-xs",
        progress_value=int(promo_pct),
        progress_color="green",
    )
    utils.render_card(
        key="no_promo_card",
        title="No Promotion",
        value=not_promo_cnt,
        secondary_text=f" ({no_promo_pct})%",
        icon="fa-sharp fa-solid fa-user-xmark fa-xs",
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
        icon="fa-sharp fa-solid fa-user-plus fa-xs",
        progress_value=int(not_retrench_pct),
        progress_color="green",
    )
    utils.render_card(
        key="retrench_card",
        title="Retrench",
        value=retrench_cnt,
        secondary_text=f" ({retrench_pct})%",
        icon="fa-sharp fa-solid fa-user-minus fa-xs",
        progress_value=int(retrench_pct),
        progress_color="red",
    )
    fig = plots.plot_retrench_donut(df)
    streamlit.plotly_chart(fig, use_container_width=True)


def __build_dept_promo_retrench_plots(df):
    with streamlit.expander("Analysis: Department wise promotion & retrenchment..."):
        utils.show_questions(
            [
                "* How each department is doing in promoting employees?",
                "* Which department has the highest rate of retrenchment?",
            ]
        )

        promo_col, retrench_col = streamlit.columns(2)
        with promo_col:
            df_promo = data.get_dept_promo_pct(df)
            fig = plots.plot_dept_promo_bar(df_promo)
            streamlit.plotly_chart(fig, use_container_width=True)
        with retrench_col:
            df_retrench = data.get_dept_retrench_pct(df)
            fig = plots.plot_dept_retrench_bar(df_retrench)
            streamlit.plotly_chart(fig, use_container_width=True)
        with streamlit.expander("View Insights..."):
            utils.show_insights(
                [
                    "* All three departments are doing extremely poorly when it comes "
                    + "to promoting employees, none of the departments even achieved "
                    + "even 50% of the stipulated promotion target (min 10%).",
                    "* On retrenchment front matter is even worse where all three "
                    + "overshot the retrenchment targets, R&D and Sales departments "
                    + "are projecting more than twice the stipulated target (max 5%) ",
                ]
            )
