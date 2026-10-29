from pathlib import Path
from PIL import Image, ImageOps

ROOT_PATH = Path(__file__).resolve().parent
IMAGES_PATH = ROOT_PATH / "images"

# Longest-edge size for student headshots vs. all other images.
STUDENT_SIZE = 400
DEFAULT_SIZE = 1200

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def max_size_for(image_path):
    rel = image_path.relative_to(IMAGES_PATH)

    # Leave the full-page background/hero images at full resolution.
    if rel.parent == Path(".") and rel.name.lower().startswith("background"):
        return None

    if rel.parts[0] == "students":
        return STUDENT_SIZE

    return DEFAULT_SIZE


def resize_image(image_path, max_size):
    img = Image.open(image_path)
    if max(img.size) <= max_size:
        return
    print(image_path, "is", img.size, "resizing...")

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

    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    img = ImageOps.exif_transpose(img)

    # JPEG can't store an alpha channel, so flatten transparency onto white.
    if image_path.suffix.lower() in {".jpg", ".jpeg"} and img.mode not in {"RGB", "L"}:
        img = img.convert("RGB")

    img.save(image_path)


def main():
    for image_path in sorted(IMAGES_PATH.rglob("*")):
        if not image_path.is_file():
            continue
        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        max_size = max_size_for(image_path)
        if max_size is None:
            continue

        resize_image(image_path, max_size)


if __name__ == "__main__":
    main()
