
import torch
import torch.nn as nn

from torchvision import transforms, models
from PIL import Image

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
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

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

classes = [
    "CANCER",
    "NORMAL"
]

def predict(image):

    image = image.convert("RGB")

    image = transform(image)

    image = image.unsqueeze(0)

    image = image.to(device)

    with torch.no_grad():

        output = model(image)

        probabilities = torch.softmax(
            output,
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