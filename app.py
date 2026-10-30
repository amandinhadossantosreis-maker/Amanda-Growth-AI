import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Amanda Growth AI", page_icon="📈", layout="wide")
st.title("📈 Amanda Growth AI")
st.caption("Assistente de crescimento orgânico para @homedaamandah")

with st.sidebar:
    st.header("⚙️ Dados do período")
    periodo = st.selectbox("Período dos Insights", ["Últimos 30 dias", "Últimos 14 dias", "Outro período"])
    seguidores = st.number_input("Seguidores atuais", min_value=0, value=1355, step=1)
    visualizacoes = st.number_input("Visualizações", min_value=0, value=252360, step=100)
    pct_nao_seguidores = st.slider("Visualizações de não seguidores (%)", 0.0, 100.0, 92.4, 0.1)
    interacoes = st.number_input("Interações com conteúdo", min_value=0, value=11420, step=10)
    visitas_perfil = st.number_input("Visitas ao perfil", min_value=0, value=922, step=1)
    novos_seguidores = st.number_input("Seguidores ganhos no período (confirme no Instagram)", min_value=0, value=245, step=1)
    dias_periodo = st.number_input("Quantidade de dias do período de seguidores", min_value=1, value=14, step=1)

nao_seguidor_views = round(visualizacoes * pct_nao_seguidores / 100)
taxa_visita = visitas_perfil / visualizacoes * 100 if visualizacoes else 0
taxa_interacao = interacoes / visualizacoes * 100 if visualizacoes else 0
media_diaria = novos_seguidores / dias_periodo if dias_periodo else 0

st.subheader("📊 Visão geral")
cols = st.columns(4)
cols[0].metric("Seguidores atuais", f"{seguidores:,}".replace(",", "."))
cols[1].metric("Visualizações", f"{visualizacoes:,}".replace(",", "."))
cols[2].metric("Views de não seguidores", f"{nao_seguidor_views:,}".replace(",", "."))
cols[3].metric("Interações", f"{interacoes:,}".replace(",", "."))
cols = st.columns(4)
cols[0].metric("Visitas ao perfil", f"{visitas_perfil:,}".replace(",", "."))
cols[1].metric("Visita / visualização", f"{taxa_visita:.2f}%")
cols[2].metric("Interação / visualização", f"{taxa_interacao:.2f}%")
cols[3].metric("Média diária de seguidores*", f"{media_diaria:.1f}")
st.caption("*Estimativa baseada nos valores inseridos. Confirme os números no Instagram Insights.")
st.info("Esta versão ainda não está conectada automaticamente ao Instagram. Os números são preenchidos manualmente.")

st.divider()
st.header("🚀 Gerador de conteúdo para Reels")
st.write("Gere uma ideia, gancho, roteiro e CTA para testar. Nenhum roteiro garante viralização.")
categorias = ["Achadinhos para casa", "Organização", "Beleza", "Maternidade", "Achadinhos variados"]

with st.form("gerador_conteudo"):
    a, b = st.columns(2)
    with a:
        categoria = st.selectbox("Tema do conteúdo", categorias)
        objetivo = st.selectbox("Objetivo principal", ["Alcançar não seguidores", "Ganhar seguidores", "Gerar compartilhamentos", "Gerar salvamentos", "Levar pessoas ao link"])
        produto = st.text_input("Produto ou achado (opcional)", placeholder="Ex.: organizador de gaveta")
    with b:
        formato = st.selectbox("Formato do Reel", ["Demonstração do produto", "Lista de 3 achadinhos", "Antes e depois", "Problema e solução", "Rotina/experiência pessoal"])
        estilo = st.selectbox("Estilo do gancho", ["Curiosidade", "Identificação", "Surpresa", "Dica prática", "Opinião sincera"])
    gerar = st.form_submit_button("✨ Gerar roteiro")

