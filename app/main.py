import os
import streamlit as st
import yaml
import streamlit_authenticator as stauth
from views.pages.train_generator import TrainGeneratorPage
from dotenv import load_dotenv
from yaml.loader import SafeLoader


def env_constructor(loader, node):
    value = loader.construct_scalar(node)
    if value.startswith("${") and value.endswith("}"):
        env_var = value[2:-1]
    else:
        env_var = value
    return os.getenv(env_var, value)

load_dotenv()

yaml.add_constructor('!ENV', env_constructor, Loader=SafeLoader)

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login(
    fields={
        "Username": "Usuário",
        "Password": "Senha",
        "Login": "Entrar"
    }
)

if st.session_state['authentication_status'] is False:
    st.error("Usuário ou senha incorretos")
elif st.session_state['authentication_status'] is None:
    st.warning("Por favor, insira seu usuário e senha")
elif st.session_state['authentication_status']:
    st.write(f'Bem-vindo')
    (TrainGeneratorPage()).display()
    authenticator.logout("Sair")