
import json
import requests  
import streamlit as st  
from streamlit_lottie import st_lottie  

st.title('Contacto')

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()    
    
lottie_linkedin = load_lottieurl("https://lottie.host/5ad65db4-1d92-4c8d-8732-8e6bd2f905fb/1NgfhDZBlu.json")
lottie_instagram = load_lottieurl("https://lottie.host/57b5f64c-a3e3-4015-a99e-e31d686041b3/wOn8trrktW.json")

instagram_url = "https://www.instagram.com/spb_engineering_ec"
linkedin_url = "https://www.linkedin.com/in/silvia-pinto-bernabé-894a91165"

col1, col2 = st.columns(2)
with col1:
    st_lottie(lottie_linkedin, speed=1, reverse=False, loop=True, quality="medium", height=50, width=50, key=None) 
    st.markdown(f"<a href='{linkedin_url}' style='font-size: 20px; color: #4078c0; margin-right: 100px;'>Sigueme en LinkedIn</a>", unsafe_allow_html=True)

with col2:
    st_lottie(lottie_instagram, speed=1, reverse=False, loop=True, quality="medium", height=50, width=50, key=None)
    st.markdown(f"<a href='{instagram_url}' style='font-size: 20px; color: #4078c0; margin-right: 100px;'>Sigueme en Instagram</a>", unsafe_allow_html=True)

  
   
    
    