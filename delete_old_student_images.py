from pathlib import Path
import yaml

ROOT_PATH = Path(__file__).resolve().parent
STUDENTS_YML = ROOT_PATH / "_data" / "students.yaml"


def main():
    student_photos_path = ROOT_PATH / "images" / "students"

    with open(STUDENTS_YML) as f:
        students = yaml.safe_load(f)
    images = [p["image"] for t in students for p in students[t]]

    for student_photo_path in student_photos_path.iterdir():
        if student_photo_path.name not in images:
            student_photo_path.unlink()


if __name__ == "__main__":
    main()
