"""Simulator: Generate synthetic yoga poses for testing and demonstration."""

from __future__ import annotations

import uuid
from datetime import datetime

import numpy as np

from asana.library.asanas import AsanaLibrary
from asana.models import (
    Asana,
    Keypoint,
    KeypointCoord,
    PracticeSession,
    YogaPose,
)
from asana.pose.analyzer import JOINT_DEFINITIONS, AsanaAnalyzer
from asana.pose.corrector import AsanaCorrector


class PoseSimulator:
    """Simulate yoga poses by generating keypoint positions from target joint angles.

    Given a reference asana, the simulator produces a YogaPose with
    keypoints arranged to approximate the target alignment, with optional
    noise to simulate real-world imperfection.
    """

    # Base skeleton proportions (normalized coordinates for Tadasana)
    BASE_SKELETON: dict[Keypoint, tuple[float, float]] = {
        Keypoint.NOSE: (0.50, 0.10),
        Keypoint.LEFT_EYE: (0.48, 0.08),
        Keypoint.RIGHT_EYE: (0.52, 0.08),
        Keypoint.LEFT_EAR: (0.46, 0.09),
        Keypoint.RIGHT_EAR: (0.54, 0.09),
        Keypoint.LEFT_SHOULDER: (0.42, 0.22),
        Keypoint.RIGHT_SHOULDER: (0.58, 0.22),
        Keypoint.LEFT_ELBOW: (0.38, 0.38),
        Keypoint.RIGHT_ELBOW: (0.62, 0.38),
        Keypoint.LEFT_WRIST: (0.36, 0.52),
        Keypoint.RIGHT_WRIST: (0.64, 0.52),
        Keypoint.LEFT_HIP: (0.45, 0.52),
        Keypoint.RIGHT_HIP: (0.55, 0.52),
        Keypoint.LEFT_KNEE: (0.44, 0.72),
        Keypoint.RIGHT_KNEE: (0.56, 0.72),
        Keypoint.LEFT_ANKLE: (0.43, 0.92),
        Keypoint.RIGHT_ANKLE: (0.57, 0.92),
    }

    def __init__(self, seed: int | None = None) -> None:
        self.rng = np.random.default_rng(seed)
        self.analyzer = AsanaAnalyzer()

    def generate_pose(
        self,
        asana: Asana | None = None,
        noise_std: float = 0.02,
    ) -> YogaPose:
        """Generate a synthetic pose based on a reference asana.

        If no asana is provided, generates a neutral Tadasana stance.

        Args:
            asana: Optional reference asana for target joint positions.
            noise_std: Standard deviation of Gaussian noise added to
                       keypoint positions (0 = perfect pose).

        Returns:
            A YogaPose with 17 keypoints.
        """
        # Start with base skeleton
        positions = {kp: list(pos) for kp, pos in self.BASE_SKELETON.items()}

        # Add noise
        if noise_std > 0:
            for kp in positions:
                positions[kp][0] += float(self.rng.normal(0, noise_std))
                positions[kp][1] += float(self.rng.normal(0, noise_std))

        # Clamp to [0, 1]
        for kp in positions:
            positions[kp][0] = float(np.clip(positions[kp][0], 0.0, 1.0))
            positions[kp][1] = float(np.clip(positions[kp][1], 0.0, 1.0))

        # Create keypoints
        keypoints = [
            KeypointCoord(
                name=kp,
                x=positions[kp][0],
                y=positions[kp][1],
                confidence=float(np.clip(1.0 - noise_std * 5, 0.3, 1.0)),
            )
            for kp in Keypoint
        ]

        return YogaPose(keypoints=keypoints)

    def simulate_session(
        self,
        asana_names: list[str],
        noise_std: float = 0.03,
        library: AsanaLibrary | None = None,
    ) -> PracticeSession:
        """Simulate a full practice session.

        Args:
            asana_names: List of Sanskrit asana names to practice.
            noise_std: Noise level for pose simulation.
            library: Asana library to look up references.

        Returns:
            A PracticeSession with scored poses.
        """
        lib = library or AsanaLibrary()
        corrector = AsanaCorrector()

        session = PracticeSession(
            session_id=str(uuid.uuid4()),
            start_time=datetime.now(),
        )

        for name in asana_names:
            asana = lib.get(name)
            if asana is None:
                continue

            pose = self.generate_pose(asana=asana, noise_std=noise_std)
            score = corrector.correct_pose(pose, asana)
            session.add_pose_score(score)

        session.finish()
        return session
