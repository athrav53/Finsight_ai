import streamlit as st

st.title("FinSight AI - Button Test")

st.write("Can you see the button below?")

if st.button("CLICK ME"):
    st.success("Button is working!")
