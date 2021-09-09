from pkg_resources import require
import streamlit as st
import time
from streamlit_folium import folium_static
import folium
import pandas as pd
import requests
from PIL import Image
import os, shutil

st.set_page_config( #
    page_icon="📖",
    page_title='Once Upon a Time AI',
    layout="wide",# "centered"
    initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center; margin-top: -70px, margin-bottom: 70px;'>Once Upon A Time AI</h1>", unsafe_allow_html=True)

backgd = "bg_prairie.png"
backgd2 = "bg_underwater.png"

def reset_scene():
    folder = './current_draw'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def send_request(content):
    url = 'http://127.0.0.1:8000/'
    message = {'message': content}
    response = requests.get(url, params=message)
    image_data = response.content
    calque = Image.frombytes('RGBA', (2560,1600), image_data)
    return calque

def calque_merger(current_scene, new_scene):
    print(f'current : {current_scene},\nnew : {current_scene}')
    final = Image.new("RGBA", current_scene.size)
    final.paste(current_scene, (0, 0), current_scene)
    final.paste(new_scene, (0, 0), new_scene)
    return final

def formulaire():
    with st.form(key='my_form'):
        text_input = st.text_input(label='Enter some text')
        submit_button = st.form_submit_button(label='Submit')
    return text_input

# Initialiser les variables persistentes
if 'pathtofolder' not in st.session_state:
    st.session_state.pathtofolder = "backgrounds"
if 'current_scene' not in st.session_state:
    st.session_state.current_scene = backgd
if 'previous_scene' not in st.session_state:
    st.session_state.previous_scene = st.session_state.current_scene
if 'iter' not in st.session_state:
    st.session_state.iter = 1

def mainy(nouvelle_scene):
    # generer la nouvelle image
    nom_nouvelle_image = str('img'+str(st.session_state.iter)+'.png')
    st.session_state.iter += 1
    if st.session_state.iter != 1:
        st.session_state.pathtofolder = "current_draw"
    #stocker son chemin
    st.session_state.current_scene = nom_nouvelle_image
    path_nouvelle_image = os.path.join(".", st.session_state.pathtofolder, st.session_state.current_scene)
    
    st.session_state.previous_scene = nom_nouvelle_image

col1, col2, col3 = st.columns([1,6,1])
with col1:
    st.write("")
with col2:
    form = formulaire()
    path_image_actuelle = os.path.join("." ,st.session_state.pathtofolder , st.session_state.previous_scene)
    nouvelle_scene = calque_merger(Image.open(path_image_actuelle), send_request(form))
    mainy(nouvelle_scene)
    nouvelle_scene.save(path_nouvelle_image)
    st.image(nouvelle_scene, caption=None, width=None, use_column_width=None, clamp=False, channels='RGB', output_format='auto')
    my_expander = st.expander('',expanded=True)
    with my_expander:
        pass
        
with col3:
    st.write("")


#######################################
st.set_page_config( #
    page_icon="📖",
    page_title='Once Upon a Time AI',
    layout="wide",# "centered"
    initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center; margin-top: -70px, margin-bottom: 70px;'>Once Upon A Time AI</h1>", unsafe_allow_html=True)

def formulaire():
    with st.form(key='my_form'):
        text_input = st.text_input(label='Enter some text')
        submit_button = st.form_submit_button(label='Submit')
    return text_input

col1, col2, col3 = st.columns([1,6,1])
with col1:
    st.write("")
with col2:
    path = './backgrounds/bg_prairie.png'
    scene = Image.open(path)
    st.image(scene, caption=None, width=None, use_column_width=None, clamp=False, channels='RGB', output_format='auto')
    my_expander = st.expander('',expanded=True)
    with my_expander:
        clicked = formulaire()
with col3:
    st.write("")










# def save_image(calque):
#     st.session_state.iter += 1
#     path_to_current_image = os.path.join("." ,st.session_state.pathtofolder , st.session_state.previous_scene)
#     new_scene = calque_merger(Image.open(path_to_current_image), calque)
#     st.session_state.pathtofolder = "current_draw"
#     image_name = str('img'+str(st.session_state.iter)+'.png')
#     IMAGES_PATH = os.path.join(".", st.session_state.pathtofolder,image_name)
#     calque.save(IMAGES_PATH)
#     return image_name



# def drawit(clicked): 
#     new_calque = send_request(clicked)
#     st.session_state.previous_scene = st.session_state.current_scene
#     st.session_state.current_scene = save_image(new_calque)
