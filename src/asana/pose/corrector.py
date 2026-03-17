"""AsanaCorrector: Generate specific alignment corrections for yoga poses."""

from __future__ import annotations

from asana.models import Asana, Correction, PoseScore, Severity, YogaPose
from asana.pose.analyzer import AsanaAnalyzer


# Mapping from joint names to human-readable body part descriptions
JOINT_BODY_PARTS: dict[str, str] = {
    "left_elbow": "left arm",
    "right_elbow": "right arm",
    "left_shoulder": "left shoulder",
    "right_shoulder": "right shoulder",
    "left_hip": "left hip",
    "right_hip": "right hip",
    "left_knee": "left leg",
    "right_knee": "right leg",
    "neck": "head and neck",
    "torso_left": "left side of torso",
    "torso_right": "right side of torso",
    "left_armpit": "left arm relative to torso",
    "right_armpit": "right arm relative to torso",
}

# Correction instruction templates keyed by (joint_category, direction)
CORRECTION_TEMPLATES: dict[tuple[str, str], str] = {
    ("elbow", "extend"): "Straighten your {side} arm more; extend through the elbow.",
    ("elbow", "bend"): "Bend your {side} elbow more; bring your forearm closer.",
    ("shoulder", "raise"): "Raise your {side} arm higher; lift from the shoulder joint.",
    ("shoulder", "lower"): "Lower your {side} arm; relax the shoulder down and back.",
    ("hip", "open"): "Open your {side} hip more; externally rotate the thigh.",
    ("hip", "close"): "Tuck your {side} hip in; engage the core to square the hips.",
    ("knee", "extend"): "Straighten your {side} leg; press through the heel.",
    ("knee", "bend"): (
        "Bend your {side} knee more deeply; aim for a 90-degree angle "
        "with the knee over the ankle."
    ),
    ("neck", "align"): (
        "Align your head with your spine; gaze forward and lengthen "
        "the back of the neck."
    ),
    ("torso", "extend"): "Lengthen your {side} torso; create space between ribs and hip.",
    ("torso", "engage"): (
        "Engage your core to stabilize the {side} side of your torso."
    ),
    ("armpit", "open"): (
        "Lift your {side} arm further from your body; create space in the armpit."
    ),
    ("armpit", "close"): (
        "Bring your {side} arm closer to your side body."
    ),
}


class AsanaCorrector:
    """Generate specific, actionable alignment corrections.

    Given a detected pose and the reference asana, the corrector identifies
    joints that deviate beyond tolerance and produces natural-language
    instructions for each correction, prioritized by severity.
    """

    SEVERITY_THRESHOLDS = {
        "info": 5.0,       # > tolerance but <= tolerance + 5
        "warning": 15.0,   # > tolerance + 5 but <= tolerance + 15
        "critical": 15.0,  # > tolerance + 15
    }

    def __init__(self) -> None:
        self.analyzer = AsanaAnalyzer()

    def _classify_severity(self, deviation: float, tolerance: float) -> Severity:
        """Classify the severity of a deviation."""
        excess = deviation - tolerance
        if excess <= 0:
            return Severity.INFO
        if excess <= self.SEVERITY_THRESHOLDS["info"]:
            return Severity.INFO
        if excess <= self.SEVERITY_THRESHOLDS["warning"]:
            return Severity.WARNING
        return Severity.CRITICAL

    def _get_joint_category(self, joint_name: str) -> str:
        """Extract the category from a joint name (e.g., 'left_elbow' -> 'elbow')."""
        parts = joint_name.split("_")
        if len(parts) >= 2 and parts[0] in ("left", "right"):
            return "_".join(parts[1:])
        return joint_name

    def _get_side(self, joint_name: str) -> str:
        """Extract the side from a joint name."""
        if joint_name.startswith("left"):
            return "left"
        if joint_name.startswith("right"):
            return "right"
        return ""

    def _generate_instruction(
        self,
        joint_name: str,
        measured: float,
        target: float,
    ) -> str:
        """Generate a natural-language correction instruction."""
        category = self._get_joint_category(joint_name)
        side = self._get_side(joint_name)
        direction = "extend" if measured < target else "bend"

        # Map specific categories to template keys
        if category in ("elbow",):
            direction = "extend" if measured < target else "bend"
        elif category in ("shoulder",):
            direction = "raise" if measured < target else "lower"
        elif category in ("hip",):
            direction = "open" if measured < target else "close"
        elif category in ("knee",):
            direction = "extend" if measured < target else "bend"
        elif category == "neck":
            direction = "align"
        elif category in ("torso_left", "torso_right", "torso"):
            category = "torso"
            direction = "extend" if measured < target else "engage"
        elif category in ("armpit",):
            direction = "open" if measured < target else "close"

        template = CORRECTION_TEMPLATES.get(
            (category, direction),
            f"Adjust your {joint_name.replace('_', ' ')}; "
            f"current angle is {{measured:.0f}} degrees, "
            f"target is {{target:.0f}} degrees.",
        )

        instruction = template.format(
            side=side, measured=measured, target=target
        )
        return instruction

    def generate_corrections(
        self, pose: YogaPose, asana: Asana
    ) -> list[Correction]:
        """Generate alignment corrections for each misaligned joint.

        Args:
            pose: The detected yoga pose.
            asana: The reference asana with target angles.

        Returns:
            List of Correction objects sorted by severity (critical first).
        """
        measured_angles = self.analyzer.compute_joint_angles(pose)
        angle_map = {ja.joint_name: ja.angle_degrees for ja in measured_angles}

        corrections: list[Correction] = []

        for joint_name, target_angle in asana.target_joint_angles.items():
            if joint_name not in angle_map:
                continue

            measured = angle_map[joint_name]
            tolerance = asana.angle_tolerance.get(
                joint_name, self.analyzer.DEFAULT_TOLERANCE_DEGREES
            )
            deviation = abs(measured - target_angle)

            if deviation <= tolerance:
                continue

            severity = self._classify_severity(deviation, tolerance)
            instruction = self._generate_instruction(joint_name, measured, target_angle)
            body_part = JOINT_BODY_PARTS.get(joint_name, joint_name.replace("_", " "))

            corrections.append(
                Correction(
                    joint_name=joint_name,
                    current_angle=measured,
                    target_angle=target_angle,
                    deviation=deviation,
                    severity=severity,
                    instruction=instruction,
                    body_part=body_part,
                )
            )

        # Sort by severity: critical first, then warning, then info
        severity_order = {Severity.CRITICAL: 0, Severity.WARNING: 1, Severity.INFO: 2}
        corrections.sort(key=lambda c: (severity_order[c.severity], -c.deviation))

        return corrections

    def correct_pose(self, pose: YogaPose, asana: Asana) -> PoseScore:
        """Analyze a pose and generate corrections, returning a full PoseScore.

        This combines the analyzer's scoring with the corrector's instructions.

        Args:
            pose: The detected yoga pose.
            asana: The reference asana.

        Returns:
            PoseScore with joint scores and correction instructions.
        """
        score = self.analyzer.analyze(pose, asana)
        corrections = self.generate_corrections(pose, asana)
        score.corrections = corrections
        return score
