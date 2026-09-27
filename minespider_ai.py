from ultralytics import YOLO
import cv2
import os

# ============================================================
# MineSpider AI - Person + Rockfall Detection
# ============================================================

PERSON_MODEL = r"C:\MineSpider\models\person_model.pt"
ROCK_MODEL = r"C:\MineSpider\models\rock_model.pt"

# Confidence thresholds
PERSON_CONF = 0.40
ROCK_CONF = 0.45

# Load models
print("Loading MineSpider AI models...")

person_model = YOLO(PERSON_MODEL)
rock_model = YOLO(ROCK_MODEL)

print("Person model loaded.")
print("Rockfall model loaded.")


def detect_minespider(image_path):

    if not os.path.exists(image_path):
        print(f"\nERROR: Image not found:")
        print(image_path)
        return

    image = cv2.imread(image_path)

    if image is None:
        print("ERROR: Could not read image.")
        return

    # --------------------------------------------------------
    # PERSON DETECTION
    # --------------------------------------------------------

    person_results = person_model.predict(
        source=image,
        conf=PERSON_CONF,
        verbose=False
    )

    # --------------------------------------------------------
    # ROCKFALL DETECTION
    # --------------------------------------------------------

    rock_results = rock_model.predict(
        source=image,
        conf=ROCK_CONF,
        verbose=False
    )

    person_count = 0
    rock_count = 0

    # --------------------------------------------------------
    # Draw PERSON detections
    # --------------------------------------------------------

    for result in person_results:

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            person_count += 1

            # Blue box = Person
            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

            label = f"PERSON {confidence:.2f}"

            cv2.putText(
                image,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 0, 0),
                2
            )

    # --------------------------------------------------------
    # Draw ROCKFALL detections
    # --------------------------------------------------------

    for result in rock_results:

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            rock_count += 1

            # Red box = Rockfall
            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (0, 0, 255),
                2
            )

            label = f"ROCKFALL {confidence:.2f}"

            cv2.putText(
                image,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 0, 255),
                2
            )

    # --------------------------------------------------------
    # MineSpider status
    # --------------------------------------------------------

    if person_count > 0 and rock_count > 0:
        status = "PERSON + ROCKFALL DETECTED"

    elif person_count > 0:
        status = "PERSON DETECTED"

    elif rock_count > 0:
        status = "ROCKFALL DETECTED"

    else:
        status = "AREA CLEAR"

    # --------------------------------------------------------
    # Information panel
    # --------------------------------------------------------

    panel_height = 115

    cv2.rectangle(
        image,
        (0, 0),
        (image.shape[1], panel_height),
        (25, 25, 25),
        -1
    )

    cv2.putText(
        image,
        "MINESPIDER AI",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        image,
        f"Persons: {person_count}",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 0, 0),
        2
    )

    cv2.putText(
        image,
        f"Rockfalls: {rock_count}",
        (200, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 0, 255),
        2
    )

    cv2.putText(
        image,
        f"STATUS: {status}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 0) if person_count == 0 and rock_count == 0 else (0, 165, 255),
        2
    )

    # --------------------------------------------------------
    # Save result
    # --------------------------------------------------------

    output_dir = r"C:\MineSpider\results"
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.basename(image_path)

    output_path = os.path.join(
        output_dir,
        "minespider_" + filename
    )

    cv2.imwrite(output_path, image)

    print("\n========================================")
    print("        MINESPIDER AI RESULT")
    print("========================================")
    print(f"Persons detected : {person_count}")
    print(f"Rockfalls detected: {rock_count}")
    print(f"Status           : {status}")
    print(f"Result saved to  : {output_path}")
    print("========================================")

    # Display result
    cv2.imshow("MineSpider AI", image)

    print("\nPress any key on the image window to close.")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    image_path = input(
        "\nEnter image path for MineSpider detection: "
    ).strip().strip('"')

    detect_minespider(image_path)