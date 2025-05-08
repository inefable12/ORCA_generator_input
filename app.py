import streamlit as st

def convert_xyz_to_inp(xyz_content, level, basis, operation, charge, multiplicity, print_orbitals):
    lines = xyz_content.strip().splitlines()
    atom_lines = lines[2:]  # Ignora las dos primeras líneas del archivo XYZ

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


st.set_page_config(page_title="Conversor XYZ a INP para ORCA")

st.title("Conversor de archivo XYZ a INP para ORCA con opciones personalizadas")

st.markdown("Sube tu archivo `.xyz`, edita los parámetros y descarga el archivo `.inp` personalizado.")

# Parámetros editables
level = st.text_input("Nivel de cálculo", "B3LYP")
basis = st.text_input("Conjunto Base", "def2-TZVP")
operation = st.text_input("Operación", "OPT FREQ")
charge = st.number_input("Carga", value=0, step=1)
multiplicity = st.number_input("Multiplicidad", value=1, step=1)
print_orbitals = st.selectbox("¿Imprimir orbitales?", ["Yes", "No"])

uploaded_file = st.file_uploader("Selecciona un archivo XYZ", type=["xyz"])

if uploaded_file is not None:
    xyz_text = uploaded_file.read().decode("utf-8")
    inp_text = convert_xyz_to_inp(
        xyz_text, level, basis, operation, charge, multiplicity, print_orbitals
    )

    st.text_area("Vista previa del archivo INP", inp_text, height=400)

    st.download_button(
        label="Descargar archivo INP",
        data=inp_text,
        file_name=uploaded_file.name.replace(".xyz", ".inp"),
        mime="text/plain"
    )
