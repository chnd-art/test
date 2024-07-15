
import streamlit as st # type: ignore
from auth import login, logout, authenticator
#st.set_page_config(page_title='Security System',layout='wide')



# Initialize session state for authentication_status, name, logout, and username
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'name' not in st.session_state:
    st.session_state['name'] = None
if 'logout' not in st.session_state:
    st.session_state['logout'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Créer un widget de connexion
login()

if st.session_state["authentication_status"]:
        authenticator.logout(key='unique_key')

            
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.header('Security system using Face Recognition')

        with st.spinner("Loading Models and Conecting to Redis db ..."):
            import face_rec

        st.success('Model loaded successfully')
        st.success('Redis db successfully connected')

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
