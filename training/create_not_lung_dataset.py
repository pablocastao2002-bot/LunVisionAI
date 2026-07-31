
from torchvision.datasets import CIFAR10
from PIL import Image
import os

# Descargar/cargar CIFAR10
dataset = CIFAR10(
    root="data",
    train=True,
    download=False
)

output_dir = "data/lung_detector_raw/NOT_LUNG_XRAY"

os.makedirs(output_dir, exist_ok=True)

num_images = 2000

for i in range(num_images):
    image, label = dataset[i]

    filename = os.path.join(
        output_dir,
        f"not_lung_{i}.jpg"
    )

    image.save(filename)

print(f"{num_images} imágenes guardadas en NOT_LUNG_XRAY")
