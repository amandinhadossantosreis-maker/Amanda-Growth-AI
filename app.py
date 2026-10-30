import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Amanda Growth AI", page_icon="📈", layout="wide")

st.title("📈 Amanda Growth AI")
st.caption("Painel inicial de crescimento orgânico para @homedaamandah")
st.info(
    "MVP inicial: os dados abaixo são editáveis e foram preenchidos com os números vistos nos prints. "
    "Ainda não há conexão automática com o Instagram. Use Insights oficiais para atualizar os dados."
)

with st.sidebar:
    st.header("⚙️ Dados do período")
    periodo = st.selectbox("Período dos Insights", ["Últimos 30 dias", "Últimos 14 dias", "Outro período"])
    seguidores = st.number_input("Seguidores atuais", min_value=0, value=1355, step=1)
    visualizacoes = st.number_input("Visualizações", min_value=0, value=252360, step=100)
    pct_nao_seguidores = st.slider("Visualizações de não seguidores (%)", 0.0, 100.0, 92.4, 0.1)
    interacoes = st.number_input("Interações com conteúdo", min_value=0, value=11420, step=10)
    contas_engajadas = st.number_input("Contas com engajamento", min_value=0, value=5872, step=10)
    visitas_perfil = st.number_input("Visitas ao perfil", min_value=0, value=922, step=1)
    toques_link = st.number_input("Toques em links externos", min_value=0, value=130, step=1)
    novos_seguidores = st.number_input("Seguidores ganhos no período (confirmar no Instagram)", min_value=0, value=245, step=1)
    dias_periodo = st.number_input("Quantidade de dias do período de seguidores", min_value=1, value=14, step=1)

nao_seguidor_views = round(visualizacoes * pct_nao_seguidores / 100)
taxa_visita = visitas_perfil / visualizacoes * 100 if visualizacoes else 0
taxa_interacao = interacoes / visualizacoes * 100 if visualizacoes else 0
taxa_visita_seguidor = novos_seguidores / visitas_perfil * 100 if visitas_perfil else 0
media_diaria = novos_seguidores / dias_periodo if dias_periodo else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Seguidores atuais", f"{seguidores:,}".replace(",", "."))
c2.metric("Visualizações", f"{visualizacoes:,}".replace(",", "."))
c3.metric("Visualizações de não seguidores", f"{nao_seguidor_views:,}".replace(",", "."))
c4.metric("Interações", f"{interacoes:,}".replace(",", "."))

c5, c6, c7, c8 = st.columns(4)
c5.metric("Visitas ao perfil", f"{visitas_perfil:,}".replace(",", "."))
c6.metric("Visita / visualização", f"{taxa_visita:.2f}%")
c7.metric("Interação / visualização", f"{taxa_interacao:.2f}%")
c8.metric("Média diária de seguidores*", f"{media_diaria:.1f}")

st.caption("*Estimativa baseada nos 245 seguidores mostrados pelo painel externo; confirme no Instagram se é ganho bruto ou crescimento líquido e se o período coincide.")

st.subheader("🔎 Diagnóstico inicial")
d1, d2 = st.columns(2)
with d1:
    st.markdown("**Oportunidade: converter alcance em visitas**")
    st.write(
        f"Com {pct_nao_seguidores:.1f}% das visualizações vindas de não seguidores, existe descoberta de público. "
        f"A taxa observada de visitas ao perfil é {taxa_visita:.2f} por 100 visualizações. "
        "Teste ganchos e CTAs que expliquem por que vale acompanhar a página."
    )
with d2:
    st.markdown("**Oportunidade: identificar formatos vencedores**")
    st.write(
        "Compare cada Reel por alcance, compartilhamentos, salvamentos, visitas ao perfil e seguidores atribuídos. "
        "Visualizações sozinhas não dizem qual vídeo trouxe seguidores."
    )

st.subheader("🏆 Conteúdos com mais visualizações")
default_posts = pd.DataFrame([
    {"Data": "03/10", "Tema": "Jogos que fazem todo mundo esquecer o celular", "Visualizações": 38000},
    {"Data": "23/10", "Tema": "Itens natalinos para decorar", "Visualizações": 23000},
    {"Data": "10/10", "Tema": "Jogos que fazem todo mundo esquecer o celular", "Visualizações": 17000},
    {"Data": "14/10", "Tema": "Montando o quarto dos meus filhos", "Visualizações": 12300},
    {"Data": "13/10", "Tema": "Minhas compras de viagem", "Visualizações": 9600},
])
edited_posts = st.data_editor(
    default_posts,
    num_rows="dynamic",
    use_container_width=True,
    column_config={"Visualizações": st.column_config.NumberColumn(min_value=0, step=100)}
)
if not edited_posts.empty:
    chart = px.bar(
        edited_posts.sort_values("Visualizações", ascending=True),
        x="Visualizações", y="Tema", color="Visualizações", orientation="h",
        title="Visualizações por conteúdo"
    )
    st.plotly_chart(chart, use_container_width=True)

st.subheader("🧪 Plano de testes para os próximos 7 dias")
tests = pd.DataFrame([
    {"Teste": "Repetir o tema jogos/família com um gancho novo", "Métrica principal": "Compartilhamentos e visitas ao perfil", "Status": "Planejar"},
    {"Teste": "Vídeo de achado útil com preço/benefício claro", "Métrica principal": "Salvamentos e cliques no perfil", "Status": "Planejar"},
    {"Teste": "CTA explicando o benefício de seguir a página", "Métrica principal": "Novos seguidores atribuídos", "Status": "Planejar"},
    {"Teste": "Sequência de Stories com enquete + recomendação", "Métrica principal": "Respostas e visitas ao perfil", "Status": "Planejar"},
])
st.dataframe(tests, hide_index=True, use_container_width=True)

st.warning(
    "Este painel não automatiza curtidas, comentários, seguidores ou ações em massa. "
    "A integração com a API oficial deve ser configurada separadamente, com autorização e permissões adequadas."
)
st.caption("Próxima etapa: importar métricas por publicação e comparar alcance, retenção, compartilhamentos, visitas e seguidores ganhos.")
