
import os
import torch
import torch.nn as nn
import torch.optim as optim

from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Dispositivo:", device)

# Transformaciones
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# Dataset
train_dataset = datasets.ImageFolder(
    "data/processed/train",
    transform=transform
)

val_dataset = datasets.ImageFolder(
    "data/processed/val",
    transform=transform
)

train_loader = DataLoader(
    train_dataset,
    batch_size=16,
    shuffle=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=16,
    shuffle=False
)

# DenseNet121 preentrenado
model = models.densenet121(weights="DEFAULT")

num_features = model.classifier.in_features

model.classifier = nn.Linear(
    num_features,
    2
)

model = model.to(device)

criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(
    model.parameters(),
    lr=0.0001
)

epochs = 5

best_acc = 0

for epoch in range(epochs):

    model.train()

    running_loss = 0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(
            outputs,
            labels
        )

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

            _, predicted = torch.max(
                outputs,
                1
            )

            total += labels.size(0)

            correct += (
                predicted == labels
            ).sum().item()

    accuracy = 100 * correct / total

    print(
        f"Epoch {epoch+1}/{epochs} | "
        f"Loss: {running_loss:.4f} | "
        f"Val Accuracy: {accuracy:.2f}%"
    )

    if accuracy > best_acc:

        best_acc = accuracy

        torch.save(
            model.state_dict(),
            "lung_model.pth"
        )

        print("Modelo guardado")

print("\nEntrenamiento finalizado")
print("Mejor accuracy:", best_acc)