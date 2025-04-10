import streamlit as st

st.set_page_config(
    page_title="Climate change project",
    page_icon="🥵",
)

st.write("# Predicting climate change effect in France")
st.write("## Le Wagon, Data Science, Batch 1835")

st.markdown(
    """
    The goal of this project is to train an algorythm in order to predict the evolution of temperatures in France over the next 50 years.
    
    #### Check out our <a href="/Demo" target="_self">demo</a> 👀
""", unsafe_allow_html=True
)