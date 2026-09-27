from flask import Flask, render_template, request, url_for, send_from_directory
from ultralytics import YOLO
from werkzeug.utils import secure_filename
from pathlib import Path
import cv2
import os
import uuid

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
RESULT_DIR = BASE_DIR / "results"

UPLOAD_DIR.mkdir(exist_ok=True)
RESULT_DIR.mkdir(exist_ok=True)

# ============================================================
# MineSpider trained models
# ============================================================

PERSON_MODEL = str(BASE_DIR / "models" / "person_model.pt")
ROCK_MODEL = str(BASE_DIR / "models" / "rock_model.pt")

PERSON_CONF = 0.40
ROCK_CONF = 0.45

print("Loading MineSpider AI models...")

person_model = YOLO(PERSON_MODEL)
rock_model = YOLO(ROCK_MODEL)

print("Person model loaded.")
print("Rockfall model loaded.")


ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ============================================================
# AI DETECTION
# ============================================================

def run_detection(input_path, output_path):

    image = cv2.imread(str(input_path))

    if image is None:
        raise ValueError("Could not read uploaded image.")

    person_count = 0
    rock_count = 0

    # --------------------------------------------------------
    # PERSON MODEL
    # --------------------------------------------------------

    person_results = person_model.predict(
        source=image,
        conf=PERSON_CONF,
        verbose=False
    )

    for result in person_results:

        for box in result.boxes:

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            confidence = float(box.conf[0])

            person_count += 1

            # BLUE = PERSON
            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (255, 90, 50),
                3
            )

            cv2.putText(
                image,
                f"PERSON {confidence:.2f}",
                (x1, max(y1 - 10, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 90, 50),
                2
            )

    # --------------------------------------------------------
    # ROCKFALL MODEL
    # --------------------------------------------------------

    rock_results = rock_model.predict(
        source=image,
        conf=ROCK_CONF,
        verbose=False
    )

    for result in rock_results:

        for box in result.boxes:

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            confidence = float(box.conf[0])

            rock_count += 1

            # RED = ROCKFALL
            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (70, 70, 255),
                3
            )

            cv2.putText(
                image,
                f"ROCKFALL {confidence:.2f}",
                (x1, max(y1 - 10, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (70, 70, 255),
                2
            )

    # --------------------------------------------------------
    # SYSTEM STATUS
    # --------------------------------------------------------

    if person_count > 0 and rock_count > 0:

        status = "MULTIPLE HAZARDS"
        status_type = "critical"

    elif rock_count > 0:

        status = "ROCKFALL DETECTED"
        status_type = "danger"

    elif person_count > 0:

        status = "PERSON DETECTED"
        status_type = "warning"

    else:

        status = "SECTOR CLEAR"
        status_type = "safe"

    # --------------------------------------------------------
    # SAVE IMAGE
    # --------------------------------------------------------

    cv2.imwrite(
        str(output_path),
        image
    )

    return (
        person_count,
        rock_count,
        status,
        status_type
    )


# ============================================================
# HOME
# ============================================================

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        file = request.files.get("image")

        if not file or file.filename == "":
            return render_template(
                "index.html",
                error="Please select an image."
            )

        if not allowed_file(file.filename):
            return render_template(
                "index.html",
                error="Only JPG, JPEG, PNG and WEBP files are supported."
            )

        job_id = uuid.uuid4().hex[:8]

        original_name = secure_filename(
            file.filename
        )

        input_name = (
            f"{job_id}_{original_name}"
        )

        output_name = (
            f"{job_id}_result.jpg"
        )

        input_path = (
            UPLOAD_DIR / input_name
        )

        output_path = (
            RESULT_DIR / output_name
        )

        file.save(input_path)

        try:

            (
                persons,
                rocks,
                status,
                status_type
            ) = run_detection(
                input_path,
                output_path
            )

        except Exception as e:

            return render_template(
                "index.html",
                error=f"Detection failed: {e}"
            )

        return render_template(
            "result.html",

            result_image=url_for(
                "result_file",
                filename=output_name
            ),

            persons=persons,
            rocks=rocks,

            status=status,
            status_type=status_type
        )

    return render_template(
        "index.html"
    )


# ============================================================
# RESULT IMAGE
# ============================================================

@app.route("/results/<filename>")
def result_file(filename):

    return send_from_directory(
        RESULT_DIR,
        filename
    )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("")
    print("========================================")
    print("        MINESPIDER COMMAND CENTER")
    print("========================================")
    print("")
    print("Open:")
    print("http://127.0.0.1:5000")
    print("")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )