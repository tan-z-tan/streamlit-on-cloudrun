from io import BytesIO

import numpy as np
import onnxruntime as ort
from PIL import Image, ImageFile
from rembg.bg import alpha_matting_cutout
from rembg.detect import predict

ImageFile.LOAD_TRUNCATED_IMAGES = True


class RemBg:
    def perform(self, img: Image, session: ort.InferenceSession) -> Image:
        mask = predict(session, np.array(img)).convert("L")
        try:
            cutout = alpha_matting_cutout(
                img,
                mask,
                foreground_threshold=240,
                background_threshold=10,
                erode_structure_siz=10,
                erode_structure_size=1000,
            )
        except Exception:
            empty = Image.new("RGBA", (img.size), 0)
            cutout = Image.composite(img, empty, mask.resize(img.size, Image.LANCZOS))

        bio = BytesIO()
        cutout.save(bio, "PNG")
        bio.seek(0)
        return bio.read()


if __name__ == "__main__":
    path = "model_files/u2net.onnx"
    session = ort.InferenceSession(str(path), providers=ort.get_available_providers())

    res_img = RemBg().perform("samples/turtle.jpg", session)
    res_img.show()
