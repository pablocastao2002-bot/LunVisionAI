
import torch
import torch.nn as nn

from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

test_dataset = datasets.ImageFolder(
    "data/processed/test",
    transform=transform
)

test_loader = DataLoader(
    test_dataset,
    batch_size=16,
    shuffle=False
)

model = models.densenet121(weights=None)

num_features = model.classifier.in_features

model.classifier = nn.Linear(
    num_features,
    2
)

model.load_state_dict(
    torch.load(
        "lung_model.pth",
        map_location=device
    )
)

model = model.to(device)

model.eval()

correct = 0
total = 0

with torch.no_grad():

    for images, labels in test_loader:

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

print()
print("Test Accuracy:", round(accuracy, 2), "%")
print("Total imágenes:", total)