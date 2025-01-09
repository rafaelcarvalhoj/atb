import streamlit as st

class AnamneseForm:
    def __init__(self, form_id: str, title: str = "Anamnese do Aluno", callback = None):
        self.__form_id = form_id
        self.__title = title
        self.callback = callback
        
    def display(self) -> dict | None:
        with st.form(self.__form_id):
            st.title(self.__title)
            form_2c_left, form_2c_right = st.columns(2)
            idade = form_2c_left.number_input("Idade", step = 1, value=20)
            altura = form_2c_left.number_input("Altura", 1.0, 2.5, value=1.70)
            peso = form_2c_right.slider("Peso (kg)", 30.0, 150.0, 75.0)
            sexo = form_2c_right.radio("Sexo", options=["Homem", "Mulher"])
            observacoes = st.text_area(
                "Observações", 
                placeholder="Descreva observações médicas, lesões, dores, histórico hospitalar e etc."
                )

            submitted = st.form_submit_button("Salvar")
            
            if submitted:
                form_data = {
                    'idade': idade,
                    'altura': altura,
                    'peso': peso,
                    'sexo': sexo,
                    'observacoes': observacoes
                }
                if self.callback:
                    self.callback(**form_data)
                return form_data