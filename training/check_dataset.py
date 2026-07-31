
import os

dataset_path = r"data/archive/The IQ-OTHNCCD lung cancer dataset/The IQ-OTHNCCD lung cancer dataset"

print("Ruta:", dataset_path)
print()

for folder in os.listdir(dataset_path):

    folder_path = os.path.join(
        dataset_path,
        folder
    )

    if os.path.isdir(folder_path):

        files = []

        for f in os.listdir(folder_path):

            if f.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ):
                files.append(f)

        print(
            f"{folder}: {len(files)} imágenes"
        )