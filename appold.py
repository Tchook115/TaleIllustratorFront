from pkg_resources import require
import streamlit as st
import time
from streamlit_folium import folium_static
import folium
import pandas as pd
import requests
from PIL import Image

url = 'https://ouatai12-qlhq5xa3oq-ew.a.run.app'
backgnd_list = ['Windows XP', 'Underwater']

backgd = Image.open('./backgrounds/bg_prairie.png')
backgd2 = Image.open('./backgrounds/bg_underwater.png')

def calque_merger(current_scene, new_scene):
    final = Image.new("RGBA", current_scene.size)
    final.paste(current_scene, (0, 0), current_scene)
    final.paste(new_scene, (0, 0), new_scene)
    return final

size_image = (2560, 1600)
final = Image.new("RGBA", (2560, 1600))

def send_request(content):
    message = {'message': content}
    response = requests.get(url, params=message)
    image_data = response.content
    scene = Image.frombytes('RGBA', size_image, image_data)

###########
## FRONT ##
###########

st.set_page_config( #
    page_icon="📖",
    page_title='Once Upon a Time AI',
    layout="wide",# "centered"
    initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center; margin-top: -70px, margin-bottom: 70px;'>Once Upon A Time AI</h1>", unsafe_allow_html=True)

backgd = './backgrounds/bg_prairie.png'
backgd2 = './backgrounds/bg_underwater.png'

if 'calque' not in st.session_state:
    st.session_state['calque'] = backgd
    print(st.write(st.session_state.calque))
def change_scene():
    st.session_state.scene = backgd2

st.button('Increment', on_click=change_scene)

def formulaire():
    with st.form('Form1'):
        st.text_input('')
        submitted1 = st.form_submit_button('Draw it!', on_click=change_scene)
    return submitted1

col1, col2, col3 = st.columns([1,6,1])
with col1:
    st.write("")
with col2:
    path = st.write(st.session_state.calque)
    scene = Image.open(path)
    st.image(scene, caption=None, width=None, use_column_width=None, clamp=False, channels='RGB', output_format='auto')
    my_expander = st.expander('',expanded=True)
    with my_expander:
        clicked = formulaire()
with col3:
    st.write("")

add_selectbox = st.sidebar.selectbox('Background displayed',backgnd_list)
add_resetbutton = st.sidebar.button('Reset scene', key=None, help=None, on_click=None)

#with st.form(key='my_form'):
#	text_input = st.text_input(label='Ask for a drawing')
#	submit_button = st.form_submit_button(label='Submit')

#if content != '':
#    size_image = eval(response.headers['size_image'])
#    coordinates = eval(response.headers['coordinates'])
#    image_data = response.content
#    calque = Image.frombytes('RGBA', size_image, image_data)
#    # st.image(image)
#    final = calque_merger(final, calque)
#    st.image(final)
