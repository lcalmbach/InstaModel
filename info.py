import streamlit as st
from graphviz import Digraph
from text import texts

def show():
    def show_process_chart():
        e = Digraph('ER', filename='er.gv', engine='neato')

        # Set global attributes for nodes
        e.attr('node', shape='box', style='filled', align='center')

        # Define nodes
        e.node('Select model name', pos='0,2!', width='1')
        e.node('Define categories', pos='0,1!', width='1')
        e.node('Search images', pos='0,0!', width='1')
        e.node('Train model', pos='1,-1!', width='1')
        e.node('Upload File', pos='1,-2!', width='1')
        e.node('Prediction', pos='1,-3!', width='1')

        # Create directed edges (arrows)
        e.edge('Select model name', 'Define categories')
        e.edge('Define categories', 'Search images', len='1.00')
        e.edge('Search images', 'Train model', len='1.00')
        e.edge('Train model', 'Upload File')
        e.edge('Upload File', 'Prediction', len='1.00')

        # Set graph attributes
        e.attr(fontsize='20')

        # Render the graph in Streamlit
        st.graphviz_chart(e)

    st.title('About the App')
    st.markdown(texts['info'])
    show_process_chart()