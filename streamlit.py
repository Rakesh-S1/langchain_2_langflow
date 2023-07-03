import streamlit as st
import os


def main():
    st.markdown(
        """
    <style>
    body {
        font-family: "Helvetica", sans-serif;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.title("Langchain to Langflow")
    input_file = st.file_uploader("Upload your Langchain File", type="py")
    if input_file is not None:
        data = input_file.read()
        # st.code(data)
        with open("input1.py", "w") as temp_file:
            temp_file.write(data.decode("utf-8"))
            temp_file_path = temp_file.name
            st.code(temp_file_path)
        run_main()


def run_main():
    with open("main.py", "r") as file:
        file_contents = file.read()
    exec(file_contents)

    st.title("Download JSON File")
    file = "converted.json"
    if os.path.isfile(file):
        st.download_button(
            label="Download JSON",
            data=open(file, "rb"),
            file_name=file,
            mime="application/json",
        )
    else:
        st.write("JSON file not found.")


if __name__ == "__main__":
    main()


