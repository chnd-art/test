import streamlit as st
import os
from PIL import Image
#from Home import face_rec
from zipfile import ZipFile
import tempfile
import io
from auth import login, logout, authenticator



if st.session_state["authentication_status"]:


        st.set_page_config(page_title='Reporting',layout='wide')
        st.subheader('Reporting')

        def show_report():
            st.title("Report of Unrecognized Faces")
            if os.path.exists('unrecognized_faces/report.txt'):
                with open('unrecognized_faces/report.txt', 'r') as f:
                    lines = f.readlines()
                    unique_images = []  # List to store unique file paths
                    for line in reversed(lines):  # Read lines in reverse order
                        file_path, timestamp = line.strip().split(',')
                        if file_path not in [image['file_path'] for image in unique_images]:
                            unique_images.append({'file_path': file_path, 'timestamp': timestamp})
                
                # Display the images in reverse order (LIFO)
                    for image in unique_images:
                        st.image(image['file_path'], caption=f"Time: {image['timestamp']}", width=200)
            else:
                st.write("No unrecognized faces recorded.")


        def create_html_report():
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Unrecognized Faces Report</title>
            </head>
            <body>
                <h1>Unrecognized Faces Report</h1>
            """
            if os.path.exists('unrecognized_faces/report.txt'):
                with open('unrecognized_faces/report.txt', 'r') as f:
                    lines = f.readlines()
                    unique_images = []  # List to store unique file paths
                    for line in reversed(lines):  # Read lines in reverse order
                        file_path, timestamp = line.strip().split(',')
                        if file_path not in [image['file_path'] for image in unique_images]:
                            unique_images.append({'file_path': file_path, 'timestamp': timestamp})
                
                # Add images to HTML content
                    for image in unique_images:
                        html_content += f'<div><img src="{image["file_path"]}" width="200"><p>Time: {image["timestamp"]}</p></div>'

            html_content += """
            </body>
            </html>
            """

            return html_content

        def create_zip_report():
            with tempfile.TemporaryDirectory() as tmpdirname:
                html_content = create_html_report()
                html_path = os.path.join(tmpdirname, "report.html")
                with open(html_path, 'w') as f:
                    f.write(html_content)
            
                zip_buffer = io.BytesIO()
                with ZipFile(zip_buffer, 'w') as zipf:
                    # Add HTML report to zip
                    zipf.write(html_path, "report.html")
                    # Add images to zip
                    if os.path.exists('unrecognized_faces/report.txt'):
                        with open('unrecognized_faces/report.txt', 'r') as f:
                            lines = f.readlines()
                            for line in lines:
                                file_path, timestamp = line.strip().split(',')
                                if os.path.exists(file_path):
                                    zipf.write(file_path)
            
                zip_buffer.seek(0)
                return zip_buffer

        def download_report():
            zip_buffer = create_zip_report()
            st.download_button(
                label="Download Report",
                data=zip_buffer,
                file_name="unrecognized_faces_report.zip",
                mime="application/zip"
            )


        def delete_report():
            if os.path.exists('unrecognized_faces/report.txt'):
                os.remove('unrecognized_faces/report.txt')
                st.write("Report deleted.")
            else:
                st.write("No report to delete.")
        # Also remove images
            for file in os.listdir('unrecognized_faces'):
                file_path = os.path.join('unrecognized_faces', file)
                if os.path.isfile(file_path):
                    os.remove(file_path)



# Create the tabs
     
        tab1, tab2 ,tab3 = st.tabs(['Refresh Data',' Download Report','Delete Report'])



# Place the buttons within the first tab
        with tab1:
            if st.button('Refresh data'):
            # Call the function to show the report when the button is clicked
                show_report()
        with tab2:
        #     if st.button('Download Report'):
                download_report()
        with tab3:
            if st.button('Delete Report'):
                delete_report()
        

else:
    st.warning('You need to log in to access this page.')
