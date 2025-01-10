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
        if 'current_tab' not in st.session_state:
            st.session_state.current_tab = 1

    def append_user_train(self, **kwargs):
        st.session_state['user_train'] = dict(kwargs)
        st.session_state.current_tab = 3
        st.rerun()
        
    def append_user_data(self, **kwargs):
        st.session_state['user_data'] = dict(kwargs)
        st.session_state.current_tab = 2
        st.rerun()

    def __generate_response(self, input_text):
        model_response = self.__llm_service.invoke(input_text) 
        return model_response

    def display(self):
        st.title("🦜 Automated Training Build App")

        if st.session_state.current_tab == 1:
            st.header("Etapa 1: Preencha a Anamnese")
            self.__anamnese_form.display()
        
        elif st.session_state.current_tab == 2:
            st.header("Etapa 2: Preencha os Detalhes do Treino")
            self.__train_form.display()
                
        elif st.session_state.current_tab == 3:
            st.header("Etapa 3:  Revisão e Geração do Treino")
            if st.session_state.user_data and st.session_state.user_train:
                st.title("Resumo do Treino")
                st.markdown("### Informações Gerais do Treino")
                st.markdown(f"- **Tempo de Treino:** {st.session_state.user_train['tempo_treino']}")
                st.markdown(f"- **Intensidade do Treino:** {st.session_state.user_train['intensidade_treino']}")
                st.markdown(f"- **Duração do Treino:** {st.session_state.user_train['duracao_treino']}")
                st.markdown(f"- **Local de Treino:** {st.session_state.user_train['local_treino']}")
                st.markdown(f"- **Quantidade Média de Exercícios:** {st.session_state.user_train['quantidade_media_exercicios']}")
                st.markdown(f"- **Descrição do Treino:** {st.session_state.user_train['descricao_treino'] or 'Não fornecida'}")
                st.markdown("### Tipos de Treino")
                if st.session_state.user_train["tipo_treino"]:
                    for t in st.session_state.user_train["tipo_treino"]:
                        st.markdown(f"- {t}")
                else:
                    st.markdown("- Nenhum tipo de treino selecionado")

                st.markdown("### Grupos Musculares Focados")
                if st.session_state.user_train["grupo_muscular"]:
                    for gm in st.session_state.user_train["grupo_muscular"]:
                        st.markdown(f"- {gm}")
                else:
                    st.markdown("- Nenhum grupo muscular selecionado")                

                st.title("Informações do Aluno")
                st.markdown("### Detalhes do Aluno")
                st.markdown(f"- **Idade:** {st.session_state.user_data['idade']} anos")
                st.markdown(f"- **Altura:** {st.session_state.user_data['altura']} m")
                st.markdown(f"- **Peso:** {st.session_state.user_data['peso']} kg")
                st.markdown(f"- **Sexo:** {st.session_state.user_data['sexo']}")
                st.markdown(f"- **Observações:** {st.session_state.user_data['observacoes'] or 'Não fornecido'}")
                        
                if st.button("💡 Gerar Treino"):
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
                        st.error(f"Ocorreu um erro ao processar a resposta. Por favor procurar o Rafael Carvalho.")
                if st.button("⭐ Novo Protocolo"):
                    st.session_state.current_tab = 1
                    st.rerun()
            else:
                st.error("Dados insuficientes.")