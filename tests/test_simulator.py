"""Tests for PoseSimulator."""

import pytest

from asana.library.asanas import AsanaLibrary
from asana.simulator import PoseSimulator


class TestPoseSimulator:
    def setup_method(self):
        self.simulator = PoseSimulator(seed=42)
        self.library = AsanaLibrary()

    def test_generate_pose(self):
        pose = self.simulator.generate_pose()
        assert len(pose.keypoints) == 17
        for kp in pose.keypoints:
            assert 0.0 <= kp.x <= 1.0
            assert 0.0 <= kp.y <= 1.0

    def test_generate_pose_with_asana(self):
        asana = self.library.get("Tadasana")
        pose = self.simulator.generate_pose(asana=asana, noise_std=0.01)
        assert len(pose.keypoints) == 17

    def test_zero_noise(self):
        pose = self.simulator.generate_pose(noise_std=0.0)
        for kp in pose.keypoints:
            assert kp.confidence == 1.0

    def test_deterministic_with_seed(self):
        sim1 = PoseSimulator(seed=123)
        sim2 = PoseSimulator(seed=123)
        pose1 = sim1.generate_pose(noise_std=0.05)
        pose2 = sim2.generate_pose(noise_std=0.05)
        for k1, k2 in zip(pose1.keypoints, pose2.keypoints):
            assert k1.x == pytest.approx(k2.x)
            assert k1.y == pytest.approx(k2.y)

    def test_simulate_session(self):
        session = self.simulator.simulate_session(
            asana_names=["Tadasana", "Virabhadrasana_I"],
            noise_std=0.02,
            library=self.library,
        )
        assert len(session.pose_scores) == 2
        assert session.average_score > 0
        assert session.end_time is not None

    def test_simulate_session_skips_unknown(self):
        session = self.simulator.simulate_session(
            asana_names=["Tadasana", "UnknownPose"],
            noise_std=0.02,
            library=self.library,
        )
        assert len(session.pose_scores) == 1
