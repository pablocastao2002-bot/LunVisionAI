
import os
import shutil

SOURCE = r"data/archive/The IQ-OTHNCCD lung cancer dataset/The IQ-OTHNCCD lung cancer dataset"

DEST = r"data/lung_detector_raw/LUNG_XRAY"

os.makedirs(
    DEST,
    exist_ok=True
)

folders = [
    "Normal cases",
    "Bengin cases",
    "Malignant cases"
]

count = 0

for folder in folders:

    path = os.path.join(
        SOURCE,
        folder
    )

    for file in os.listdir(path):

        if file.lower().endswith(
            (".png", ".jpg", ".jpeg")
        ):

            shutil.copy(
                os.path.join(path, file),
                os.path.join(
                    DEST,
                    f"{count}_{file}"
                )
            )

            count += 1

print(
    f"Copiadas {count} imágenes"
)
