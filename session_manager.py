import streamlit as st

class SessionManager:
    @staticmethod
    def initialize_session_state(game):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "game_state" not in st.session_state:
            st.session_state.game_state = "question"
        if "current_question" not in st.session_state:
            st.session_state.current_question = game.get_random_question()
        if "user_choice" not in st.session_state:
            st.session_state.user_choice = None
        if "opponent_choice" not in st.session_state:
            st.session_state.opponent_choice = None
        if "rounds_played" not in st.session_state:
            st.session_state.rounds_played = 0

    @staticmethod
    def reset_game(game):
        st.session_state.messages = []
        st.session_state.game_state = "question"
        st.session_state.current_question = game.get_random_question()
        st.session_state.rounds_played = 0
        st.session_state.user_choice = None
        st.session_state.opponent_choice = None