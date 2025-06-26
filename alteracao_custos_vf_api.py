import streamlit as st
import requests
import json
import datetime
import pandas as pd

# Função para formatar código de barras
def formatar_codigo_barras(codigo_barras):
    if len(codigo_barras) < 13:
        codigo_barras = codigo_barras.zfill(13)
    return codigo_barras

# Função de login
def login(username, password):
    url_login = "https://lojasmimi.varejofacil.com/api/auth"
    payload = json.dumps({
        "username": username,
        "password": password
    })
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url_login, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            return data.get("accessToken")
        return None
    except:
        return None

# Função para obter o produto ID
def obter_produto_id(codigo_barras, access_token):
    url_produto = f"https://lojasmimi.varejofacil.com/api/v1/produto/produtos/consulta/0{codigo_barras}"
    headers = {
        'Authorization': access_token
    }
    try:
        response = requests.get(url_produto, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('id'), data.get('descricao', 'Descrição não encontrada')
    except:
        pass
    return None, None

# Obter custos do produto
def obter_custos_produto(produtoid, access_token):
    url = f"https://lojasmimi.varejofacil.com/api/v1/produto/produtos/{produtoid}/precos"
    headers = {
        'Authorization': access_token
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# Função centralizada para atualizar preços
def atualizar_precos_por_tipo(custos, novo_valor, tipo_atualizacao, access_token):
    data_atual = datetime.datetime.now().astimezone().isoformat()
    sucesso = []

    for custo in custos:
        if custo['lojaId'] in [1, 2, 5]:
            id_preco = custo['id']
            url = f"https://lojasmimi.varejofacil.com/api/v1/produto/precos/{id_preco}"

            payload = {
                "id": id_preco,
                "lojaId": custo['lojaId'],
                "produtoId": custo['produtoId'],
                "dataUltimoReajustePreco1": data_atual,
                "precoVenda1": custo.get("precoVenda1"),
                "custoProduto": custo.get("custoProduto"),
                "precoMedioDeReposicao": custo.get("precoMedioDeReposicao"),
                "precoFiscalDeReposicao": custo.get("precoFiscalDeReposicao")
            }

            if tipo_atualizacao == "Venda":
                payload["precoVenda1"] = novo_valor
            elif tipo_atualizacao == "Custo":
                payload["custoProduto"] = novo_valor
                payload["precoMedioDeReposicao"] = novo_valor
                payload["precoFiscalDeReposicao"] = novo_valor

            headers = {
                'Content-Type': 'application/json',
                'Authorization': access_token
            }

            response = requests.put(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                sucesso.append(custo['lojaId'])
    return sucesso

# Configuração da página
st.set_page_config(page_title="Atualizador de Custos", layout="centered")

# Barra lateral
with st.sidebar:
    st.title("🛠️ Menu")
    st.markdown("Utilitário para atualização de preços")
    st.markdown("---")
    st.markdown("Desenvolvido para **Lojas Mimi** por [Pablo Dantas](https://github.com/opablodantas)")


st.title("📦 Atualizador de Preços - Lojas Mimi")

# Sessão de login
if "access_token" not in st.session_state:
    st.subheader("🔐 Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        with st.spinner("🔄 Validando credenciais..."):
            token = login(username, password)
        if token:
            st.session_state.access_token = token
            st.session_state.usuario = username
            st.success("✅ Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("❌ Falha no login. Verifique suas credenciais.")

# Após login
# Após login
if "access_token" in st.session_state:
    st.success(f"👤 Usuário logado: {st.session_state.usuario}")
    
    # Botão Sair (logoff)
    if st.button("🚪 Sair"):
        for key in ["access_token", "usuario"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()  # Atualiza a página para tela de login
    
    st.divider()

    st.subheader("📇 Consultar e Atualizar Produto")
    
    # ... resto do código continua normalmente ...


    # Layout de seleção em colunas
    col1, col2 = st.columns(2)
    with col1:
        metodo_busca = st.selectbox("🔍 Método de busca", ["Código de Barras", "ProdutoId"])
    with col2:
        tipo_atualizacao = st.selectbox("💲 Tipo de atualização", ["Venda", "Custo"])

    entrada_usuario = st.text_input(f"Digite o {metodo_busca}")

    if entrada_usuario:
        produtoid = None
        descricao = None

        if metodo_busca == "Código de Barras":
            codigo_barras_formatado = formatar_codigo_barras(entrada_usuario)
            with st.spinner("🔄 Consultando produto..."):
                produtoid, descricao = obter_produto_id(codigo_barras_formatado, st.session_state.access_token)
        else:  # ProdutoId
            try:
                produtoid = int(entrada_usuario)
                descricao = f"Produto ID: {produtoid}"
            except ValueError:
                st.error("❌ ProdutoId inválido.")

        if produtoid:
            st.write(f"**Produto:** {descricao}")
            with st.spinner("🔄 Obtendo preços do produto..."):
                custos = obter_custos_produto(produtoid, st.session_state.access_token)

            if custos:
                precos = [
                    {
                        "Loja": c['lojaId'],
                        "Preço Venda (R$)": c.get('precoVenda1', 0.0),
                        "Custo Produto (R$)": c.get('custoProduto', 0.0)
                    }
                    for c in custos if c['lojaId'] in [1, 2, 5]
                ]

                df_precos = pd.DataFrame(precos)
                st.write("**Preços atuais nas lojas:**")
                st.dataframe(df_precos, use_container_width=True)

                novo_valor = st.number_input(
                    f"Novo valor de {tipo_atualizacao.lower()} (R$)",
                    min_value=0.0,
                    format="%.2f",
                    step=0.01,
                    key="novo_preco"
                )

                if st.button("Atualizar Preço"):
                    with st.spinner("🔄 Atualizando preços..."):
                        sucesso = atualizar_precos_por_tipo(custos, novo_valor, tipo_atualizacao, st.session_state.access_token)

                    if sucesso:
                        st.success(f"✅ {tipo_atualizacao} atualizado com sucesso para as lojas: {', '.join(map(str, sucesso))}")
                    else:
                        st.warning("⚠️ Nenhum valor foi atualizado.")
            else:
                st.error("❌ Erro ao obter os preços do produto.")
        else:
            st.error("❌ Produto não encontrado.")
