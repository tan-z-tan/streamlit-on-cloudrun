import io

import onnxruntime as ort
import streamlit as st
from PIL import Image

from app.model.rembg import RemBg


def main(model: RemBg, session: ort.InferenceSession):
    st.title("Background Remover")
    st.info("https://github.com/tan-z-tan/streamlit-on-cloudrun")

    img = None
    uploaded_file = st.file_uploader(
        "Choose a image", type=["jpg", "jpeg", "png"])

    # images area
    col1, col2 = st.columns(2)
    col1.header("Original Image")
    image_area = col1.empty()
    col2.header("Processed Image")
    res_image_area = col2.empty()

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        img_bin = io.BytesIO(bytes_data)

        img = Image.open(img_bin)

    if img is None:
        img = Image.open("samples/turtle.jpg")

    image_area.image(img)
    if img is not None:
        res_img = model.perform(img, session=session)
        res_image_area.image(res_img)


@st.experimental_singleton
def get_ort_session():
    session = ort.InferenceSession(
        "model_files/u2netp.onnx",
        providers=ort.get_available_providers()
        # "model_files/u2net.onnx", providers=ort.get_available_providers()
    )
    return session


if __name__ == "__main__":
    # call set_page_config before any calls of streamlit api
    st.set_page_config(
        layout="wide",
    )

    model = RemBg()
    session = get_ort_session()

    main(model, session)
