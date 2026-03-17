"""Tests for Pydantic data models."""

from datetime import datetime

import pytest

from asana.models import (
    Asana,
    BreathPhase,
    BreathingPattern,
    Correction,
    DifficultyLevel,
    Keypoint,
    KeypointCoord,
    PoseScore,
    PracticeSession,
    Severity,
    YogaPose,
)


def _make_keypoints() -> list[KeypointCoord]:
    """Create a full set of 17 keypoints for testing."""
    return [
        KeypointCoord(name=kp, x=0.5, y=0.5, confidence=0.9)
        for kp in Keypoint
    ]


class TestKeypointCoord:
    def test_valid_keypoint(self):
        kp = KeypointCoord(name=Keypoint.NOSE, x=0.5, y=0.3, confidence=0.95)
        assert kp.name == Keypoint.NOSE
        assert kp.x == 0.5
        assert kp.y == 0.3

    def test_boundary_values(self):
        kp = KeypointCoord(name=Keypoint.LEFT_ANKLE, x=0.0, y=1.0, confidence=0.0)
        assert kp.x == 0.0
        assert kp.y == 1.0

    def test_invalid_coordinate_raises(self):
        with pytest.raises(Exception):
            KeypointCoord(name=Keypoint.NOSE, x=1.5, y=0.5)


class TestYogaPose:
    def test_valid_pose(self):
        keypoints = _make_keypoints()
        pose = YogaPose(keypoints=keypoints)
        assert len(pose.keypoints) == 17

    def test_get_keypoint(self):
        keypoints = _make_keypoints()
        pose = YogaPose(keypoints=keypoints)
        nose = pose.get_keypoint(Keypoint.NOSE)
        assert nose.name == Keypoint.NOSE

    def test_get_missing_keypoint_raises(self):
        keypoints = [
            KeypointCoord(name=kp, x=0.5, y=0.5)
            for kp in list(Keypoint)[:16]
        ]
        # This should fail validation (min_length=17)
        with pytest.raises(Exception):
            YogaPose(keypoints=keypoints)

    def test_to_coordinate_array(self):
        keypoints = _make_keypoints()
        pose = YogaPose(keypoints=keypoints)
        coords = pose.to_coordinate_array()
        assert len(coords) == 17
        assert all(isinstance(c, tuple) and len(c) == 2 for c in coords)


class TestAsana:
    def test_create_asana(self):
        asana = Asana(
            sanskrit_name="Tadasana",
            english_name="Mountain Pose",
            description="Stand tall.",
            difficulty=DifficultyLevel.BEGINNER,
            target_joint_angles={"left_knee": 175.0},
            benefits=["Improves posture"],
        )
        assert asana.sanskrit_name == "Tadasana"
        assert asana.difficulty == DifficultyLevel.BEGINNER


class TestPracticeSession:
    def test_add_pose_score(self):
        session = PracticeSession(session_id="test-001")
        score = PoseScore(
            asana_name="Tadasana",
            overall_score=85.0,
            joint_scores={"left_knee": 90.0},
            corrections=[],
        )
        session.add_pose_score(score)
        assert len(session.pose_scores) == 1
        assert session.average_score == 85.0

    def test_running_average(self):
        session = PracticeSession(session_id="test-002")
        session.add_pose_score(PoseScore(
            asana_name="A", overall_score=80.0, joint_scores={}, corrections=[],
        ))
        session.add_pose_score(PoseScore(
            asana_name="B", overall_score=100.0, joint_scores={}, corrections=[],
        ))
        assert session.average_score == pytest.approx(90.0)

    def test_finish(self):
        session = PracticeSession(session_id="test-003")
        session.finish()
        assert session.end_time is not None
