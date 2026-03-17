"""Pydantic data models for Asana-AI."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Keypoint(str, Enum):
    """17 anatomical keypoints detected by the pose model."""

    NOSE = "nose"
    LEFT_EYE = "left_eye"
    RIGHT_EYE = "right_eye"
    LEFT_EAR = "left_ear"
    RIGHT_EAR = "right_ear"
    LEFT_SHOULDER = "left_shoulder"
    RIGHT_SHOULDER = "right_shoulder"
    LEFT_ELBOW = "left_elbow"
    RIGHT_ELBOW = "right_elbow"
    LEFT_WRIST = "left_wrist"
    RIGHT_WRIST = "right_wrist"
    LEFT_HIP = "left_hip"
    RIGHT_HIP = "right_hip"
    LEFT_KNEE = "left_knee"
    RIGHT_KNEE = "right_knee"
    LEFT_ANKLE = "left_ankle"
    RIGHT_ANKLE = "right_ankle"


class KeypointCoord(BaseModel):
    """A single keypoint with 2D coordinates and confidence."""

    name: Keypoint
    x: float = Field(ge=0.0, le=1.0, description="Normalized x coordinate")
    y: float = Field(ge=0.0, le=1.0, description="Normalized y coordinate")
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)


class YogaPose(BaseModel):
    """A detected yoga pose represented by 17 keypoints."""

    keypoints: list[KeypointCoord] = Field(min_length=17, max_length=17)
    timestamp: datetime = Field(default_factory=datetime.now)
    image_path: Optional[str] = None

    def get_keypoint(self, name: Keypoint) -> KeypointCoord:
        """Get a specific keypoint by name."""
        for kp in self.keypoints:
            if kp.name == name:
                return kp
        raise ValueError(f"Keypoint {name} not found")

    def to_coordinate_array(self) -> list[tuple[float, float]]:
        """Return keypoints as a flat list of (x, y) tuples."""
        return [(kp.x, kp.y) for kp in self.keypoints]


class JointAngle(BaseModel):
    """An angle measured at a specific joint."""

    joint_name: str
    angle_degrees: float = Field(ge=0.0, le=360.0)
    keypoints_used: tuple[Keypoint, Keypoint, Keypoint]


class DifficultyLevel(str, Enum):
    """Difficulty level of a yoga asana."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class BreathPhase(str, Enum):
    """Breathing phase."""

    INHALE = "inhale"
    EXHALE = "exhale"
    HOLD = "hold"
    NATURAL = "natural"


class BreathingPattern(BaseModel):
    """A breathing instruction for a pose."""

    phase: BreathPhase
    duration_seconds: float = Field(gt=0)
    instruction: str


class Asana(BaseModel):
    """A reference yoga asana with correct alignment data."""

    sanskrit_name: str
    english_name: str
    description: str
    difficulty: DifficultyLevel
    target_joint_angles: dict[str, float] = Field(
        description="Mapping of joint name to target angle in degrees"
    )
    angle_tolerance: dict[str, float] = Field(
        default_factory=dict,
        description="Per-joint tolerance in degrees; defaults to 15 if absent",
    )
    benefits: list[str]
    contraindications: list[str] = Field(default_factory=list)
    breathing: list[BreathingPattern] = Field(default_factory=list)
    hold_duration_seconds: float = Field(default=30.0, ge=5.0)
    category: str = "standing"


class Severity(str, Enum):
    """Severity of a correction."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class Correction(BaseModel):
    """A single alignment correction for a practitioner."""

    joint_name: str
    current_angle: float
    target_angle: float
    deviation: float
    severity: Severity
    instruction: str
    body_part: str


class PoseScore(BaseModel):
    """Overall score for a pose attempt."""

    asana_name: str
    overall_score: float = Field(ge=0.0, le=100.0)
    joint_scores: dict[str, float]
    corrections: list[Correction]
    timestamp: datetime = Field(default_factory=datetime.now)


class PracticeSession(BaseModel):
    """A complete yoga practice session."""

    session_id: str
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    sequence_name: Optional[str] = None
    pose_scores: list[PoseScore] = Field(default_factory=list)
    total_duration_seconds: float = 0.0
    average_score: float = 0.0
    notes: str = ""

    def add_pose_score(self, score: PoseScore) -> None:
        """Add a scored pose to the session and update the running average."""
        self.pose_scores.append(score)
        total = sum(ps.overall_score for ps in self.pose_scores)
        self.average_score = total / len(self.pose_scores)

    def finish(self) -> None:
        """Mark the session as complete."""
        self.end_time = datetime.now()
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.total_duration_seconds = delta.total_seconds()
