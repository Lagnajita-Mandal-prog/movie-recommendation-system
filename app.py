import streamlit as st
from recommendation import recommend

st.title("Movie Recommendation System")

user_input = st.text_input("Enter a movie name:")

# Button with key to avoid duplicate error
if st.button("Recommend", key="search") and user_input:
    suggestions = recommend(user_input)
    
    if not suggestions or suggestions[0] == "Movie not found :(":
        st.error("Movie not found in database. Please check the spelling or try another movie.")
    else:
        st.subheader("You might also like:")
        for i, movie in enumerate(suggestions, 1):
            st.write(f"{i}. {movie}")

elif st.button("Recommend", key="empty_input"):
    st.warning("Please enter a movie name first.")
