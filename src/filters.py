"""handles dashboard filters"""

import data
import streamlit as st


def apply(df):
    """filters the dataframe using active filters and returns the filtered dataframe"""
    ### get all filters elements to be build from the dataset
    filter_elem = data.get_filter_elements(df)
    ### build the filter UI
    curr_filter_ui = __build_filter_ui(df, filter_elem)
    ### read the session state and apply filter on the dataframe
    df = __apply_filters(df, filter_elem, curr_filter_ui)
    return df


### modules internal functions
def __build_filter_ui(df, filter_elem):
    st.sidebar.markdown("# REPORT FILTERS")
    st.sidebar.markdown("---")

    ### If user clicked to clear all the filters then reset the session state
    filter_clear = data.get_filter_elements(df, clear_filters=True)
    if st.sidebar.button("Clear Filters"):
        for key, options in filter_clear.items():
            st.session_state[key] = options
    curr_filter_ui = st.sidebar.expander("Current Active Filter:")

    ### build the UI
    for key, options in filter_elem.items():
        st.sidebar.markdown("---")
        # if categorical variable
        if isinstance(options[0], str):
            st.sidebar.multiselect(key=key, label=key, options=options)
        # if numeric variable
        else:
            st.sidebar.slider(
                key=key,
                label=key,
                min_value=int(options[0]),
                max_value=int(options[1]),
                value=(int(options[0]), int(options[1])),
            )
    return curr_filter_ui


def __apply_filters(df, filter_elem, curr_filter_ui):
    ### build the query
    ### loop through filter elements and get its current value from session_state
    ### and . Include the element only if its non-empty-list
    filter = ""
    for key, _ in filter_elem.items():
        elem = st.session_state[key]
        # non-empty
        if elem:
            # if there are existing filters then append "and"
            if filter:
                filter += " and "
            # check if string
            if isinstance(elem[0], str):
                filter += f"({key} == {elem})"
            # else (numerical), it will have a min and max range
            else:
                filter += f"({elem[0]} <= {key} <= {elem[1]})"
    # show filter in sidebar
    with curr_filter_ui:
        filter_show = "<br>and".join(filter.split("and"))
        st.markdown(
            f'<span style="color:#002b36"><b><i>{filter_show}</i></b></span>',
            unsafe_allow_html=True,
        )
    # return the filtered dataframe
    return df.query(filter)
