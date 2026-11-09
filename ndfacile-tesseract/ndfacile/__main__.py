from .auto_ndf.ocr import Océaire
from .auto_ndf.extractor import extract_date, extract_price
from .utils.file_utils import load_image, collect_files, rename_img

 
def main():
    # Get all files from ./img directory
    dir_path = "./img/"
    files_list = collect_files(dir_path)

    for img_path in files_list:
        print(img_path)

        # Load image and extract text
        img = load_image(file_path=img_path)
        raw_text = Océaire.extract_text(img)
        print(raw_text)

        # Parse dates and price from raw text
        dates = extract_date(raw_text)
        print(dates)

        moula = extract_price(raw_text)
        print(f"Moula: {moula}")

        # Save renamed image
        print(f"Saving file ./img/parsed/{dates[0]}_{moula}.jpeg ")
        rename_img(img, dates[0], moula)

        print("\n\n----------------------------------------------------\n\n")


if __name__ == "__main__":
    main()
