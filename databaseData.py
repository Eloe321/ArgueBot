import streamlit as st
from google.cloud import firestore
import json

from google.cloud.firestore import Client
from google.oauth2 import service_account

@st.experimental_singleton
def get_db():
    key_dict = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_json('key.json')
    return db
