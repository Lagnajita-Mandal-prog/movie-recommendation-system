# app.py
import streamlit as st
from recommendation import recommend

st.title("Movie Recommendation System")

user_input = st.text_input("Enter a movie name:")
if st.button("Recommend") and user_input:
    suggestions = recommend(user_input)
    if not suggestions or suggestions[0] == "Movie not found :(":
        st.error("Movie not found in database. Check spelling or try another.")
    else:
        st.subheader("You might also like:")
        for i, movie in enumerate(suggestions, 1):
            st.write(f"{i}. {movie}")
elif st.button("Recommend"):
    st.warning("Please enter a movie name.")
