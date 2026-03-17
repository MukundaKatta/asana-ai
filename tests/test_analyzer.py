"""Tests for AsanaAnalyzer and joint angle computation."""

import math

import pytest

from asana.models import (
    Asana,
    DifficultyLevel,
    Keypoint,
    KeypointCoord,
    YogaPose,
)
from asana.pose.analyzer import AsanaAnalyzer


def _make_pose(overrides: dict[Keypoint, tuple[float, float]] | None = None) -> YogaPose:
    """Create a test pose with optional keypoint overrides."""
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


class TestComputeAngle:
    def test_right_angle(self):
        # Points forming a right angle at B
        angle = AsanaAnalyzer.compute_angle(
            (0.0, 0.0), (0.0, 1.0), (1.0, 1.0)
        )
        assert angle == pytest.approx(90.0, abs=0.1)

    def test_straight_line(self):
        # Collinear points -> 180 degrees
        angle = AsanaAnalyzer.compute_angle(
            (0.0, 0.0), (0.5, 0.0), (1.0, 0.0)
        )
        assert angle == pytest.approx(180.0, abs=0.1)

    def test_acute_angle(self):
        # 60-degree angle
        angle = AsanaAnalyzer.compute_angle(
            (1.0, 0.0), (0.0, 0.0), (0.5, math.sqrt(3) / 2)
        )
        assert angle == pytest.approx(60.0, abs=0.1)

    def test_zero_length_vector(self):
        # Coincident points -> 0 degrees
        angle = AsanaAnalyzer.compute_angle(
            (0.5, 0.5), (0.5, 0.5), (1.0, 1.0)
        )
        assert angle == 0.0


class TestAsanaAnalyzer:
    def setup_method(self):
        self.analyzer = AsanaAnalyzer()

    def test_compute_joint_angles(self):
        pose = _make_pose()
        angles = self.analyzer.compute_joint_angles(pose)
        assert len(angles) > 0
        for ja in angles:
            assert 0.0 <= ja.angle_degrees <= 360.0

    def test_score_joint_within_tolerance(self):
        score = self.analyzer.score_joint(90.0, 90.0, 15.0)
        assert score == 100.0

    def test_score_joint_at_tolerance_edge(self):
        score = self.analyzer.score_joint(105.0, 90.0, 15.0)
        assert score == 100.0

    def test_score_joint_beyond_tolerance(self):
        score = self.analyzer.score_joint(120.0, 90.0, 15.0)
        assert score < 100.0

    def test_score_joint_extreme_deviation(self):
        score = self.analyzer.score_joint(180.0, 90.0, 15.0)
        assert score == 0.0

    def test_analyze_returns_pose_score(self):
        pose = _make_pose()
        asana = Asana(
            sanskrit_name="Test",
            english_name="Test Pose",
            description="Test",
            difficulty=DifficultyLevel.BEGINNER,
            target_joint_angles={"left_knee": 170.0, "right_knee": 170.0},
            benefits=["Testing"],
        )
        result = self.analyzer.analyze(pose, asana)
        assert result.asana_name == "Test"
        assert 0.0 <= result.overall_score <= 100.0
        assert "left_knee" in result.joint_scores

    def test_identify_asana(self):
        pose = _make_pose()
        asanas = [
            Asana(
                sanskrit_name="A",
                english_name="Pose A",
                description="A",
                difficulty=DifficultyLevel.BEGINNER,
                target_joint_angles={"left_knee": 170.0},
                benefits=["A"],
            ),
        ]
        results = self.analyzer.identify_asana(pose, asanas, threshold=0.0)
        assert len(results) >= 1