if gerar:
    tema = produto.strip() if produto.strip() else categoria.lower()
    hooks = {
        "Curiosidade": f"Eu não imaginava que um achadinho como {tema} poderia ser tão útil!",
        "Identificação": f"Se você ama facilitar a rotina sem gastar à toa, olha esta ideia: {tema}.",
        "Surpresa": f"Este achadinho merece ser conhecido: {tema}!",
        "Dica prática": f"Uma ideia simples para facilitar seu dia: conheça {tema}.",
        "Opinião sincera": f"Antes de comprar {tema}, veja estes detalhes."
    }
    gancho = hooks[estilo]
    roteiros = {
        "Demonstração do produto": ["0–2 s: mostre o produto em uso e coloque o gancho na tela.", "2–6 s: mostre como funciona, sem introdução longa.", "6–12 s: explique um benefício real e para quem pode ser útil.", "12–15 s: termine com uma pergunta ou convite para acompanhar a página."],
        "Lista de 3 achadinhos": ["0–2 s: mostre os três itens e apresente o gancho.", "2–6 s: item 1 + benefício principal.", "6–10 s: item 2 + benefício principal.", "10–14 s: item 3 + benefício principal.", "14–17 s: peça para salvar ou compartilhar a lista."],
        "Antes e depois": ["0–2 s: mostre o antes.", "2–5 s: apresente o produto ou método.", "5–12 s: mostre o processo e o resultado real.", "12–15 s: convide a pessoa a salvar a ideia."],
        "Problema e solução": ["0–2 s: mostre um problema cotidiano.", "2–5 s: apresente o achado como possível solução.", "5–12 s: demonstre o uso de forma objetiva.", "12–15 s: pergunte quem também enfrenta esse problema."],
        "Rotina/experiência pessoal": ["0–3 s: comece com uma situação real da sua rotina.", "3–8 s: mostre onde o produto entra no seu dia.", "8–13 s: conte o que gostou e o que verificar antes de comprar.", "13–16 s: convide o público a acompanhar mais dicas honestas."]
    }
    ctas = {
        "Alcançar não seguidores": "Envie este vídeo para alguém que gostaria de descobrir esse tipo de achado.",
        "Ganhar seguidores": "Siga a página para descobrir mais achadinhos úteis para casa, beleza e maternidade.",
        "Gerar compartilhamentos": "Compartilhe com aquela pessoa que ama encontrar coisas úteis.",
        "Gerar salvamentos": "Salve este Reel para consultar quando precisar dessa ideia.",
        "Levar pessoas ao link": "Confira as informações do produto no link indicado no perfil, se estiver disponível."
    }
    cta = ctas[objetivo]
    legenda = f"{gancho}\n\nCompartilho ideias e achadinhos para facilitar a rotina. Confira características, avaliações e preço atualizado antes de comprar.\n\n{cta}"
    st.success("Roteiro criado! Adapte-o à sua experiência real e mostre o produto com honestidade.")
    st.markdown("#### 🎣 Gancho para os primeiros segundos")
    st.write(gancho)
    st.markdown("#### 🎬 Roteiro sugerido")
    for etapa in roteiros[formato]:
        st.write("• " + etapa)
    st.markdown("#### 📣 CTA")
    st.write(cta)
    st.text_area("Legenda sugerida (copie e adapte)", value=legenda, height=140, key="legenda_gerada")
    st.info("Depois de publicar, anote alcance, compartilhamentos, salvamentos, visitas ao perfil e seguidores ganhos.")

st.divider()
st.header("📈 Registro dos resultados por conteúdo")
st.caption("O histórico desta primeira versão fica apenas durante a sessão. Baixe o CSV para guardar uma cópia.")
colunas = ["Data", "Tema", "Formato", "Alcance", "Visualizações", "Compartilhamentos", "Salvamentos", "Visitas ao perfil", "Seguidores ganhos"]
if "historico_posts" not in st.session_state:
    st.session_state.historico_posts = pd.DataFrame(columns=colunas)

with st.form("adicionar_resultado"):
    a, b, c = st.columns(3)
    with a:
        data_post = st.date_input("Data da publicação", value=date.today())
        tema_post = st.text_input("Tema do Reel", placeholder="Ex.: organizador de cozinha")
        formato_post = st.selectbox("Formato publicado", ["Demonstração", "Lista", "Antes e depois", "Problema e solução", "Rotina"])
    with b:
        alcance_post = st.number_input("Alcance", min_value=0, step=10)
        views_post = st.number_input("Visualizações", min_value=0, step=10)
        compartilhamentos_post = st.number_input("Compartilhamentos", min_value=0, step=1)
    with c:
        salvamentos_post = st.number_input("Salvamentos", min_value=0, step=1)
        visitas_post = st.number_input("Visitas ao perfil", min_value=0, step=1)
        seguidores_post = st.number_input("Seguidores ganhos atribuídos", min_value=0, step=1)
    salvar = st.form_submit_button("➕ Registrar resultado")

if salvar:
    linha = pd.DataFrame([{
        "Data": data_post.isoformat(), "Tema": tema_post, "Formato": formato_post,
        "Alcance": alcance_post, "Visualizações": views_post,
        "Compartilhamentos": compartilhamentos_post, "Salvamentos": salvamentos_post,
        "Visitas ao perfil": visitas_post, "Seguidores ganhos": seguidores_post
    }])
    st.session_state.historico_posts = pd.concat([st.session_state.historico_posts, linha], ignore_index=True)
    st.success("Resultado adicionado à tabela desta sessão.")

if not st.session_state.historico_posts.empty:
    st.dataframe(st.session_state.historico_posts, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Baixar histórico em CSV", data=st.session_state.historico_posts.to_csv(index=False).encode("utf-8-sig"), file_name="historico_amanda_growth.csv", mime="text/csv")
    st.metric("Seguidores ganhos nos conteúdos registrados", int(pd.to_numeric(st.session_state.historico_posts["Seguidores ganhos"]).sum()))
else:
    st.info("Nenhum resultado registrado ainda. Depois de publicar um Reel, adicione os números reais aqui.")

st.divider()
st.subheader("💡 Ideias rápidas para testar")
ideias = pd.DataFrame([
    {"Tema": "3 achadinhos para organizar a cozinha", "Gancho": "Sua cozinha também fica bagunçada tão rápido?", "Medir": "Compartilhamentos e salvamentos"},
    {"Tema": "Achado útil para rotina de mãe", "Gancho": "Mães, olha esta ideia para facilitar a correria do dia!", "Medir": "Compartilhamentos e visitas ao perfil"},
    {"Tema": "Produto de beleza acessível", "Gancho": "Antes de comprar, veja estes detalhes neste achadinho.", "Medir": "Salvamentos e visitas ao perfil"}
])
st.dataframe(ideias, use_container_width=True, hide_index=True)
st.warning("Ainda não há conexão automática com Instagram nem IA externa. O gerador usa modelos de roteiro. A próxima etapa será adicionar IA e armazenamento persistente. Não automatizamos curtidas, comentários ou seguidores.")
st.caption("A meta de 1.000 novos seguidores por semana é um objetivo, não uma promessa de resultado.")
