import streamlit as st
import py3Dmol
from rdkit import Chem
from rdkit.Chem import AllChem
import tempfile

# =========================
# FUNCIONES GENERALES
# =========================

def convert_xyz_to_inp(xyz_content, level, basis, operation, charge, multiplicity, print_orbitals):
    lines = xyz_content.strip().splitlines()
    atom_lines = lines[2:]

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


def smiles_to_xyz(smiles):
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    AllChem.MMFFOptimizeMolecule(mol)

    conf = mol.GetConformer()
    atoms = mol.GetAtoms()

    xyz_lines = [str(mol.GetNumAtoms()), "Generated from SMILES"]

    for atom in atoms:
        pos = conf.GetAtomPosition(atom.GetIdx())
        xyz_lines.append(
            f"{atom.GetSymbol():<2} {pos.x:>12.5f} {pos.y:>12.5f} {pos.z:>12.5f}"
        )

    return "\n".join(xyz_lines), mol


# =========================
# CONFIGURACIÓN DE PÁGINA
# =========================

st.set_page_config(page_title="ORCA Input Generator")

st.sidebar.image("img/inORCA.png", caption="Dr. Jesus Alvarado-Huayhuaz")

st.sidebar.title("¿Tienes las coordenadas?")

default_xyz = """3
Hello water (https://www.faccts.de/docs/orca/6.0/tutorials/first_steps/first_calc.html)
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
"""

menu = st.sidebar.radio(
    "Si no las tienes puedes seleccionar NO e ingresar el código SMILES:",
    ("SI",
     "NO")
)

st.title("Generador de INP para ORCA", divider='rainbow'))

# =========================
# CAMPOS COMUNES
# =========================

def parameter_section():
    col1, col2 = st.columns(2)

    with col1:
        level = st.text_input("Nivel de cálculo", "B3LYP")
        operation = st.text_input("Operación", "OPT FREQ")
        print_orbitals = st.selectbox("¿Imprimir orbitales?", ["Yes", "No"])

    with col2:
        basis = st.text_input("Conjunto Base", "def2-TZVP")
        charge = st.number_input("Carga", value=0, step=1)
        multiplicity = st.number_input("Multiplicidad", value=1, step=1)

    return level, basis, operation, charge, multiplicity, print_orbitals


# =====================================================
# OPCIÓN 1 — SUBIR XYZ  (PÁGINA ORIGINAL MEJORADA)
# =====================================================

if menu == "SI":

    uploaded_file = st.file_uploader("Selecciona un archivo XYZ", type=["xyz"])

    # Si el usuario sube archivo, usar ese
    if uploaded_file is not None:
        xyz_text = uploaded_file.read().decode("utf-8")
    else:
        # Si no, usar molécula por defecto
        xyz_text = default_xyz

    st.subheader("Contenido del archivo XYZ")
    xyz_text = st.text_area("Texto del XYZ", xyz_text, height=150)

    # Visualización 3D
    st.subheader("Visualización 3D")
    viewer = show_xyz(xyz_text)
    st.components.v1.html(viewer._make_html(), height=400, width=500)

    # Parámetros
    st.subheader("Parámetros de cálculo")
    level, basis, operation, charge, multiplicity, print_orbitals = parameter_section()

    # Generación INP
    inp_text = convert_xyz_to_inp(
        xyz_text, level, basis, operation, charge, multiplicity, print_orbitals
    )

    st.subheader("Archivo INP generado")
    st.text_area("Vista previa del INP", inp_text, height=300)

    st.download_button(
        label="Descargar archivo INP",
        data=inp_text,
        file_name="default_structure.inp",
        mime="text/plain"
    )

# =====================================================
# OPCIÓN 2 — GENERAR DESDE SMILES
# =====================================================

elif menu == "NO":

    smiles_input = st.text_input("Ingresa código SMILES", "CCO")

    if smiles_input:

        try:
            xyz_text, mol = smiles_to_xyz(smiles_input)

            st.subheader("Coordenadas 3D generadas (formato XYZ)")
            st.text_area("Texto XYZ generado", xyz_text, height=200)

            # Visualización 3D
            st.subheader("Visualización 3D")
            viewer = show_xyz(xyz_text)
            st.components.v1.html(viewer._make_html(), height=400, width=500)

            # Parámetros
            st.subheader("Parámetros de cálculo")
            level, basis, operation, charge, multiplicity, print_orbitals = parameter_section()

            # Generar INP
            inp_text = convert_xyz_to_inp(
                xyz_text, level, basis, operation, charge, multiplicity, print_orbitals
            )

            st.subheader("Archivo INP generado")
            st.text_area("Vista previa del INP", inp_text, height=300)

            st.download_button(
                label="Descargar archivo INP",
                data=inp_text,
                file_name="smiles_generated.inp",
                mime="text/plain"
            )

        except:
            st.error("SMILES inválido. Por favor verifica la sintaxis.")
