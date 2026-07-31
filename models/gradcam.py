
import os
import torch
import torch.nn as nn
import cv2
import numpy as np

from torchvision import models, transforms
from PIL import Image

os.makedirs(
    "outputs",
    exist_ok=True
)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model = models.densenet121(
    weights=None
)

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

model.to(device)

model.eval()

gradients = None
activations = None


def save_gradient(grad):

    global gradients

    gradients = grad


def forward_hook(
    module,
    input,
    output
):

    global activations

    activations = output

    output.register_hook(
        save_gradient
    )


target_layer = model.features.norm5

target_layer.register_forward_hook(
    forward_hook
)

transform = transforms.Compose([
    transforms.Resize(
        (224, 224)
    ),
    transforms.ToTensor()
])


def generate_gradcam(image):

    global gradients
    global activations

    gradients = None
    activations = None

    image_rgb = image.convert(
        "RGB"
    )

    tensor = transform(
        image_rgb
    )

    tensor = tensor.unsqueeze(
        0
    ).to(device)

    output = model(
        tensor
    )

    pred_class = output.argmax(
        dim=1
    )

    model.zero_grad()

    output[
        0,
        pred_class
    ].backward(
        retain_graph=True
    )

    grads = gradients[0]

    acts = activations[0]

    grad_2 = grads.pow(2)

    grad_3 = grads.pow(3)

    eps = 1e-8

    alpha = grad_2 / (
        2 * grad_2
        + torch.sum(
            acts * grad_3,
            dim=(1, 2),
            keepdim=True
        )
        + eps
    )

    positive_gradients = torch.relu(
        grads
    )

    weights = torch.sum(
        alpha * positive_gradients,
        dim=(1, 2)
    )

    cam = torch.zeros(
        acts.shape[1:],
        dtype=torch.float32
    ).to(device)

    for i in range(
        len(weights)
    ):

        cam += (
            weights[i]
            * acts[i]
        )

    cam = torch.relu(
        cam
    )

    cam = cam.cpu()

    cam = cam.detach()

    cam = cam.numpy()

    cam -= np.min(
        cam
    )

    cam /= (
        np.max(cam)
        + 1e-8
    )

    cam = cv2.resize(
        cam,
        (224, 224)
    )

    cam = cv2.GaussianBlur(
        cam,
        (5, 5),
        0
    )

    threshold = 0.55

    cam[
        cam < threshold
    ] = 0

    heatmap = np.uint8(
        255 * cam
    )

    heatmap_color = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    heatmap_color[
        heatmap == 0
    ] = 0

    heatmap_color = cv2.cvtColor(
        heatmap_color,
        cv2.COLOR_BGR2RGB
    )

    image_np = np.array(
        image_rgb.resize(
            (224, 224)
        )
    )

    overlay = cv2.addWeighted(
        image_np,
        0.80,
        heatmap_color,
        0.40,
        0
    )

    heatmap_path = (
        "outputs/heatmap.png"
    )

    overlay_path = (
        "outputs/overlay.png"
    )

    cv2.imwrite(
        heatmap_path,
        cv2.cvtColor(
            heatmap_color,
            cv2.COLOR_RGB2BGR
        )
    )

    cv2.imwrite(
        overlay_path,
        cv2.cvtColor(
            overlay,
            cv2.COLOR_RGB2BGR
        )
    )

    return (
        heatmap_path,
        overlay_path
    )


