import pickle
import streamlit as st
import numpy as np

# Load the updated Random Forest model
with open("assignment.pkl", "rb") as file:
    model = pickle.load(file)

# Define the top 10 features from your feature importance chart
top_features_human_readable = {
    "odor_n": "Odor (None)?",
    "gill_size_n": "Gill Size (Narrow)?",
    "odor_f": "Odor (Foul)?",
    "gill_size_b": "Gill Size (Broad)?",
    "stalk-surface-below-ring_k": "Stalk Surface Below Ring (Silky)?",
    "spore-print-color_h": "Spore Print Color (Chocolate)?",
    "ring-type_p": "Ring Type (Pendant)?",
    "gill-color_b": "Gill Color (Buff)?",
    "bruises_f": "Bruises (None)?",
    "stalk-surface-above-ring_k": "Stalk Surface Above Ring (Silky)?"
}

# Streamlit app setup
st.set_page_config(page_title="Mushroom Classification", page_icon="🍄", layout="centered")
st.title("Mushroom Classification App 🍄")
st.write("Predict whether a mushroom is **poisonous** or **edible** based on its characteristics.")

st.header("Enter Mushroom Characteristics")

# Create a dictionary to collect user inputs
user_inputs = {}
for feature, label in top_features_human_readable.items():
    user_inputs[feature] = st.selectbox(
        label, ["Select a value", "Yes", "No"]
    )

# Add custom CSS and JavaScript for floating emojis and sound effects
custom_css_js = """
<style>
@keyframes floatEmojis {
  0% {
    transform: translate(0, 0);
    opacity: 1;
  }
  100% {
    transform: translate(0, -200px);
    opacity: 0;
  }
}
.emoji {
  position: fixed;
  font-size: 3rem;
  animation: floatEmojis 3s ease-out forwards;
  pointer-events: none;
}
</style>
<script>
function addEmoji(emoji) {
  const span = document.createElement('span');
  span.textContent = emoji;
  span.className = 'emoji';
  span.style.left = Math.random() * 100 + 'vw';
  span.style.top = Math.random() * 100 + 'vh';
  document.body.appendChild(span);
  setTimeout(() => span.remove(), 3000);
}
function floatEmojis(emojis) {
  emojis.forEach(emoji => {
    for (let i = 0; i < 10; i++) {
      setTimeout(() => addEmoji(emoji), i * 100);
    }
  });
}
</script>
"""

st.markdown(custom_css_js, unsafe_allow_html=True)

# Prediction logic
if st.button("Predict"):
    # Ensure all values are selected
    if "Select a value" in user_inputs.values():
        st.error("Please select all values before making a prediction.")
    else:
        # Convert user inputs to numerical format (Yes -> 1, No -> 0)
        input_data = [1 if value == "Yes" else 0 for value in user_inputs.values()]

        # Make prediction
        prediction = model.predict([input_data])[0]

        # Add floating emojis and sound effects based on prediction
        if prediction == 1:
            st.error("**☠️ DONT EAT THE MUSHROOM, IT IS POISONOUS! ☠️**")
            st.markdown(
                "<script>floatEmojis(['💀', '☠️', '⚰️']);</script>",
                unsafe_allow_html=True,
            )
            st.audio("https://www.soundjay.com/misc/sounds/fail-trombone-01.mp3", format="audio/mp3")
        else:
            st.success("**🎉 Congratulations, the mushroom is edible! 🎉**")
            st.markdown(
                "<script>floatEmojis(['🍄', '👨‍🍳', '🍽️']);</script>",
                unsafe_allow_html=True,
            )
            st.audio("https://www.soundjay.com/button/beep-07.wav", format="audio/wav")
