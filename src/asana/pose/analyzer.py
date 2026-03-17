"""AsanaAnalyzer: Compare detected poses to reference asanas using joint angles."""

from __future__ import annotations

import math

import numpy as np

from asana.models import (
    Asana,
    JointAngle,
    Keypoint,
    KeypointCoord,
    PoseScore,
    YogaPose,
)


# Joint definitions: each joint is defined by three keypoints (A, B, C)
# where B is the vertex and the angle is measured as angle(A-B-C).
JOINT_DEFINITIONS: dict[str, tuple[Keypoint, Keypoint, Keypoint]] = {
    "left_elbow": (Keypoint.LEFT_SHOULDER, Keypoint.LEFT_ELBOW, Keypoint.LEFT_WRIST),
    "right_elbow": (
        Keypoint.RIGHT_SHOULDER,
        Keypoint.RIGHT_ELBOW,
        Keypoint.RIGHT_WRIST,
    ),
    "left_shoulder": (Keypoint.LEFT_HIP, Keypoint.LEFT_SHOULDER, Keypoint.LEFT_ELBOW),
    "right_shoulder": (
        Keypoint.RIGHT_HIP,
        Keypoint.RIGHT_SHOULDER,
        Keypoint.RIGHT_ELBOW,
    ),
    "left_hip": (Keypoint.LEFT_SHOULDER, Keypoint.LEFT_HIP, Keypoint.LEFT_KNEE),
    "right_hip": (Keypoint.RIGHT_SHOULDER, Keypoint.RIGHT_HIP, Keypoint.RIGHT_KNEE),
    "left_knee": (Keypoint.LEFT_HIP, Keypoint.LEFT_KNEE, Keypoint.LEFT_ANKLE),
    "right_knee": (Keypoint.RIGHT_HIP, Keypoint.RIGHT_KNEE, Keypoint.RIGHT_ANKLE),
    "neck": (Keypoint.LEFT_SHOULDER, Keypoint.NOSE, Keypoint.RIGHT_SHOULDER),
    "torso_left": (Keypoint.LEFT_SHOULDER, Keypoint.LEFT_HIP, Keypoint.LEFT_KNEE),
    "torso_right": (
        Keypoint.RIGHT_SHOULDER,
        Keypoint.RIGHT_HIP,
        Keypoint.RIGHT_KNEE,
    ),
    "left_armpit": (Keypoint.LEFT_ELBOW, Keypoint.LEFT_SHOULDER, Keypoint.LEFT_HIP),
    "right_armpit": (
        Keypoint.RIGHT_ELBOW,
        Keypoint.RIGHT_SHOULDER,
        Keypoint.RIGHT_HIP,
    ),
}


