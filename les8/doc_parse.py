import re
from pathlib import Path
import PyPDF2
from PyPDF2.utils import PdfReadError
from PIL import Image
import pytesseract


def pdf_images_extract(pdf_path: Path, images_path: Path) -> list[Path]:
    result = []
    with pdf_path.open("rb") as file:
        print(1)
        try:
            pdf_file = PyPDF2.PdfFileReader(file)
        except PdfReadError:
            # TODO: Записать информацию о ошибке в БД или возбудить ошибку
            return result
        for page_num, page in enumerate(pdf_file.pages, 1):
            image_name = f"{pdf_path.name}_{page_num}"
            img_path = images_path.joinpath(image_name)
            img_path.write_bytes(page['/Resources']['/XObject']['/Im0']._data)
            result.append(img_path)
    return result


# TODO: Извлечь из изображения серийные номера
def get_serial_numbers(image_path: Path) -> list[str]:
    image = Image.open(image_path)
    text_rus = pytesseract.image_to_string(image, "rus")
    pattern = re.compile(r"([з|З]аводской.*[номер|№])")
    matches = len(re.findall(pattern, text_rus))
    result = []
    if matches:
        text_eng = pytesseract.image_to_string(image, "eng").split("\n")
        for idx, string in enumerate(text_rus.split("\n")):
            if re.match(pattern, string):
                number = text_eng[idx].split(" ")[-1]
                result.append(number)
                if len(result) == matches:
                    break
    return result


def get_dir_path(dirname: str) -> Path:
    dir_path = Path(__file__).parent.joinpath(dirname)
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path


if __name__ == '__main__':
    images_path = get_dir_path("images")
    pdf_path = Path(__file__).parent.joinpath("8416_4.pdf")
    images = pdf_images_extract(pdf_path, images_path)
    numbers = list(map(get_serial_numbers, images))
    print(1)
