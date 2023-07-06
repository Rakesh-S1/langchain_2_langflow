import os
import streamlit as st


def redirect_to_url(url):
    js = f"window.location.href='{url}'"
    html = f"<script>{js}</script>"
    st.markdown(html, unsafe_allow_html=True)


def main():
    st.markdown(
        """
    <style>
    body {
        font-family: "Helvetica", sans-serif;
    }s
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
        if st.button("Langflow"):
            st.markdown("[langflow](https://huggingface.co/spaces/Logspace/LangFlow)")


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
