
from torchvision.datasets import CIFAR10

dataset = CIFAR10(
    root="data",
    download=True
)

print("Dataset descargado")
print("Imágenes:", len(dataset))