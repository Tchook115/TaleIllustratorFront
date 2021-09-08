from pkg_resources import require
import streamlit as st
import time
from streamlit_folium import folium_static
import folium
import pandas as pd
import requests
from PIL import Image


url = 'http://127.0.0.1:8000/'

st.set_page_config(
    page_title="Once Upon A Time AI",  # => Quick reference - Streamlit
    page_icon="📖",
    layout="centered",  # wide
    initial_sidebar_state="auto")
'''
# Once Upon A Time AI

'''

def calque_merger(current_scene, new_scene):
    final = Image.new("RGBA", current_scene.size)
    final.paste(current_scene, (0, 0), current_scene)
    final.paste(new_scene, (0, 0), new_scene)
    return final

i = 0
size_image = (2560, 1600)


final = Image.new("RGBA", (2560, 1600))


content = st.text_input('Ask for a drawing', '')

message = {'message': content}



response = requests.get(url, params=message)

if content != '':
    size_image = eval(response.headers['size_image'])
    coordinates = eval(response.headers['coordinates'])
    image_data = response.content
    calque = Image.frombytes('RGBA', size_image, image_data)
    # st.image(image)
    final = calque_merger(final, calque)
    st.image(final)
