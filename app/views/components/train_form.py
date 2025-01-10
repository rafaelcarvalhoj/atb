import streamlit as st

muscle_groups = {
    "Região Superior": {
        "Peitoral": ["Peitoral maior", "Peitoral menor"],
        "Costas": ["Latíssimo do dorso", "Trapézio", "Rombóides maior", "Rombóides menor", "Eretor da espinha (parte superior)"],
        "Ombros": ["Deltoide anterior", "Deltoide medial", "Deltoide posterior", "Supraespinhal", "Infraespinhal", "Redondo maior", "Redondo menor"],
        "Braços": ["Bíceps braquial", "Braquial", "Tríceps braquial", "Braquiorradial"]
    },
    "Região Central (Core)": {
        "Abdômen": ["Reto abdominal", "Oblíquo externo", "Oblíquo interno", "Transverso abdominal"],
        "Lombar": ["Quadrado lombar", "Eretor da espinha (parte inferior)"]
    },
    "Região Inferior": {
        "Quadril e Glúteos": ["Glúteo máximo", "Glúteo médio", "Glúteo mínimo", "Psoas maior", "Psoas menor", "Íliaco"],
        "Coxas": {
            "Quadríceps femoral": ["Reto femoral", "Vasto lateral", "Vasto medial", "Vasto intermédio"],
            "Isquiotibiais": ["Bíceps femoral", "Semitendinoso", "Semimembranoso"],
            "Adutores": ["Adutor longo", "Adutor curto", "Adutor magno", "Grácil", "Pectíneo"]
        },
        "Panturrilhas": ["Gastrocnêmio (parte medial)", "Gastrocnêmio (parte lateral)", "Sóleo", "Tibial anterior", "Tibial posterior", "Fibular longo", "Fibular curto"]
    }
}

class TrainForm:
    def __init__(self, form_id: str, title: str = "Treino", callback = None):
        self.__form_id = form_id
        self.__title = title
        self.callback = callback
            
    def display(self) -> dict | None:
        with st.form(self.__form_id):
            st.title(self.__title) 
            col1, col2 = st.columns(2)

            with col1:
                tempo_treino = st.radio(
                    "**Tempo de treino**", 
                    options=[
                        "Nunca treinou",
                        "Menos de um ano",
                        "Entre um e dois anos",
                        "Entre dois e quatro anos",
                        "Quatro anos ou mais"
                        ]
                    )
                
                intensidade = st.radio(
                "**Intensidade do Treino**",
                options=[
                    "Leve",
                    "Moderada",
                    "Alta"
                    ]
                )
            with col2:
                st.write("**Duração do Treino**")
                duracao_horas = st.number_input("Horas", 0, 5, 1, 1)
                duracao_minutos = st.number_input("Minutos", 0, 59, 30, 1)
                
            tipo_treino = st.multiselect(
                "Tipo de Treino", 
                options=[
                    "Hipertrofia",
                    "Emagrecimento", 
                    "Cardiovascular", 
                    "Funcional"
                    ],
                placeholder="Selecione o(s) tipo(s) de treino...",
                default="Hipertrofia"
                )
            local_treino = st.selectbox(
                "Local de Treino",
                options=[
                    "Casa",
                    "Academia",
                    "Rua",
                    "Box Crossfit"
                    ],
                placeholder="Esolha um local de treino",
                index=1
                )
                
            quantidade_media_exercicios = st.number_input("Quantidade média de exercícios no treino",1,20,5,1)

            st.markdown("### Seleção de Grupos Musculares")
            
            all_muscles = []
            for region, groups in muscle_groups.items():
                for group, muscles in groups.items():
                    if isinstance(muscles, list):
                        all_muscles.extend(muscles)
                    elif isinstance(muscles, dict):
                        for sub_group, sub_muscles in muscles.items():
                            all_muscles.extend(sub_muscles)
            
            all_muscles = sorted(all_muscles) 
            
            grupo_muscular = st.multiselect(
                "Grupos Musculares",
                placeholder="Selecione os grupos musculares desejados",
                options=all_muscles,
                help="Use a barra de busca para encontrar facilmente os músculos desejados."
            )
            
            descricao_treino = st.text_area("**Dê uma descrição geral do treino**")            
            
            submitted = st.form_submit_button("➡️ Próximo")
                                        
            if submitted:
                form_data = {
                    'tempo_treino': tempo_treino,
                    'intensidade_treino': intensidade,
                    'duracao_treino': f"{duracao_horas} hora e {duracao_minutos} minutos",
                    'tipo_treino': tipo_treino,
                    'local_treino': local_treino,
                    'grupo_muscular': grupo_muscular,
                    'quantidade_media_exercicios': quantidade_media_exercicios,
                    'descricao_treino': descricao_treino
                }
                if self.callback:
                    self.callback(**form_data)
                return form_data