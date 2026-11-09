import os
from .auto_ndf.ocr import Océaire
from .auto_ndf.extractor import extract_date, extract_price
from .utils.file_utils import base64_image, collect_files, rename_img


def main():
    dir_path = "./img/"
    vllm_url = os.getenv("VLLM_URL", "http://auto-ndf-vllm:8000/v1")
    model_name = os.getenv("MODEL_NAME", "ovisocr2")

    # Get all files from ./img directory
    files_list = collect_files(dir_path)

    océaire = Océaire(model_name=model_name, vllm_url=vllm_url)

    for img_path in files_list:
        print(f"[LOG] Processing image {img_path}")

        # Load image and extract text
        img_b64 = base64_image(file_path=img_path)
        raw_text = océaire.parse(base64_image=img_b64)
        print(f"[LOG] Raw extracted text {raw_text}")

        # Parse dates and price from raw text
        dates = extract_date(raw_text)
        print(f"[LOG] Extracted dates: {dates}")

        moula = extract_price(raw_text)
        print(f"[LOG] Extracted Moula: {moula}")

        # Save renamed image
        print(f"[LOG] Saving file ./img_sorted/{dates[0]}_{moula}.jpeg ")
        rename_img(img_path, dates[0], moula)

        print("\n\n----------------------------------------------------\n\n")


if __name__ == "__main__":
    main()
    # cli()