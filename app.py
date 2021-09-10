import streamlit as st
import requests
from PIL import Image
import streamlit.components.v1 as components
# config
st.set_page_config( #
    page_icon="📖",
    layout="wide",# "centered"
    initial_sidebar_state="collapsed")

# CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css('style.css')
st.markdown("<h1 style='text-align: center; margin-top: -70px; margin-bottom: 70px;'>Once Upon A Time AI</h1>", unsafe_allow_html=True)

#variables
url = 'https://ouatai30-qlhq5xa3oq-ew.a.run.app'
size_image = (2560, 1600)
user_input = None
txt = ''
# si on n'a rien dans le cache intanciation vide
if 'utterances' not in st.session_state:
    st.session_state['utterances'] = ''
# si on n'a pas d'image dans le cache, instanciation à image vide
if 'image' not in st.session_state:
    st.session_state['image'] = True
    image = Image.open('./backgrounds/bg_prairie.png')
    image.save('current_draw/frame.png')
# contruction de l'image depuis l'API
def get_image(message):
    if message != '':
        params = {'message': message}
        response = requests.get(url, params=params)
        if response.headers['content-type'] == 'application/json':
            global txt
            txt = eval(response.content.decode("utf-8")).get('text')
            return Image.open('current_draw/frame.png')
        else:
            if response.status_code == 200:
                image_data = response.content
                calque = Image.frombytes('RGBA', size_image, image_data)
                image = Image.open('current_draw/frame.png')
                image.paste(calque, (0,0), calque)
                image.save('current_draw/frame.png')
    return Image.open('current_draw/frame.png')
# mise dans le cache de la recherche
def get_text():
    utterance = st.text_input('', value = '')
    st.session_state['utterances'] = utterance
    return utterance

def formulaire():
    with st.form(key='my_form'):
        text_input = st.text_input(label='Enter some text')
        submit_button = st.form_submit_button(label='Submit')
    return text_input

col1, col2, col3 = st.columns([2, 8, 2])
with col2:
    user_input = formulaire()
    # affichage de l'image
    st.image(get_image(user_input), use_column_width=True)
    st.container()
    st.text(txt)
