import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
from PIL import Image
import io



def promopt(prompt, img):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, img])

    return response.text

def process_image(st_image):
    # Ensure the image is a Streamlit
    image_data = st_image.read()
    process_image = Image.open(io.BytesIO(image_data))

    return process_image

if __name__ == '__main__':

    load_dotenv(find_dotenv(), override=True)

    API_key = os.environ.get('GOOGLE_API_KEY')
    genai.configure(api_key=API_key)

    img_width = 90  # Adjust the width as needed

    # Center the image using Streamlit layout options
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column widths as needed
    with col1:
        st.image('logo.png', width=img_width)
        st.header('ImageGem')

    img = st.file_uploader('Drop an Image', type=['jpg', 'png', 'jpeg', 'gif'])
    if img:
        st.image(img, caption='Talk with the Image')
        prompt = st.text_input("What you want to ask")

        if prompt:
            processed_image = process_image(img)
            with st.spinner('Running ...'):
                answer =  promopt(prompt, processed_image)
                st.text_area('Gemini Answer: ', value=answer)

            st.divider()

            if 'history' not in st.session_state:
                st.session_state.history = ''

            value = f'Q: {prompt} \n\n A: {answer}'
            st.session_state.history = f'{value} \n\n {"-" * 100} \n\n {st.session_state.history}'

            h = st.session_state.history
            st.text_area(label='Chat History', value=h, height=400, key='history')





