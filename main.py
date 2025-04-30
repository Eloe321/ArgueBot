import streamlit as st
from openai import OpenAI
import random

# Set up the OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# List of "Would You Rather" questions
would_you_rather_questions = [
    {"option_a": "be able to fly", "option_b": "be able to read minds"},
    {"option_a": "have unlimited money", "option_b": "have unlimited time"},
    {"option_a": "be invisible", "option_b": "be super strong"},
    {"option_a": "always be 10 minutes late", "option_b": "always be 20 minutes early"},
    {"option_a": "live in the past", "option_b": "live in the future"},
    {"option_a": "have a photographic memory", "option_b": "have an IQ of 200"},
    {"option_a": "win the lottery", "option_b": "live twice as long"},
    {"option_a": "speak all languages", "option_b": "be able to talk to animals"},
    {"option_a": "never have to sleep", "option_b": "never have to eat"},
    {"option_a": "be famous", "option_b": "be anonymous but rich"},
]

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "game_state" not in st.session_state:
    st.session_state.game_state = "question"  # possible states: "question", "debate"

if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(would_you_rather_questions)

if "user_choice" not in st.session_state:
    st.session_state.user_choice = None

if "opponent_choice" not in st.session_state:
    st.session_state.opponent_choice = None

if "rounds_played" not in st.session_state:
    st.session_state.rounds_played = 0

# Function to generate AI's debate response
def generate_debate_response(user_choice, opponent_choice):
    prompt = f"""
    The user has chosen they would rather {user_choice} in a 'Would You Rather' game.
    You should playfully and persuasively argue why {opponent_choice} would actually be the better choice.
    Be creative, entertaining, and use humor while making compelling points about why their choice isn't as good as they think.
    Keep your response concise (3-5 sentences).
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    
    return response.choices[0].message.content

# Function to handle user's choice
def handle_choice(choice, alternative):
    st.session_state.user_choice = choice
    st.session_state.opponent_choice = alternative
    st.session_state.game_state = "debate"
    
    # Generate AI's debate response
    ai_response = generate_debate_response(choice, alternative)
    
    # Add the debate to messages
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Function to start a new round
def new_round():
    st.session_state.current_question = random.choice(would_you_rather_questions)
    st.session_state.game_state = "question"
    st.session_state.user_choice = None
    st.session_state.opponent_choice = None
    st.session_state.rounds_played += 1

# App title
st.title("Would You Rather: AI Debate Edition")
st.write("Choose an option, and the AI will debate why the other option is better!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Game logic
if st.session_state.game_state == "question":
    # Display the current "Would You Rather" question
    st.write("## Would you rather...")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"A: {st.session_state.current_question['option_a']}"):
            handle_choice(
                st.session_state.current_question['option_a'],
                st.session_state.current_question['option_b']
            )
    
    with col2:
        if st.button(f"B: {st.session_state.current_question['option_b']}"):
            handle_choice(
                st.session_state.current_question['option_b'],
                st.session_state.current_question['option_a']
            )

elif st.session_state.game_state == "debate":
    # Process user's response to the AI's debate
    if prompt := st.chat_input("Your response?"):
        # Add user response to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Move to next round
        new_round()
        
        # Force a rerun to refresh the UI with the new game state
        st.rerun()

# Show score
st.sidebar.write(f"Rounds played: {st.session_state.rounds_played}")

# Reset game button
if st.sidebar.button("Reset Game"):
    st.session_state.messages = []
    st.session_state.game_state = "question"
    st.session_state.current_question = random.choice(would_you_rather_questions)
    st.session_state.rounds_played = 0
    st.session_state.user_choice = None
    st.session_state.opponent_choice = None
    st.rerun()