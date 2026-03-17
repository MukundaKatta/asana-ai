"""YogaPoseDetector: CNN-based 17-keypoint pose detection."""

from __future__ import annotations

from typing import Optional

import numpy as np
import torch
import torch.nn as nn

from asana.models import Keypoint, KeypointCoord, YogaPose


class KeypointHead(nn.Module):
    """Heatmap regression head that produces one heatmap per keypoint."""

    def __init__(self, in_channels: int, num_keypoints: int = 17):
        super().__init__()
        self.deconv = nn.Sequential(
            nn.ConvTranspose2d(in_channels, 256, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
        )
        self.final_conv = nn.Conv2d(64, num_keypoints, kernel_size=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.deconv(x)
        return self.final_conv(x)


class YogaPoseDetector(nn.Module):
    """Convolutional neural network for detecting 17 anatomical keypoints.

    Architecture:
        - Backbone: series of Conv2d blocks with batch norm and max pooling
        - Head: transposed convolutions producing heatmaps for each keypoint
        - Soft-argmax decoding to extract sub-pixel keypoint coordinates

    The model accepts an RGB image tensor of shape (B, 3, 256, 256) and outputs
    normalized (x, y) coordinates for each of the 17 keypoints along with a
    per-keypoint confidence score.
    """

    NUM_KEYPOINTS = 17
    INPUT_SIZE = 256

    KEYPOINT_NAMES: list[Keypoint] = list(Keypoint)

    def __init__(self, pretrained_path: Optional[str] = None):
        super().__init__()

        self.backbone = nn.Sequential(
            # Block 1: 3 -> 64, 256 -> 128
            nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            # Block 2: 64 -> 128, 64 -> 32
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            # Block 3: 128 -> 256, 32 -> 16
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            # Block 4: 256 -> 512, 16 -> 8
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
        )

        self.head = KeypointHead(in_channels=512, num_keypoints=self.NUM_KEYPOINTS)

        if pretrained_path:
            self.load_state_dict(torch.load(pretrained_path, map_location="cpu"))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass producing keypoint heatmaps.

        Args:
            x: Input tensor of shape (B, 3, 256, 256).

        Returns:
            Heatmaps of shape (B, 17, H, W).
        """
        features = self.backbone(x)
        heatmaps = self.head(features)
        return heatmaps

    def decode_heatmaps(
        self, heatmaps: torch.Tensor
    ) -> tuple[np.ndarray, np.ndarray]:
        """Decode heatmaps into keypoint coordinates and confidences.

        Uses soft-argmax for sub-pixel accuracy.

        Args:
            heatmaps: Tensor of shape (B, 17, H, W).

        Returns:
            coords: Array of shape (B, 17, 2) with normalized (x, y).
            confidences: Array of shape (B, 17) with confidence values.
        """
        batch_size, num_kp, h, w = heatmaps.shape

        # Soft-argmax decoding
        heatmaps_flat = heatmaps.view(batch_size, num_kp, -1)
        softmax = torch.softmax(heatmaps_flat, dim=-1)

        # Create coordinate grids
        grid_y, grid_x = torch.meshgrid(
            torch.linspace(0, 1, h, device=heatmaps.device),
            torch.linspace(0, 1, w, device=heatmaps.device),
            indexing="ij",
        )
        grid_x = grid_x.reshape(-1)
        grid_y = grid_y.reshape(-1)

        # Weighted sum for expected coordinates
        x_coords = (softmax * grid_x.unsqueeze(0).unsqueeze(0)).sum(dim=-1)
        y_coords = (softmax * grid_y.unsqueeze(0).unsqueeze(0)).sum(dim=-1)

        coords = torch.stack([x_coords, y_coords], dim=-1)

        # Confidence is the max value of the softmax
        confidences = softmax.max(dim=-1).values

        return coords.detach().cpu().numpy(), confidences.detach().cpu().numpy()

    @torch.no_grad()
    def detect(self, image_tensor: torch.Tensor) -> list[YogaPose]:
        """Run full detection pipeline on a batch of images.

        Args:
            image_tensor: Tensor of shape (B, 3, 256, 256), values in [0, 1].

        Returns:
            List of YogaPose objects, one per image in the batch.
        """
        self.eval()
        heatmaps = self.forward(image_tensor)
        coords, confidences = self.decode_heatmaps(heatmaps)

        poses: list[YogaPose] = []
        for b in range(coords.shape[0]):
            keypoints = []
            for k in range(self.NUM_KEYPOINTS):
                kp = KeypointCoord(
                    name=self.KEYPOINT_NAMES[k],
                    x=float(np.clip(coords[b, k, 0], 0.0, 1.0)),
                    y=float(np.clip(coords[b, k, 1], 0.0, 1.0)),
                    confidence=float(confidences[b, k]),
                )
                keypoints.append(kp)
            poses.append(YogaPose(keypoints=keypoints))

        return poses

    @staticmethod
    def preprocess_image(image_array: np.ndarray) -> torch.Tensor:
        """Preprocess a numpy image (H, W, 3) uint8 into a model-ready tensor.

        Args:
            image_array: RGB image as numpy array, shape (H, W, 3), dtype uint8.

        Returns:
            Tensor of shape (1, 3, 256, 256), values in [0, 1].
        """
        from torch.nn.functional import interpolate

        img = torch.from_numpy(image_array).float() / 255.0
        img = img.permute(2, 0, 1).unsqueeze(0)  # (1, 3, H, W)
        img = interpolate(img, size=(256, 256), mode="bilinear", align_corners=False)
        return img
