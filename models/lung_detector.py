
import torch
import torch.nn as nn
from torchvision import transforms, models

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model = models.resnet18(weights=None)

model.fc = nn.Linear(
    model.fc.in_features,
    2
)

model.load_state_dict(
    torch.load(
        "lung_detector.pth",
        map_location=device
    )
)

model.to(device)
model.eval()

classes = [
    "LUNG_XRAY",
    "NOT_LUNG_XRAY"
]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def is_lung_xray(image):

    image = image.convert("RGB")

    image = transform(image)

    image = image.unsqueeze(0)

    image = image.to(device)

    with torch.no_grad():

        outputs = model(image)

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, predicted = torch.max(
            probabilities,
            1
        )

    return (
        classes[predicted.item()],
        confidence.item() * 100
    )