class AsanaAnalyzer:
    """Analyze a detected yoga pose by computing joint angles and comparing
    them against a reference asana's target alignment.

    The analyzer computes the angle at each joint defined in JOINT_DEFINITIONS,
    then scores each joint based on how close it is to the reference angle
    within the allowed tolerance.
    """

    DEFAULT_TOLERANCE_DEGREES: float = 15.0

    def __init__(self) -> None:
        self.joint_definitions = JOINT_DEFINITIONS

    @staticmethod
    def compute_angle(
        point_a: tuple[float, float],
        point_b: tuple[float, float],
        point_c: tuple[float, float],
    ) -> float:
        """Compute the angle at point B formed by rays BA and BC.

        Uses the dot product formula:
            angle = arccos( (BA . BC) / (|BA| * |BC|) )

        Args:
            point_a: (x, y) coordinates of point A.
            point_b: (x, y) coordinates of point B (vertex).
            point_c: (x, y) coordinates of point C.

        Returns:
            Angle in degrees, range [0, 180].
        """
        ba = np.array([point_a[0] - point_b[0], point_a[1] - point_b[1]])
        bc = np.array([point_c[0] - point_b[0], point_c[1] - point_b[1]])

        mag_ba = np.linalg.norm(ba)
        mag_bc = np.linalg.norm(bc)

        if mag_ba < 1e-8 or mag_bc < 1e-8:
            return 0.0

        cos_angle = np.dot(ba, bc) / (mag_ba * mag_bc)
        cos_angle = float(np.clip(cos_angle, -1.0, 1.0))

        return math.degrees(math.acos(cos_angle))

    def compute_joint_angles(self, pose: YogaPose) -> list[JointAngle]:
        """Compute angles at all defined joints for a detected pose.

        Args:
            pose: The detected YogaPose with 17 keypoints.

        Returns:
            List of JointAngle objects for every joint in JOINT_DEFINITIONS.
        """
        angles: list[JointAngle] = []

        for joint_name, (kp_a, kp_b, kp_c) in self.joint_definitions.items():
            a = pose.get_keypoint(kp_a)
            b = pose.get_keypoint(kp_b)
            c = pose.get_keypoint(kp_c)

            angle = self.compute_angle((a.x, a.y), (b.x, b.y), (c.x, c.y))

            angles.append(
                JointAngle(
                    joint_name=joint_name,
                    angle_degrees=angle,
                    keypoints_used=(kp_a, kp_b, kp_c),
                )
            )

        return angles

    def score_joint(
        self,
        measured_angle: float,
        target_angle: float,
        tolerance: float,
    ) -> float:
        """Score a single joint alignment on a 0-100 scale.

        Returns 100 if within tolerance, linearly decreasing beyond that,
        down to a minimum of 0.

        Args:
            measured_angle: The measured angle in degrees.
            target_angle: The target angle in degrees.
            tolerance: Acceptable deviation in degrees.

        Returns:
            Score between 0 and 100.
        """
        deviation = abs(measured_angle - target_angle)
        if deviation <= tolerance:
            return 100.0
        # Linear falloff: lose 2 points per degree beyond tolerance
        penalty = (deviation - tolerance) * 2.0
        return max(0.0, 100.0 - penalty)

    def analyze(self, pose: YogaPose, asana: Asana) -> PoseScore:
        """Compare a detected pose against a reference asana.

        Args:
            pose: The detected YogaPose.
            asana: The reference Asana with target joint angles.

        Returns:
            A PoseScore with per-joint scores and overall score.
        """
        measured_angles = self.compute_joint_angles(pose)
        angle_map = {ja.joint_name: ja.angle_degrees for ja in measured_angles}

        joint_scores: dict[str, float] = {}
        total_score = 0.0
        scored_count = 0

        for joint_name, target_angle in asana.target_joint_angles.items():
            if joint_name not in angle_map:
                continue

            tolerance = asana.angle_tolerance.get(
                joint_name, self.DEFAULT_TOLERANCE_DEGREES
            )
            measured = angle_map[joint_name]
            score = self.score_joint(measured, target_angle, tolerance)

            joint_scores[joint_name] = score
            total_score += score
            scored_count += 1

        overall = total_score / scored_count if scored_count > 0 else 0.0

        return PoseScore(
            asana_name=asana.sanskrit_name,
            overall_score=overall,
            joint_scores=joint_scores,
            corrections=[],  # Corrections are generated by AsanaCorrector
        )

    def identify_asana(
        self, pose: YogaPose, candidates: list[Asana], threshold: float = 60.0
    ) -> list[tuple[Asana, float]]:
        """Identify which asana a pose most closely matches.

        Args:
            pose: The detected pose.
            candidates: List of candidate asanas to compare against.
            threshold: Minimum score to include in results.

        Returns:
            List of (Asana, score) tuples sorted by score descending,
            filtered to those above the threshold.
        """
        results: list[tuple[Asana, float]] = []

        for asana in candidates:
            score = self.analyze(pose, asana)
            if score.overall_score >= threshold:
                results.append((asana, score.overall_score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results
