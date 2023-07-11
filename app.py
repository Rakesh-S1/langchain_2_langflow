import os, io
import streamlit as st


def redirect_to_url(url):
    js = f"window.location.href='{url}'"
    html = f"<script>{js}</script>"
    st.markdown(html, unsafe_allow_html=True)


def main():
    # st.set_page_config(layout="wide")
    st.markdown(
        """
    <style>
    body {
        font-family: "Helvetica", sans-serif;
    },
    .file-upload-btn .stFileUploader > div:first-child {
        padding: 0.5rem 0.75rem;
        font-size: 14px;
        line-height: 1.5;
        border-radius: 0.2rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.title("Langchain to Langflow")
    left_column, right_column = st.columns(2)
    with left_column:
        input_file = st.file_uploader("Upload your Langchain File", type="py")
    if input_file is not None:
        with io.TextIOWrapper(input_file, encoding="utf-8", newline="") as file_wrapper:
            file_contents = file_wrapper.read()

        # Create a new file with the same contents
        with open("input1.py", "w", newline="") as new_file:
            new_file.write(file_contents)
            temp_file_path = new_file.name
            with right_column:
                st.write('')
                st.write('')
                st.code(f"File Name: {input_file.name}")
                st.code(f"File Size: {len(file_contents)} bytes")
        container = st.sidebar.container()
        with container:
            st.text_area("File Contents", file_contents, height=400)
        run_main()
        download_json()
        if st.button("Langflow"):
            st.markdown("[langflow](https://127.0.0.1/7860/)")


@st.cache_resource
def run_main():
    with open("main.py", "r") as file:
        file_contents = file.read()
    exec(file_contents)


def download_json():
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
