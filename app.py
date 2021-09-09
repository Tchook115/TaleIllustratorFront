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
    final1 = Image.new("RGBA", current_scene.size)
    final1.paste(current_scene, (0, 0), current_scene)
    final1.paste(new_scene, (0, 0), new_scene)
    return final1


size_image = (2560, 1600)

f = open("init.txt", "r")
param=f.read()
f.close()


if param:
    final = Image.new("RGBA", (2560, 1600))
else:
    final = Image.open('calque.png')

f = open("init.txt", "w")
f.write("param = False")
f.close()

content = st.text_input('Ask for a drawing', '')

message = {'message': content}

response = requests.get(url, params=message)
st.text(response.headers)

if content != '':
    if response.headers['content-type'] == 'application/json':
        txt = eval(response.content.decode("utf-8")).get('text')
        st.text(txt)
    else:
        size_image = eval(response.headers['size_image'])
        coordinates = eval(response.headers['coordinates'])
        image_data = response.content
        calque = Image.frombytes('RGBA', size_image, image_data)
        # st.image(image)
        final = calque_merger(final, calque)
        st.image(final)
        final.save("calque.png")
# st.experimental_set_query_params(final=final)
