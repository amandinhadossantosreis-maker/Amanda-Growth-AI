import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Amanda Growth AI", page_icon="📈", layout="wide")

st.title("📈 Amanda Growth AI")
st.caption("Crescimento orgânico + estúdio criativo para @homedaamandah")

# ---- Sidebar: métricas ----
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
st.caption("*Estimativa com base nos valores inseridos. Confirme os números no Instagram Insights.")
st.info("Os números ainda são manuais; esta versão não está conectada automaticamente ao Instagram.")

st.divider()
st.header("🎨 Estúdio Criativo da Amanda")
st.write("Planeje artes, carrosséis e conteúdo com intenção. A avaliação é uma orientação criativa, não uma garantia de alcance.")
abas = st.tabs(["🖼️ Criar conceito de imagem", "📚 Planejar carrossel", "🔍 Analisar uma arte", "✍️ Legenda e publicação"])

temas = ["Decoração", "Achadinhos para casa", "Organização", "Beleza", "Maternidade", "Brinquedos", "Moda", "Cozinha", "Natal e datas comemorativas", "Outro"]
estilos = ["Realista e aconchegante", "Elegante e sofisticado", "Colorido e divertido", "Minimalista", "Promocional e chamativo", "Editorial/lifestyle"]
formatos = ["Feed vertical 4:5", "Story/Reel vertical 9:16", "Quadrado 1:1", "Carrossel 4:5"]

with abas[0]:
    st.subheader("Crie um briefing visual")
    with st.form("briefing_imagem"):
        c1, c2 = st.columns(2)
        with c1:
            tema_img = st.selectbox("Tema", temas)
            produto_img = st.text_input("Produto ou assunto", placeholder="Ex.: árvore de Natal de 1,80 m")
            estilo_img = st.selectbox("Estilo visual", estilos)
        with c2:
            formato_img = st.selectbox("Formato desejado", formatos)
            objetivo_img = st.selectbox("Objetivo", ["Atrair novos seguidores", "Gerar compartilhamentos", "Gerar salvamentos", "Apresentar produto", "Gerar cliques no link"])
            incluir_texto = st.checkbox("A arte deve conter texto", value=True)
        detalhes_img = st.text_area("Detalhes importantes", placeholder="Cores, ambiente, público, benefícios reais, elementos que precisam aparecer...")
        criar_conceito = st.form_submit_button("✨ Criar conceito e prompt")
    if criar_conceito:
        assunto = produto_img.strip() or tema_img
        textos_objetivo = {
            "Atrair novos seguidores": "Crie uma ideia visual com leitura imediata, identidade memorável e curiosidade que incentive a conhecer o perfil.",
            "Gerar compartilhamentos": "Priorize uma ideia útil, identificável e fácil de compartilhar com amigos ou familiares.",
            "Gerar salvamentos": "Priorize informação prática, organização visual e utilidade para consulta futura.",
            "Apresentar produto": "Destaque claramente o produto, mostre escala e detalhes, sem inventar características.",
            "Gerar cliques no link": "Mostre o produto com clareza e reserve espaço para uma chamada honesta para conferir detalhes."
        }
        chamada = "Texto curto, legível e em português brasileiro, com hierarquia clara." if incluir_texto else "Não inclua palavras, letras, logotipos ou marcas d'água."
        prompt = (
            f"Crie uma imagem para Instagram sobre {assunto}. Tema: {tema_img}. "
            f"Estilo: {estilo_img}. Formato: {formato_img}. Objetivo: {objetivo_img}. "
            f"{chamada} {textos_objetivo[objetivo_img]} "
            f"Detalhes adicionais: {detalhes_img or 'sem detalhes adicionais'}. "
            "Composição profissional, foco visual claro, boa iluminação, aparência natural e acabamento de alta qualidade. "
            "Não invente preços, avaliações, especificações ou promessas. Evite textos pequenos e elementos confusos."
        )
        st.session_state["ultimo_prompt_imagem"] = prompt
        st.session_state["ultimo_conceito"] = {
            "assunto": assunto, "tema": tema_img, "estilo": estilo_img,
            "formato": formato_img, "objetivo": objetivo_img,
            "texto": incluir_texto, "detalhes": detalhes_img
        }
    if "ultimo_prompt_imagem" in st.session_state:
        st.markdown("#### Seu conceito")
        conceito = st.session_state["ultimo_conceito"]
        st.write(f"**Assunto:** {conceito['assunto']} · **Estilo:** {conceito['estilo']} · **Formato:** {conceito['formato']}")
        st.text_area("Prompt pronto para copiar", value=st.session_state["ultimo_prompt_imagem"], height=180, key="prompt_imagem_exibido")
        st.info("Esta etapa prepara o conceito e o prompt. A geração automática da imagem será ativada quando conectarmos um serviço de geração de imagens.")
        st.download_button("⬇️ Baixar prompt .txt", data=st.session_state["ultimo_prompt_imagem"], file_name="prompt_estudio_amanda.txt", mime="text/plain")

