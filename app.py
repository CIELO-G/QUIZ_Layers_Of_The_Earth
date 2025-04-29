import streamlit as st
import json

# ──────────────────────────────────────────────────────────────────────────────
# 1. Page Setup
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Earth Layers Quiz", page_icon="🌎")

st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# 2. Initialize Session State
# ──────────────────────────────────────────────────────────────────────────────
default_values = {
    'current_index': 0,
    'score': 0,
    'selected_option': None,
    'answer_submitted': False
}
for key, value in default_values.items():
    st.session_state.setdefault(key, value)

# ──────────────────────────────────────────────────────────────────────────────
# 3. Load Quiz Data
# ──────────────────────────────────────────────────────────────────────────────
with open('content/quiz_data.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

# ──────────────────────────────────────────────────────────────────────────────
# 4. Helper Functions
# ──────────────────────────────────────────────────────────────────────────────
def restart_quiz():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False

def submit_answer():
    if st.session_state.selected_option is not None:
        st.session_state.answer_submitted = True
        correct = quiz_data[st.session_state.current_index]['answer']
        if st.session_state.selected_option == correct:
            st.session_state.score += 10
    else:
        st.warning("Please select an option before submitting.")

def next_question():
    st.session_state.current_index += 1
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False

# ──────────────────────────────────────────────────────────────────────────────
# 5. Quiz Interface
# ──────────────────────────────────────────────────────────────────────────────
st.title("🌎 Earth Layers Quiz")

progress = (st.session_state.current_index + 1) / len(quiz_data)
st.metric(label="Score", value=f"{st.session_state.score} / {len(quiz_data) * 10}")
st.progress(progress)

# Display current question
question_item = quiz_data[st.session_state.current_index]
st.subheader(f"Question {st.session_state.current_index + 1}")
st.write(f"**{question_item['question']}**")
st.write(question_item['information'])

correct_answer = question_item['answer']
options = question_item['options']

# Answer buttons
if st.session_state.answer_submitted:
    for i, option in enumerate(options):
        if option == correct_answer:
            st.success(f"✅ {option} (Correct)")
        elif option == st.session_state.selected_option:
            st.error(f"❌ {option} (Your Choice)")
        else:
            st.write(option)
else:
    for i, option in enumerate(options):
        if st.button(option, key=i, use_container_width=True):
            st.session_state.selected_option = option

# Submit or Next
st.divider()

if st.session_state.answer_submitted:
    if st.session_state.current_index < len(quiz_data) - 1:
        st.button('Next Question ➡️', on_click=next_question)
    else:
        st.success(f"🏁 Quiz Finished! Final Score: {st.session_state.score} / {len(quiz_data) * 10}")
        if st.button('Restart Quiz 🔄', on_click=restart_quiz):
            pass
else:
    if st.session_state.selected_option is not None:
        st.button('Submit Answer ✅', on_click=submit_answer)
