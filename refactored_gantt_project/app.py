import streamlit as st
import tempfile
import os
from gantt.service import process_file

st.set_page_config(page_title="Gantt Generator", page_icon="📊")

st.title("📊 Gantt Chart Generator")
st.write("Upload your project Excel file and generate a Gantt chart.")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    st.success("File uploaded successfully!")

    if st.button("Generate Gantt Chart"):
        with st.spinner("Processing..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_input:
                temp_input.write(uploaded_file.read())
                input_path = temp_input.name

            output_path = input_path.replace(".xlsx", "_output.xlsx")

            try:
                process_file(input_path, output_path)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Gantt Chart",
                        data=f,
                        file_name="gantt_chart.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                st.success("✅ Gantt chart generated!")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

            finally:
                if os.path.exists(input_path):
                    os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