with abas[1]:
    st.subheader("Planeje um carrossel completo")
    with st.form("briefing_carrossel"):
        tema_car = st.text_input("Assunto do carrossel", placeholder="Ex.: 5 achadinhos para decorar no Natal")
        publico_car = st.selectbox("Público principal", ["Pessoas que amam decoração", "Mães", "Quem gosta de organização", "Público de beleza", "Público geral de achadinhos"])
        qtd_car = st.slider("Número de páginas", 4, 10, 6)
        estilo_car = st.selectbox("Identidade visual do carrossel", estilos, key="estilo_car")
        objetivo_car = st.selectbox("Objetivo do carrossel", ["Ganhar seguidores", "Gerar salvamentos", "Gerar compartilhamentos", "Apresentar produtos"], key="objetivo_car")
        criar_car = st.form_submit_button("📚 Montar carrossel")
    if criar_car:
        assunto = tema_car.strip() or "Achadinhos que facilitam a rotina"
        paginas = []
        paginas.append({"Página": 1, "Função": "Capa", "Texto sugerido": f"{assunto.upper()} — DESLIZE PARA VER", "Direção visual": f"Capa impactante, estilo {estilo_car}, texto grande e assunto evidente."})
        for i in range(2, qtd_car):
            if i == 2:
                funcao, texto = "Destaque 1", "Apresente o primeiro item/ideia e o benefício real."
            elif i == 3:
                funcao, texto = "Destaque 2", "Mostre o segundo item/ideia com foto ou detalhe em destaque."
            elif i == 4:
                funcao, texto = "Destaque 3", "Explique por que esse item pode ser útil para o público."
            elif i == qtd_car - 1:
                funcao, texto = "Resumo", "Reúna os favoritos ou os pontos mais úteis em uma composição limpa."
            else:
                funcao, texto = f"Destaque {i-1}", "Inclua outro item/ideia com benefício verificável e visual diferente."
            paginas.append({"Página": i, "Função": funcao, "Texto sugerido": texto, "Direção visual": f"Imagem vertical 4:5, estilo {estilo_car}, foco no assunto, pouco texto e margens consistentes."})
        cta_final = {
            "Ganhar seguidores": "Se você gosta de achadinhos assim, siga o perfil para ver mais.",
            "Gerar salvamentos": "Salve este carrossel para consultar depois.",
            "Gerar compartilhamentos": "Envie para alguém que gostaria dessas ideias.",
            "Apresentar produtos": "Confira os detalhes e as informações atualizadas antes de comprar."
        }[objetivo_car]
        paginas.append({"Página": qtd_car, "Função": "CTA final", "Texto sugerido": cta_final, "Direção visual": "Final simples, CTA legível e identidade consistente."})
        df_car = pd.DataFrame(paginas)
        st.session_state["carrossel_atual"] = df_car
        st.session_state["carrossel_tema"] = assunto
    if "carrossel_atual" in st.session_state:
        st.write(f"**Carrossel:** {st.session_state['carrossel_tema']}")
        st.dataframe(st.session_state["carrossel_atual"], use_container_width=True, hide_index=True)
        st.download_button("⬇️ Baixar planejamento do carrossel (CSV)", data=st.session_state["carrossel_atual"].to_csv(index=False).encode("utf-8-sig"), file_name="planejamento_carrossel_amanda.csv", mime="text/csv")

with abas[2]:
    st.subheader("Análise visual de uma arte")
    st.write("Envie uma imagem para registrar qual arte está avaliando. Nesta versão, a avaliação é um checklist guiado; a análise automática por visão computacional será integrada depois.")
    arquivo_arte = st.file_uploader("Enviar imagem para avaliar", type=["png", "jpg", "jpeg", "webp"], key="arquivo_arte")
    if arquivo_arte:
        st.image(arquivo_arte, caption="Arte enviada para avaliação", use_container_width=True)
        st.session_state["nome_arte"] = arquivo_arte.name
    with st.form("avaliacao_arte"):
        st.write("Dê uma nota de 1 a 5 para cada critério:")
        nota_gancho = st.slider("Texto principal chama atenção?", 1, 5, 3)
        nota_produto = st.slider("Produto/assunto está evidente?", 1, 5, 3)
        nota_legivel = st.slider("Texto é legível no celular?", 1, 5, 3)
        nota_hierarquia = st.slider("Composição tem hierarquia visual?", 1, 5, 3)
        nota_relevancia = st.slider("A arte oferece uma ideia útil ou desejável?", 1, 5, 3)
        observacoes = st.text_area("O que você quer melhorar?", placeholder="Ex.: título maior, menos elementos, mais destaque ao produto...")
        avaliar = st.form_submit_button("🔎 Gerar diagnóstico")
    if avaliar:
        media = (nota_gancho + nota_produto + nota_legivel + nota_hierarquia + nota_relevancia) / 5
        pontos = {
            "Gancho": nota_gancho, "Destaque do assunto": nota_produto,
            "Legibilidade": nota_legivel, "Hierarquia visual": nota_hierarquia,
            "Utilidade/desejo": nota_relevancia
        }
        st.metric("Nota média do checklist", f"{media:.1f}/5")
        baixos = [nome for nome, nota in pontos.items() if nota <= 3]
        if baixos:
            st.write("**Priorize estas melhorias:** " + ", ".join(baixos) + ".")
        else:
            st.success("O checklist está consistente. Teste a arte e compare os resultados reais.")
        st.write("**Próximas ações sugeridas:** use um título curto; mantenha contraste alto; destaque um único foco; verifique a leitura em tela pequena; evite promessas ou características não confirmadas.")
        if observacoes:
            st.write("**Sua observação:**", observacoes)

