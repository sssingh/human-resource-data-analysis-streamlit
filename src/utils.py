"""App agnostic reusable utility functionality"""

from typing import List
from PIL import Image

import streamlit
from streamlit_kpi import streamlit_kpi as card
from config import app_config


def setup_app(config):
    """Sets up all application level configurations"""
    streamlit.set_page_config(
        page_title=config.app_title,
        page_icon=config.icon,
        initial_sidebar_state=config.sidebar_state,
        layout=config.layout,
    )
    __set_banner_title(banner=config.banner_image, title=config.app_title)


def create_tabs(tabs: List[str]):
    """Creates streamlit tabs"""
    return streamlit.tabs(tabs)


def sep():
    """Renders a horizontal separator"""
    streamlit.markdown("---")


def render_card(
    key,
    title,
    value,
    secondary_text="",
    progress_value=100,
    progress_color="#007a99",
    icon="fa-globe",
):
    """Renders a custom KPI card with optional icon and progress-bar"""
    the_card = card(
        key=key,
        title=title,
        value=int(value),
        unit=secondary_text,
        icon=icon,
        iconTop=5,
        iconLeft=98,
        height=150,
        progressValue=progress_value,
        progressColor=progress_color,
        backgroundColor="#003d4d",  # "#D3D3D3"
        titleColor="#d9d9d9",
        valueColor="#d9d9d9",
    )
    return the_card


def download_file(btn_label, data, file_name, mime_type):
    """Creates a download button for data download"""
    streamlit.download_button(
        label=btn_label, data=data, file_name=file_name, mime=mime_type
    )


def show_questions(questions: List[str]):
    q = "QUESTIONS:\n" + "\n".join(questions)
    streamlit.info(q, icon=app_config.icon_question)


def show_insights(insights: List[str]):
    a = "INSIGHTS:\n" + "\n".join(insights)
    streamlit.warning(a, icon=app_config.icon_insight)


### module's internal/private functions
def __set_banner_title(banner, title):
    image = Image.open(banner)
    image = image.resize((image.width, 150), resample=Image.Resampling.NEAREST)
    streamlit.image(image=image)
    streamlit.title(title)
