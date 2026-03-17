"""Tests for AsanaLibrary, SequenceBuilder, and PranayamaGuide."""

import pytest

from asana.library.asanas import AsanaLibrary
from asana.library.breathing import PranayamaGuide
from asana.library.sequences import SequenceBuilder
from asana.models import DifficultyLevel


class TestAsanaLibrary:
    def setup_method(self):
        self.library = AsanaLibrary()

    def test_has_at_least_30_asanas(self):
        assert self.library.count >= 30

    def test_get_tadasana(self):
        asana = self.library.get("Tadasana")
        assert asana is not None
        assert asana.english_name == "Mountain Pose"

    def test_get_by_english_name(self):
        asana = self.library.get_by_english("Downward-Facing Dog")
        assert asana is not None
        assert asana.sanskrit_name == "Adho_Mukha_Svanasana"

    def test_get_nonexistent(self):
        assert self.library.get("Nonexistent") is None

    def test_filter_by_difficulty(self):
        beginners = self.library.filter_by_difficulty(DifficultyLevel.BEGINNER)
        assert len(beginners) > 0
        assert all(a.difficulty == DifficultyLevel.BEGINNER for a in beginners)

    def test_filter_by_category(self):
        standing = self.library.filter_by_category("standing")
        assert len(standing) > 0

    def test_search(self):
        results = self.library.search("warrior")
        assert len(results) >= 3  # Warrior I, II, III

    def test_list_all_sorted(self):
        asanas = self.library.list_all()
        names = [a.sanskrit_name for a in asanas]
        assert names == sorted(names)

    def test_all_asanas_have_benefits(self):
        for asana in self.library.list_all():
            assert len(asana.benefits) > 0, f"{asana.sanskrit_name} has no benefits"

    def test_all_asanas_have_target_angles(self):
        for asana in self.library.list_all():
            assert len(asana.target_joint_angles) > 0, (
                f"{asana.sanskrit_name} has no target angles"
            )

    def test_add_custom_asana(self):
        from asana.models import Asana
        custom = Asana(
            sanskrit_name="CustomAsana",
            english_name="Custom Pose",
            description="A custom test pose.",
            difficulty=DifficultyLevel.BEGINNER,
            target_joint_angles={"left_knee": 90.0},
            benefits=["Testing"],
        )
        self.library.add(custom)
        assert self.library.get("CustomAsana") is not None


class TestSequenceBuilder:
    def setup_method(self):
        self.builder = SequenceBuilder()

    def test_sun_salutation_a_exists(self):
        seq = self.builder.get("Surya_Namaskar_A")
        assert seq is not None
        assert len(seq.steps) > 0

    def test_sun_salutation_b_exists(self):
        seq = self.builder.get("Surya_Namaskar_B")
        assert seq is not None

    def test_warrior_series_exists(self):
        seq = self.builder.get("Warrior_Series")
        assert seq is not None

    def test_standing_series_exists(self):
        seq = self.builder.get("Standing_Series")
        assert seq is not None

    def test_sequence_duration_computed(self):
        seq = self.builder.get("Surya_Namaskar_A")
        assert seq is not None
        assert seq.total_duration_minutes > 0

    def test_create_custom_sequence(self):
        seq = self.builder.create_custom(
            name="My_Flow",
            description="A custom flow",
            asana_names=["Tadasana", "Uttanasana"],
            hold_seconds=15.0,
        )
        assert seq.name == "My_Flow"
        assert len(seq.steps) == 2
        assert seq.total_duration_minutes > 0

    def test_resolve_sequence(self):
        seq = self.builder.get("Surya_Namaskar_A")
        assert seq is not None
        resolved = self.builder.resolve_sequence(seq)
        assert len(resolved) == len(seq.steps)


class TestPranayamaGuide:
    def setup_method(self):
        self.guide = PranayamaGuide()

    def test_list_patterns(self):
        patterns = self.guide.list_patterns()
        assert len(patterns) >= 5

    def test_get_for_pose(self):
        pattern = self.guide.get_for_pose("Tadasana")
        assert pattern is not None
        assert len(pattern.phases) > 0

    def test_get_for_unknown_pose(self):
        assert self.guide.get_for_pose("Nonexistent") is None

    def test_breathing_instructions(self):
        instructions = self.guide.get_breathing_instructions("Adho_Mukha_Svanasana")
        assert len(instructions) > 0
        assert all(isinstance(i, str) for i in instructions)

    def test_default_breathing_for_unknown(self):
        instructions = self.guide.get_breathing_instructions("Unknown")
        assert len(instructions) == 1
        assert "naturally" in instructions[0].lower()

    def test_pattern_durations(self):
        for pattern in self.guide.list_patterns():
            assert pattern.cycle_duration > 0
            assert pattern.total_duration > 0