with abas[3]:
    st.subheader("Legenda e plano de publicação")
    with st.form("legenda_publicacao"):
        tema_leg = st.text_input("Tema ou produto", placeholder="Ex.: itens natalinos fofos para decorar gastando pouco")
        tom_leg = st.selectbox("Tom da legenda", ["Amigável e próximo", "Divertido", "Elegante", "Informativo", "Opinião sincera"])
        objetivo_leg = st.selectbox("CTA desejado", ["Ganhar seguidores", "Comentários", "Salvamentos", "Compartilhamentos", "Visitas ao perfil"])
        criar_leg = st.form_submit_button("✍️ Criar legenda")
    if criar_leg:
        tema = tema_leg.strip() or "este achadinho"
        aberturas = {
            "Amigável e próximo": f"Olha essa ideia que encontrei para quem ama {tema.lower()}! ✨",
            "Divertido": f"Me conta que você também ficou com vontade de testar {tema.lower()} 😂✨",
            "Elegante": f"Pequenos detalhes podem transformar a forma de aproveitar {tema.lower()}.",
            "Informativo": f"Uma ideia para conhecer melhor: {tema}. Confira os detalhes antes de escolher.",
            "Opinião sincera": f"Antes de decidir sobre {tema}, vale observar estes detalhes."
        }
        ctas = {
            "Ganhar seguidores": "Siga @homedaamandah para mais ideias, achadinhos e inspirações.",
            "Comentários": "Qual detalhe você mais gostou? Me conta nos comentários.",
            "Salvamentos": "Salve este post para consultar quando precisar.",
            "Compartilhamentos": "Envie para alguém que também vai gostar dessa ideia.",
            "Visitas ao perfil": "Visite o perfil para ver mais inspirações e achadinhos."
        }
        legenda = aberturas[tom_leg] + "\\n\\n" + "Confira características, avaliações e preço atualizado antes de comprar. " + "\\n\\n" + ctas[objetivo_leg]
        st.text_area("Legenda pronta para adaptar", value=legenda, height=140, key="legenda_estudio")
        st.caption("Se houver comissão ou parceria, sinalize isso de forma clara conforme as regras aplicáveis.")

# ---- Gerador de roteiros ----
st.divider()
st.header("🎬 Gerador de roteiros para Reels")
with st.form("gerador_reels"):
    c1, c2 = st.columns(2)
    with c1:
        tema_reel = st.selectbox("Tema do Reel", temas, key="tema_reel")
        produto_reel = st.text_input("Produto/assunto do Reel", placeholder="Ex.: mão do Grinch para decorar a porta")
        objetivo_reel = st.selectbox("Objetivo", ["Ganhar seguidores", "Gerar compartilhamentos", "Gerar salvamentos", "Apresentar produto"])
    with c2:
        formato_reel = st.selectbox("Formato", ["Demonstração", "Lista de 3 itens", "Antes e depois", "Problema e solução", "Rotina/experiência"])
        gancho_tipo = st.selectbox("Tipo de gancho", ["Curiosidade", "Identificação", "Surpresa", "Dica prática", "Opinião sincera"])
    gerar_reel = st.form_submit_button("✨ Gerar roteiro")
