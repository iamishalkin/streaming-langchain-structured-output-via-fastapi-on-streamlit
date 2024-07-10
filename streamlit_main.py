import streamlit as st
import httpx
import json

st.title('Streaming FastAPI LLM demo')

button = st.button('Start streaming')




url = "http://127.0.0.1:8000/stream_biographies/"
data = {"persons": 10}

headers = {"Content-type": "application/json",
           'accept': 'application/json'}


if button:
    with httpx.stream('POST', url, params=data, headers=headers) as r:
        containers = {}
        for chunk in r.iter_text():
            chunk = json.loads(chunk)
            bios = chunk.get('biographies', [{}])
            for idx, bio in enumerate(bios):
                if idx not in containers:
                    print(idx)
                    containers[idx] = st.empty()
                with containers[idx].container():
                    st.write(f"Biography of {bio.get('name', '')} {bio.get('surname', '')}, "
                             f"born in {bio.get('birth_place', '')}")
                    st.write(bio.get('biography', ''))

