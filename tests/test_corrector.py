"""Tests for AsanaCorrector."""

import pytest

from asana.library.asanas import AsanaLibrary
from asana.models import (
    Keypoint,
    KeypointCoord,
    Severity,
    YogaPose,
)
from asana.pose.corrector import AsanaCorrector


def _make_pose(overrides: dict[Keypoint, tuple[float, float]] | None = None) -> YogaPose:
    defaults: dict[Keypoint, tuple[float, float]] = {
        Keypoint.NOSE: (0.50, 0.10),
        Keypoint.LEFT_EYE: (0.48, 0.08),
        Keypoint.RIGHT_EYE: (0.52, 0.08),
        Keypoint.LEFT_EAR: (0.46, 0.09),
        Keypoint.RIGHT_EAR: (0.54, 0.09),
        Keypoint.LEFT_SHOULDER: (0.40, 0.25),
        Keypoint.RIGHT_SHOULDER: (0.60, 0.25),
        Keypoint.LEFT_ELBOW: (0.35, 0.40),
        Keypoint.RIGHT_ELBOW: (0.65, 0.40),
        Keypoint.LEFT_WRIST: (0.30, 0.55),
        Keypoint.RIGHT_WRIST: (0.70, 0.55),
        Keypoint.LEFT_HIP: (0.45, 0.55),
        Keypoint.RIGHT_HIP: (0.55, 0.55),
        Keypoint.LEFT_KNEE: (0.44, 0.75),
        Keypoint.RIGHT_KNEE: (0.56, 0.75),
        Keypoint.LEFT_ANKLE: (0.43, 0.95),
        Keypoint.RIGHT_ANKLE: (0.57, 0.95),
    }
    if overrides:
        defaults.update(overrides)
    keypoints = [
        KeypointCoord(name=kp, x=pos[0], y=pos[1], confidence=1.0)
        for kp, pos in defaults.items()
    ]
    return YogaPose(keypoints=keypoints)


class TestAsanaCorrector:
    def setup_method(self):
        self.corrector = AsanaCorrector()
        self.library = AsanaLibrary()

    def test_generate_corrections(self):
        pose = _make_pose()
        asana = self.library.get("Tadasana")
        assert asana is not None
        corrections = self.corrector.generate_corrections(pose, asana)
        assert isinstance(corrections, list)

    def test_corrections_sorted_by_severity(self):
        pose = _make_pose()
        asana = self.library.get("Virabhadrasana_I")
        assert asana is not None
        corrections = self.corrector.generate_corrections(pose, asana)
        if len(corrections) >= 2:
            severity_order = {Severity.CRITICAL: 0, Severity.WARNING: 1, Severity.INFO: 2}
            for i in range(len(corrections) - 1):
                assert severity_order[corrections[i].severity] <= severity_order[corrections[i + 1].severity]

    def test_correct_pose_returns_score_with_corrections(self):
        pose = _make_pose()
        asana = self.library.get("Virabhadrasana_II")
        assert asana is not None
        score = self.corrector.correct_pose(pose, asana)
        assert score.asana_name == "Virabhadrasana_II"
        assert 0.0 <= score.overall_score <= 100.0

    def test_corrections_have_instructions(self):
        pose = _make_pose()
        asana = self.library.get("Virabhadrasana_I")
        assert asana is not None
        corrections = self.corrector.generate_corrections(pose, asana)
        for c in corrections:
            assert len(c.instruction) > 0
            assert len(c.body_part) > 0

    def test_perfect_pose_no_corrections(self):
        """A pose within all tolerances should have zero corrections."""
        # Create a simple asana where the default pose angles match
        from asana.models import Asana, DifficultyLevel
        # Use very wide tolerances to guarantee a match
        asana = Asana(
            sanskrit_name="Easy",
            english_name="Easy",
            description="Easy",
            difficulty=DifficultyLevel.BEGINNER,
            target_joint_angles={"left_knee": 170.0},
            angle_tolerance={"left_knee": 90.0},  # very wide tolerance
            benefits=["Test"],
        )
        pose = _make_pose()
        corrections = self.corrector.generate_corrections(pose, asana)
        assert len(corrections) == 0
