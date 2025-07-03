try:
    import streamlit as st
except ImportError:
    print("Streamlit is not installed. Please install it with 'pip install streamlit'.")
    exit(1)
try:
    import pandas as pd
except ImportError:
    print("Pandas is not installed. Please install it with 'pip install pandas'.")
    exit(1)
import os
import sys

# Import the model if available
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from power_distribution import Generation, Transmission, Substation, Distribution, Consumer
    MODEL_AVAILABLE = all([Generation, Transmission, Substation, Distribution, Consumer])
except Exception:
    Generation = Transmission = Substation = Distribution = Consumer = None
    MODEL_AVAILABLE = False

st.set_page_config(page_title="Electricity Distribution Hierarchy", layout="wide")
st.title("Electricity Distribution Hierarchy Simulator")

st.markdown("""
**Instructions:**
1. Upload your Excel workbook using the sidebar.
2. The app will try to automatically detect columns for each hierarchy level (Generation, Transmission, Substation, Distribution, Consumer).
3. If columns are missing or named differently, please rename them in your Excel file and re-upload.
4. You can view the hierarchy and run a sample simulation below.
""")

st.sidebar.header("Upload Workbook")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xlsx", "xls"]) 

data = None
if uploaded_file:
    try:
        data = pd.read_excel(uploaded_file)
        if data.empty:
            st.error("The uploaded Excel file is empty. Please check your file and try again.")
            data = None
        else:
            st.success("Workbook loaded successfully!")
            st.dataframe(data.head())
    except Exception as e:
        st.error(f"Error reading file: {e}")
        data = None
else:
    st.info("Please upload an Excel workbook to begin.")

# --- Data Cleaning and Mapping ---
def clean_and_map_data(df):
    columns = [col.lower() for col in df.columns]
    mapping = {
        'generation': None,
        'transmission': None,
        'substation': None,
        'distribution': None,
        'consumer': None
    }
    for key in mapping:
        for col in df.columns:
            if key in col.lower():
                mapping[key] = col
                break
    missing = [k for k, v in mapping.items() if v is None]
    if missing:
        st.warning(f"Could not find columns for: {', '.join(missing)}. Please ensure your Excel file has columns named for each hierarchy level (e.g., 'Generation', 'Transmission', etc.).")
    return mapping

# --- Visualization ---
def show_hierarchy(df, mapping):
    st.header("Hierarchy Visualization")
    if not all(mapping.values()):
        st.info("Cannot visualize hierarchy until all levels are mapped. Please check your Excel column names.")
        return
    try:
        st.write("### Sample Hierarchy Table")
        st.dataframe(df[[mapping[k] for k in mapping if mapping[k] is not None]].head(20))
        st.write("### Textual Hierarchy (first 5 rows)")
        for i, row in df.iterrows():
            st.write(f"- Generation: {row[mapping['generation']]} -> Transmission: {row[mapping['transmission']]} -> Substation: {row[mapping['substation']]} -> Distribution: {row[mapping['distribution']]} -> Consumer: {row[mapping['consumer']]}")
            if i >= 4:
                break
    except Exception as e:
        st.error(f"Error displaying hierarchy: {e}")

# --- Simulation ---
def simulate_flow():
    st.header("Simulate Electricity Flow")
    if not MODEL_AVAILABLE:
        st.error("Simulation model not found. Please ensure power_distribution.py is present and error-free.")
        st.button("Run Example Simulation", disabled=True)
        return
    if st.button("Run Example Simulation"):
        try:
            gen = Generation("Power Plant") if Generation else None
            trans = Transmission("High Voltage Line") if Transmission else None
            sub = Substation("City Substation") if Substation else None
            dist = Distribution("Local Distribution Line") if Distribution else None
            cons = Consumer("Residential Area") if Consumer else None
            if None in [gen, trans, sub, dist, cons]:
                st.error("Simulation classes are not available.")
                return
            e = gen.generate()  # type: ignore
            e = trans.transmit(e)
            e = sub.step_down(e)
            e = dist.distribute(e)
            cons.consume(e)
            st.success("Simulation complete! Check the output above.")
        except Exception as e:
            st.error(f"Simulation error: {e}")

# --- Main App Logic ---
if data is not None:
    mapping = clean_and_map_data(data)
    show_hierarchy(data, mapping)
    simulate_flow()
else:
    st.info("Upload an Excel file to begin.")