if gerar_reel:
    assunto = produto_reel.strip() or tema_reel.lower()
    hooks = {
        "Curiosidade": f"Olha esse detalhe de {assunto} que talvez você ainda não tenha visto!",
        "Identificação": f"Se você ama encontrar ideias úteis e bonitas, veja {assunto}.",
        "Surpresa": f"Eu não esperava encontrar uma ideia assim para {assunto}!",
        "Dica prática": f"Uma ideia para transformar ou facilitar sua rotina: {assunto}.",
        "Opinião sincera": f"Antes de escolher {assunto}, veja estes detalhes."
    }
    passos = {
        "Demonstração": ["0–2 s: mostre o resultado final e o gancho na tela.", "2–7 s: mostre detalhes e uso real.", "7–13 s: destaque benefícios confirmados.", "13–16 s: finalize com CTA."],
        "Lista de 3 itens": ["0–2 s: mostre os três itens.", "2–6 s: apresente o item 1.", "6–10 s: apresente o item 2.", "10–14 s: apresente o item 3.", "14–17 s: convide a salvar ou compartilhar."],
        "Antes e depois": ["0–2 s: mostre o antes.", "2–5 s: apresente a mudança.", "5–12 s: mostre o processo e o resultado real.", "12–15 s: finalize com CTA."],
        "Problema e solução": ["0–2 s: apresente o problema cotidiano.", "2–5 s: mostre a ideia ou produto.", "5–12 s: demonstre a solução.", "12–15 s: pergunte se a pessoa já passou por isso."],
        "Rotina/experiência": ["0–3 s: comece com uma situação real.", "3–8 s: mostre o produto no contexto.", "8–13 s: compartilhe uma observação honesta.", "13–16 s: convide a acompanhar o perfil."]
    }
    cta = {
        "Ganhar seguidores": "Siga @homedaamandah para mais ideias e achadinhos.",
        "Gerar compartilhamentos": "Envie para alguém que também gostaria desta ideia.",
        "Gerar salvamentos": "Salve para consultar depois.",
        "Apresentar produto": "Confira detalhes, avaliações e preço atualizado antes de comprar."
    }[objetivo_reel]
    st.markdown("#### 🎣 Gancho")
    st.write(hooks[gancho_tipo])
    st.markdown("#### 🎬 Sequência")
    for passo in passos[formato_reel]:
        st.write("• " + passo)
    st.markdown("#### 📣 CTA")
    st.write(cta)

# ---- Registro de resultados ----
st.divider()
st.header("📈 Registro de resultados por conteúdo")
st.caption("Nesta primeira versão, os registros permanecem na sessão atual. Baixe o CSV para guardar uma cópia.")
colunas = ["Data", "Tema", "Formato", "Alcance", "Visualizações", "Compartilhamentos", "Salvamentos", "Visitas ao perfil", "Seguidores ganhos"]
if "historico_posts" not in st.session_state:
    st.session_state.historico_posts = pd.DataFrame(columns=colunas)

with st.form("adicionar_resultado"):
    a, b, c = st.columns(3)
    with a:
        data_post = st.date_input("Data da publicação", value=date.today())
        tema_post = st.text_input("Tema publicado", placeholder="Ex.: decoração de Natal")
        formato_post = st.selectbox("Formato publicado", ["Imagem única", "Carrossel", "Reel", "Stories"])
    with b:
        alcance_post = st.number_input("Alcance", min_value=0, step=10)
        views_post = st.number_input("Visualizações", min_value=0, step=10)
        compartilhamentos_post = st.number_input("Compartilhamentos", min_value=0, step=1)
    with c:
        salvamentos_post = st.number_input("Salvamentos", min_value=0, step=1)
        visitas_post = st.number_input("Visitas ao perfil", min_value=0, step=1)
        seguidores_post = st.number_input("Seguidores ganhos atribuídos", min_value=0, step=1)
    salvar_post = st.form_submit_button("➕ Registrar resultado")
if salvar_post:
    linha = pd.DataFrame([{
        "Data": data_post.isoformat(), "Tema": tema_post, "Formato": formato_post,
        "Alcance": alcance_post, "Visualizações": views_post,
        "Compartilhamentos": compartilhamentos_post, "Salvamentos": salvamentos_post,
        "Visitas ao perfil": visitas_post, "Seguidores ganhos": seguidores_post
    }])
    st.session_state.historico_posts = pd.concat([st.session_state.historico_posts, linha], ignore_index=True)
    st.success("Resultado registrado nesta sessão.")
if not st.session_state.historico_posts.empty:
    st.dataframe(st.session_state.historico_posts, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Baixar histórico em CSV", data=st.session_state.historico_posts.to_csv(index=False).encode("utf-8-sig"), file_name="historico_amanda_growth.csv", mime="text/csv")
    st.metric("Seguidores ganhos nos conteúdos registrados", int(pd.to_numeric(st.session_state.historico_posts["Seguidores ganhos"]).sum()))
else:
    st.info("Ainda não há resultados registrados.")

st.warning("Limitações atuais: o estúdio prepara briefings, prompts e planos, mas ainda não gera imagens automaticamente nem analisa a imagem com IA. Também não há conexão automática ao Instagram nem armazenamento permanente. Essas serão as próximas integrações.")
st.caption("A meta de 1.000 novos seguidores por semana é um objetivo, não uma promessa de resultado.")
