import streamlit as st
import tempfile

def convert_xyz_to_inp(xyz_content):
    lines = xyz_content.strip().splitlines()
    atom_lines = lines[2:]  # Ignora las dos primeras líneas del archivo XYZ

    inp_header = """! B3LYP OPT FREQ def2-TZVP
%output
  print[ p_mos ] 1
  print[ p_overlap ] 5
end

* xyz -1 1
"""
    inp_footer = "*"

    return inp_header + "\n".join(atom_lines) + "\n" + inp_footer

st.set_page_config(page_title="Conversor XYZ a INP para ORCA")

st.title("Conversor de archivo XYZ a formato INP para ORCA")
st.markdown("Sube tu archivo `.xyz` y descarga el archivo `.inp` compatible con ORCA.")

uploaded_file = st.file_uploader("Selecciona un archivo XYZ", type=["xyz"])

if uploaded_file is not None:
    xyz_text = uploaded_file.read().decode("utf-8")
    inp_text = convert_xyz_to_inp(xyz_text)

    st.text_area("Vista previa del archivo INP", inp_text, height=400)

    # Botón para descargar el archivo .inp
    st.download_button(
        label="Descargar archivo INP",
        data=inp_text,
        file_name=uploaded_file.name.replace(".xyz", ".inp"),
        mime="text/plain"
    )
