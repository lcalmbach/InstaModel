import os
import requests
from duckduckgo_search import DDGS
from fastcore.all import *
from PIL import Image
import zipfile
from io import BytesIO
from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu
import json

from model import Model
import info
import create_model


__version__ = "0.0.1"
__author__ = "Lukas Calmbach"
__author_email__ = "lcalmbach@gmail.com"
VERSION_DATE = "2024-08-27"
APP_NAME = "InstaModel"
GIT_REPO = "https://github.com/lcalmbach/insta-model"

menu_options = [
    "About",
    "Select/Create Model",
    "Search Images",
    "Train"
]

# https://icons.getbootstrap.com/?q=image
menu_icons = ["house", "bar-chart-steps", "search", "gear"]

APP_INFO = f"""<div style="background-color:#34282C; padding: 10px;border-radius: 15px; border:solid 1px white;">
    <small>App von <a href="mailto:{__author_email__}">{__author__}</a><br>
    Version: {__version__} ({VERSION_DATE})<br>
    <a href="{GIT_REPO}">git-repo</a></small></div>
    """

def init():
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def main():
    if 'model' not in st.session_state:
        with open('./projects.json', 'r') as file:
            st.session_state.projects_dict = json.load(file)
        st.session_state.model = Model(st.session_state.projects_dict['cities'])
    
    init()
    
    if "keywords" not in st.session_state:
        st.session_state.keywords = []
        st.session_state.image_dict = {}

    with st.sidebar:
        st.sidebar.title(f"{APP_NAME} 🔦")
        menu_action = option_menu(
            None,
            menu_options,
            icons=menu_icons,
            menu_icon="cast",
            default_index=0,
        )
    index = menu_options.index(menu_action)
    if index == 0:
        info.show()
    if index == 1:
        create_model.show()
    if index == 2:
        info.show()

    

if __name__ == "__main__":
    main()