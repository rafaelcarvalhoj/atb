import json
import streamlit as st
import pandas as pd
from views.components.anamnese_form import AnamneseForm
from views.components.train_form import TrainForm
from services.llm import LlmService

class TrainGeneratorPage:
    def __init__(self):
        self.__llm_service = LlmService(model="llama-3.3-70b-versatile")
        self.__anamnese_form = AnamneseForm("anamnese", callback=self.append_user_data)
        self.__train_form = TrainForm("train", callback=self.append_user_train)
        if 'user_data' not in st.session_state:
            st.session_state.user_data = None
        if 'user_train' not in st.session_state:
            st.session_state.user_train = None

    def append_user_train(self, **kwargs):
        st.session_state['user_train'] = dict(kwargs)
        
    def append_user_data(self, **kwargs):
        st.session_state['user_data'] = dict(kwargs)

    def __generate_response(self, input_text):
        model_response = self.__llm_service.invoke(input_text) 
        return model_response

    def display(self):
        st.title("🦜 Automated Training Build App")

        tabs = st.tabs(["1. Anamnese", "2. Preencher Treino", "3. Resumo"])
        
        with tabs[0]:
            st.header("Etapa 1: Preencha a Anamnese")
            self.__anamnese_form.display()
        
        with tabs[1]:
            st.header("Etapa 2: Preencha os Detalhes do Treino")
            self.__train_form.display()
                
        with tabs[2]:
            st.header("Etapa 3: Resumo dos dados")
            if st.session_state.user_data and st.session_state.user_train:
                st.subheader("Informações do Treino:")
                st.markdown(f"**Treino:**")
                st.json(st.session_state.user_train)
                
                st.subheader("Informações do Aluno:")
                st.markdown(f"**Aluno:**")
                st.json(st.session_state.user_data)
                if st.button("💡Gerar Treino"):
                    print("gerando treino...")
                    prompt = ""
                    with open("./app/utils/prompts/sample_04.txt", "r") as f:
                        prompt_content = f.read()
                    
                    
                    prompt = prompt_content.format(**st.session_state.user_train, **st.session_state.user_data)
                    chat = self.__generate_response(prompt)
                    raw_response = list(chat)[0][1]
                    cleaned_response = str(
                        raw_response
                        .replace("```json", "")
                        .replace("```", "")
                        .strip()
                    )
                    
                    try:
                        data = json.loads(cleaned_response)
                        for index, train in enumerate(data["structured"]):
                            columns = ["Exercício", "Séries", "Repetições", "Orientações"]
                            st.markdown(f"## Treino {index+1}")
                            train_data = []
                            for exercice in train:
                                train_data.append([
                                    exercice.get("name", ""),
                                    exercice.get("series", ""),
                                    exercice.get("reps", ""),
                                    exercice.get("orientations", "")
                                ])
                            st.table(pd.DataFrame(train_data, columns=columns))
                            st.divider()
                    except Exception as e:
                        st.error(f"Ocorreu um erro ao processar a resposta: {e}")
            else:
                st.error("Dados insuficientes.")