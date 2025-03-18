import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import joblib
import re

# Load the pre-trained model
pipe_lr = joblib.load(open("model/text_emotion.pkl", "rb"))

# Emoji dictionary for emotions
emotions_emoji_dict = {
    "anger": "😠", "disgust": "🤮", "fear": "😨😱", "happy": "🤗", 
    "joy": "😂", "neutral": "😐", "sad": "😔", "sadness": "😔", 
    "shame": "😳", "surprise": "😮"
}

# Function to predict emotion
def predict_emotions(docx):
    results = pipe_lr.predict([docx])
    return results[0]

# Function to get prediction probabilities
def get_prediction_proba(docx):
    results = pipe_lr.predict_proba([docx])
    return results

# Function to check if the input contains only numbers, punctuation, or symbols without text
def is_invalid_input(text):
    # Check if the text is only numbers, punctuation, or symbols
    if re.match(r'^\d+$', text):  # One or more numbers
        return True
    if re.match(r'^[.,!?]+$', text):  # One or more punctuation marks
        return True
    if re.match(r'^[\W_]+$', text):  # One or more symbols (non-word characters or symbols in the keyboard)
        return True
    return False

# Main function for the app
def main():
    st.title("Discover the Mental Health Status")
    st.subheader("Identify Emotion Status from Text")
      
    with st.form(key='my_form'):
        raw_text = st.text_area("Type Here")
        submit_text = st.form_submit_button(label='Submit')

    # If the user submits the form
    if submit_text:
        # Validation: Check if the text box is empty, null, or contains invalid input (numbers, punctuation, or symbols without text)
        if raw_text is None or not raw_text.strip():
            st.warning("✨ Oops! Looks like you forgot to type something. Please fill in the text box before submitting!")  # Pop-up-like warning message
        elif is_invalid_input(raw_text):
            st.warning("⚠️ Invalid input!")  # Pop-up for invalid input
        else:
            # If the input is valid, initialize col1 and col2
            col1, col2 = st.columns(2)

            prediction = predict_emotions(raw_text)
            probability = get_prediction_proba(raw_text)

            with col1:
                st.success("Original Text")
                st.write(raw_text)

                st.success("Prediction")
                emoji_icon = emotions_emoji_dict[prediction]
                st.write(f"{prediction}: {emoji_icon}")
                st.write(f"Confidence: {np.max(probability):.2f}")

            with col2:
                st.success("Prediction Probability")
                proba_df = pd.DataFrame(probability, columns=pipe_lr.classes_)
                proba_df_clean = proba_df.T.reset_index()
                proba_df_clean.columns = ["emotions", "probability"]

                fig = alt.Chart(proba_df_clean).mark_bar().encode(
                    x='emotions', 
                    y='probability', 
                    color='emotions'
                )
                st.altair_chart(fig, use_container_width=True)

if __name__ == '__main__':
    main()
