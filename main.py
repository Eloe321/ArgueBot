import streamlit as st
import auth_functions

from game_logic import WouldYouRatherGame
from ai_handler import AIDebater
from session_manager import SessionManager


def handle_choice(ai_debater, choice, alternative):
    st.session_state.user_choice = choice
    st.session_state.opponent_choice = alternative
    st.session_state.game_state = "debate"
    
    ai_response = ai_debater.generate_debate_response(choice, alternative)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

def new_round(game):
    st.session_state.current_question = game.get_random_question()
    st.session_state.game_state = "question"
    st.session_state.user_choice = None
    st.session_state.opponent_choice = None
    st.session_state.rounds_played += 1

def main():
    ## -------------------------------------------------------------------------------------------------
    ## Not logged in -----------------------------------------------------------------------------------
    ## -------------------------------------------------------------------------------------------------
    if not auth_functions.check_session():
        col1,col2,col3 = st.columns([1,2,1])

        # Authentication form layout
        do_you_have_an_account = col2.selectbox(label='Do you have an account?',options=('Yes','No','I forgot my password'))
        auth_form = col2.form(key='Authentication form',clear_on_submit=False)
        email = auth_form.text_input(label='Email')
        password = auth_form.text_input(label='Password',type='password') if do_you_have_an_account in {'Yes','No'} else auth_form.empty()
        auth_notification = col2.empty()

        # Sign In
        if do_you_have_an_account == 'Yes' and auth_form.form_submit_button(label='Sign In',use_container_width=True,type='primary'):
            with auth_notification, st.spinner('Signing in'):
                auth_functions.sign_in(email,password)

        # Create Account
        elif do_you_have_an_account == 'No' and auth_form.form_submit_button(label='Create Account',use_container_width=True,type='primary'):
            with auth_notification, st.spinner('Creating account'):
                auth_functions.create_account(email,password)

        # Password Reset
        elif do_you_have_an_account == 'I forgot my password' and auth_form.form_submit_button(label='Send Password Reset Email',use_container_width=True,type='primary'):
            with auth_notification, st.spinner('Sending password reset link'):
                auth_functions.reset_password(email)

        # Authentication success and warning messages
        if 'auth_success' in st.session_state:
            auth_notification.success(st.session_state.auth_success)
            del st.session_state.auth_success
        elif 'auth_warning' in st.session_state:
            auth_notification.warning(st.session_state.auth_warning)
            del st.session_state.auth_warning

    ## -------------------------------------------------------------------------------------------------
    ## Logged in --------------------------------------------------------------------------------------
    ## -------------------------------------------------------------------------------------------------
    else:

        # Initialize components
        game = WouldYouRatherGame()
        ai_debater = AIDebater()
        SessionManager.initialize_session_state(game)

        # App title
        st.title("Would You Rather: AI Debate Edition")
        st.write("Choose an option, and the AI will debate why the other option is better!")

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Game logic
        if st.session_state.game_state == "question":
            st.write("## Would you rather...")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"A: {st.session_state.current_question['option_a']}"):
                    handle_choice(
                        ai_debater,
                        st.session_state.current_question['option_a'],
                        st.session_state.current_question['option_b']
                    )
            
            with col2:
                if st.button(f"B: {st.session_state.current_question['option_b']}"):
                    handle_choice(
                        ai_debater,
                        st.session_state.current_question['option_b'],
                        st.session_state.current_question['option_a']
                    )

        elif st.session_state.game_state == "debate":
            if prompt := st.chat_input("Your response?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                new_round(game)
                st.rerun()

        # Sidebar
        st.sidebar.write(f"Rounds played: {st.session_state.rounds_played}")
        if st.sidebar.button("Reset Game"):
            SessionManager.reset_game(game)
            st.rerun()

if __name__ == "__main__":
    main()