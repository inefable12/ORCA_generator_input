import streamlit as st
import py3Dmol

def convert_xyz_to_inp(xyz_content, level, basis, operation, charge, multiplicity, print_orbitals):
    lines = xyz_content.strip().splitlines()
    atom_lines = lines[2:]  # Ignora encabezado y número de átomos

    header = f"! {level} {operation} {basis}\n"
    
    output_block = ""
    if print_orbitals == "Yes":
        output_block = """%output
  print[ p_mos ] 1
  print[ p_overlap ] 5
end

"""

    coord_block = f"* xyz {charge} {multiplicity}\n" + "\n".join(atom_lines) + "\n*"

    return header + output_block + coord_block

def show_xyz(xyz_data):
    viewer = py3Dmol.view(width=500, height=400)
    viewer.addModel(xyz_data, 'xyz')
    viewer.setStyle({'stick': {}})
    viewer.zoomTo()
    return viewer

# Configuración de página
st.set_page_config(page_title="XYZ a INP + Visualización 3D")

st.title("Conversor de XYZ a INP para ORCA con Visualización 3D")

st.markdown("Sube un archivo `.xyz`, visualízalo en 3D, personaliza parámetros y descarga el archivo `.inp`.")

# Campos editables
col1, col2 = st.columns(2)
with col1:
    level = st.text_input("Nivel de cálculo", "B3LYP")
    operation = st.text_input("Operación", "OPT FREQ")
    print_orbitals = st.selectbox("¿Imprimir orbitales?", ["Yes", "No"])
with col2:
    basis = st.text_input("Conjunto Base", "def2-TZVP")
    charge = st.number_input("Carga", value=0, step=1)
    multiplicity = st.number_input("Multiplicidad", value=1, step=1)

# Subida del archivo
uploaded_file = st.file_uploader("Selecciona un archivo XYZ", type=["xyz"])

if uploaded_file is not None:
    xyz_text = uploaded_file.read().decode("utf-8")
    
    st.subheader("📄 Contenido del archivo XYZ")
    st.text_area("Texto del archivo XYZ", xyz_text, height=150)

    st.subheader("📦 Archivo INP generado")
    inp_text = convert_xyz_to_inp(
        xyz_text, level, basis, operation, charge, multiplicity, print_orbitals
    )
    st.text_area("Vista previa del archivo INP", inp_text, height=250)

    st.download_button(
        label="Descargar archivo INP",
        data=inp_text,
        file_name=uploaded_file.name.replace(".xyz", ".inp"),
        mime="text/plain"
    )

    st.subheader("🧪 Visualización 3D de la molécula")
    viewer = show_xyz(xyz_text)
    viewer_html = viewer._make_html()
    st.components.v1.html(viewer_html, height=400, width=500)
