import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator.utilities.exceptions import (CredentialsError,
                                                          ForgotError,
                                                          LoginError,
                                                          RegisterError,
                                                          ResetError,
                                                          UpdateError)

# Charger la configuration
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialiser l'authentificateur
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

def login():
    try:
        authenticator.login()
    except LoginError as e:
        st.error(e)

def logout():
    authenticator.logout(key='unique_key')
