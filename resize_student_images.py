from pathlib import Path
from PIL import Image, ImageOps

ROOT_PATH = Path(__file__).resolve().parent


def main():
    student_photos_path = ROOT_PATH / "images" / "students"

    for student_photo_path in student_photos_path.iterdir():
        img = Image.open(student_photo_path)
        if max(img.size) <= 400:
            continue
        print(student_photo_path, "is", img.size, "resizing...")

        # Remove all exif tags
        # https://github.com/python-pillow/Pillow/issues/4346
        exif = img.getexif()
        for k in exif.keys():
            if k == 0x0112:
                continue

            # For some reason certain keys show up in the keys() list, but then still throw a KeyError
            try:
                # If I don't set it to None first (or print it) the del fails for some reason.
                exif[k] = None
                del exif[k]
            except KeyError:
                pass
        new_exif = exif.tobytes()
        img.info["exif"] = new_exif

        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
        img = ImageOps.exif_transpose(img)
        img.save(student_photo_path)


if __name__ == "__main__":
    main()
