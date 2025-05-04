from openai import OpenAI
import streamlit as st

class AIDebater:
    def __init__(self):
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    def generate_debate_response(self, user_choice, opponent_choice):
        prompt = f"""
        The user has chosen they would rather {user_choice} in a 'Would You Rather' game.
        You should playfully and persuasively argue why {opponent_choice} would actually be the better choice.
        Be creative, entertaining, and use humor while making compelling points about why their choice isn't as good as they think.
        Keep your response concise (3-5 sentences).
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        
        return response.choices[0].message.content