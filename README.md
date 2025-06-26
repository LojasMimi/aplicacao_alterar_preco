
# 📦 Atualizador de Preços - Lojas Mimi

Aplicação web desenvolvida em Python com [Streamlit](https://streamlit.io/) para realizar **consulta e atualização de preços de produtos (venda e custo)** nas Lojas Mimi, via API do [Varejo Fácil](https://varejofacil.com/).

## 🧩 Funcionalidades

- 🔐 **Login seguro** com token de acesso.
- 🔍 Consulta de produto por:
  - Código de Barras
  - ID do Produto
- 📊 Visualização de preços atuais por loja (Loja 1, 2 e 5).
- ✏️ Atualização de preço de **venda** ou **custo** em múltiplas lojas.
- 🚪 Botão "Sair" para logoff seguro da sessão.

---

## 🖼️ Interface

<img src="https://via.placeholder.com/600x300.png?text=Exemplo+de+Interface+Streamlit" alt="Interface do app" width="600"/>

---

## 🚀 Como Executar Localmente

### 1. Clone este repositório

```bash
git clone https://github.com/LojasMimi/aplicacao_alterar_preco.git
cd seurepositorio
````

### 2. Crie e ative um ambiente virtual (opcional)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

> Exemplo de `requirements.txt`:
>
> ```
> streamlit
> requests
> pandas
> ```

### 4. Rode a aplicação

```bash
streamlit run app.py
```

---

## ⚙️ Tecnologias Utilizadas

* [Python 3.9+](https://www.python.org/)
* [Streamlit](https://streamlit.io/)
* [Requests](https://pypi.org/project/requests/)
* [Pandas](https://pandas.pydata.org/) (para exibição de dados tabulados)
* API do Varejo Fácil

---

## 👨‍💻 Desenvolvido por

[Pablo Dantas](https://github.com/opablodantas)
Aspirante a Engenheiro de Inteligência Artificial 

---

## 📄 Licença

Este projeto é privado e de uso interno das **Lojas Mimi**. Consulte os responsáveis legais da empresa antes de redistribuir ou modificar.

```

