import streamlit as st
import requests

def get_iupac_from_input(user_input):
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    iupac_name = None

    # 1. Si el input es numérico, se trata como CID
    if user_input.isdigit():
        url = f"{base_url}/compound/cid/{user_input}/property/IUPACName/JSON"
    # 2. Si es un SMILES
    elif any(char in user_input for char in "=#()/\\[]"):
        url = f"{base_url}/compound/smiles/{user_input}/property/IUPACName/JSON"
    # 3. De lo contrario, se trata como nombre común
    else:
        url = f"{base_url}/compound/name/{user_input}/property/IUPACName/JSON"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        iupac_name = data["PropertyTable"]["Properties"][0]["IUPACName"]
    else:
        st.error("No se pudo obtener el nombre IUPAC. Revisa el formato del input o prueba con otro compuesto.")

    return iupac_name

# Streamlit UI
st.set_page_config(page_title="IUPAC Name Finder", page_icon="🧪")
st.title("🔎 IUPAC Name Finder")
st.markdown("Introduce un código **SMILES**, un **nombre común en inglés** o un **PubChem CID**, y obtén el nombre **IUPAC** del compuesto.")

user_input = st.text_input("Introduce el código o nombre del compuesto")

if st.button("Obtener nombre IUPAC"):
    if user_input:
        iupac_name = get_iupac_from_input(user_input)
        if iupac_name:
            st.success(f"**Nombre IUPAC:** {iupac_name}")
    else:
        st.warning("Por favor, introduce algún dato de entrada.")
