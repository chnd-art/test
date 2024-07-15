import streamlit as st
#from Home import face_rec
import redis
import face_rec
from auth import login, logout, authenticator



if st.session_state["authentication_status"]:


    st.set_page_config(page_title='Reporting',layout='wide')
    st.subheader('Reporting')


# # Retrive logs data and show in Report.py
#  extract data from redis list
    name = 'attendance:logs'
    def load_logs(name,end=-1):
        logs_list = face_rec.r.lrange(name,start=0,end=end) # extract all data from the redis database
        return logs_list

# Connect to Redis Client
    hostname = 'redis-15463.c104.us-east-1-mz.ec2.redns.redis-cloud.com'
    portnumber = 15463
    password = 'QIVOlx9BN6OL2ZDRfOWQcQJL7YkPxVuG' 

    r = redis.StrictRedis(
                        host=hostname,
                        port=portnumber,
                        password=password,
                        decode_responses=False,
                        socket_timeout=20,
                        socket_connect_timeout=20)

# # tabs to show the info
    tab1, tab2 ,tab3 = st.tabs(['Registered Data','Logs','Delete User'])

    with tab1:
        if st.button('Refresh Data'):
            # Retrive the data from Redis Database
            with st.spinner('Retriving Data from Redis DB ...'):    
                redis_face_db = face_rec.retrive_data(name='academy:register')
                st.dataframe(redis_face_db[['Name','Role']])
            
    with tab2:
        if st.button('Refresh Logs'):
            st.write(load_logs(name=name))

    with tab3:
        st.subheader('Delete User')

    # Collecte du nom de la personne et du rôle pour la suppression
        def collect_delete_info():
            person_name_to_del = st.text_input(label='Name ', placeholder='First & Last Name')
            role_to_del = st.selectbox(label='Role ', options=('Student', 'Teacher', 'Administrative staff'))
            return person_name_to_del, role_to_del

        person_name_to_del, role_to_del = collect_delete_info()
        key_to_del = f"{person_name_to_del}@{role_to_del}"

        if st.button('Delete'):
            if person_name_to_del and role_to_del:
                if r.hdel('academy:register', key_to_del):
                    st.success(f"User '{key_to_del}' deleted successfully.")
                else:
                    st.error(f"User '{key_to_del}' not found in database.")
            else:
                st.error('Please enter a valid name and select a role.')

else:
    st.warning('You need to log in to access this page.')
