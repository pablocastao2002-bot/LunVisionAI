
import os
import shutil
import random

from sklearn.model_selection import train_test_split

random.seed(42)

SOURCE = r"data/archive/The IQ-OTHNCCD lung cancer dataset/The IQ-OTHNCCD lung cancer dataset"

DEST = r"data/processed"

os.makedirs(DEST, exist_ok=True)

for split in ["train", "val", "test"]:
    for cls in ["NORMAL", "CANCER"]:
        os.makedirs(
            os.path.join(
                DEST,
                split,
                cls
            ),
            exist_ok=True
        )

normal_folder = os.path.join(
    SOURCE,
    "Normal cases"
)

benign_folder = os.path.join(
    SOURCE,
    "Bengin cases"
)

malignant_folder = os.path.join(
    SOURCE,
    "Malignant cases"
)

normal_images = [
    os.path.join(normal_folder, f)
    for f in os.listdir(normal_folder)
    if f.lower().endswith(
        (".jpg", ".png", ".jpeg")
    )
]

cancer_images = []

for folder in [
    benign_folder,
    malignant_folder
]:

    cancer_images.extend([
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(
            (".jpg", ".png", ".jpeg")
        )
    ])

train_normal, temp_normal = train_test_split(
    normal_images,
    test_size=0.2,
    random_state=42
)

val_normal, test_normal = train_test_split(
    temp_normal,
    test_size=0.5,
    random_state=42
)

train_cancer, temp_cancer = train_test_split(
    cancer_images,
    test_size=0.2,
    random_state=42
)

val_cancer, test_cancer = train_test_split(
    temp_cancer,
    test_size=0.5,
    random_state=42
)

def copy_files(files, split, cls):

    for file in files:

        shutil.copy(
            file,
            os.path.join(
                DEST,
                split,
                cls
            )
        )

copy_files(
    train_normal,
    "train",
    "NORMAL"
)

copy_files(
    val_normal,
    "val",
    "NORMAL"
)

copy_files(
    test_normal,
    "test",
    "NORMAL"
)

copy_files(
    train_cancer,
    "train",
    "CANCER"
)

copy_files(
    val_cancer,
    "val",
    "CANCER"
)

copy_files(
    test_cancer,
    "test",
    "CANCER"
)

print("Dataset preparado correctamente")