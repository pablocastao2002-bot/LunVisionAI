
import torch
import torch.nn as nn
import torch.optim as optim

from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split

# GPU
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Dispositivo:", device)

# Transformaciones
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Dataset
dataset = datasets.ImageFolder(
    "data/lung_detector_raw",
    transform=transform
)

print("Clases:", dataset.classes)
print("Imágenes:", len(dataset))

# División entrenamiento/validación
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size

train_dataset, val_dataset = random_split(
    dataset,
    [train_size, val_size]
)

train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=32,
    shuffle=False
)

# Modelo
model = models.resnet18(weights="DEFAULT")

model.fc = nn.Linear(
    model.fc.in_features,
    2
)

model = model.to(device)

criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(
    model.parameters(),
    lr=0.0001
)

best_acc = 0

# Entrenamiento
for epoch in range(5):

    model.train()

    running_loss = 0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    # Validación
    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            _, predicted = torch.max(outputs, 1)

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    acc = 100 * correct / total

    print(
        f"Epoch {epoch+1}/5 | "
        f"Loss: {running_loss:.4f} | "
        f"Val Accuracy: {acc:.2f}%"
    )

    if acc > best_acc:

        best_acc = acc

        torch.save(
            model.state_dict(),
            "lung_detector.pth"
        )

print()
print("Entrenamiento finalizado")
print("Mejor accuracy:", best_acc)