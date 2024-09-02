import streamlit as st
import json
from model import Model


def show():
    model_options = st.session_state.projects_dict.keys()
    key = st.selectbox("Select Model or create a new model by clicking on the `Create Model` button", options=model_options)
    settings = st.session_state.projects_dict[key]
    st.write(settings)
    settings['title'] = st.text_input("Model Name", value=settings['title'])
    settings['description'] = st.text_area("Description", value=settings['description'])
    categories = st.text_input("Categories (comma separated)", value=','.join(settings['categories']))
    settings['categories'] = categories.split(',')
    settings['image_number'] = st.number_input("Number of Images", min_value=1, max_value=100, value=settings['image_number'])
    
    cols = st.columns(4)
    with cols[0]:
        if st.button("Save"):
            if settings['new']:
                key = settings['title'].lower().replace(' ', '_')
                settings['key'] = key
                st.session_state.model = Model(settings)
            
            settings['new'] = False
            st.session_state.projects_dict[key].settings = settings
            st.session_state.model.save()
    with cols[1]:
        if st.button("Create Model"):
            settings = {'title': '<project_title>',
                'description':'<project_description>',
                'categories': '<category1, category2>',
                'image_number': 10,
                'default': False,
                'new': True
            }
    with cols[2]:
        if not st.session_state.model.default:
            if st.button("Delete Model"):
                del st.session_state.projects_dict[key]
                save_dict()
        
