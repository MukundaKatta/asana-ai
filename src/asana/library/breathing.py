"""PranayamaGuide: Breathing patterns and instructions for yoga poses."""

from __future__ import annotations

from dataclasses import dataclass, field

from asana.models import BreathingPattern, BreathPhase


@dataclass
class PranayamaPattern:
    """A complete pranayama (breathing) pattern for a pose or standalone practice."""

    name: str
    sanskrit_name: str
    description: str
    phases: list[BreathingPattern]
    cycles: int = 5
    benefits: list[str] = field(default_factory=list)

    @property
    def cycle_duration(self) -> float:
        """Total duration of one breathing cycle in seconds."""
        return sum(p.duration_seconds for p in self.phases)

    @property
    def total_duration(self) -> float:
        """Total duration of all cycles in seconds."""
        return self.cycle_duration * self.cycles


def _bp(phase: BreathPhase, duration: float, instruction: str) -> BreathingPattern:
    return BreathingPattern(phase=phase, duration_seconds=duration, instruction=instruction)


# ---------------------------------------------------------------------------
# Pranayama patterns
# ---------------------------------------------------------------------------

UJJAYI = PranayamaPattern(
    name="Ujjayi Breath",
    sanskrit_name="Ujjayi_Pranayama",
    description="Victorious breath with slight throat constriction producing an oceanic sound.",
    phases=[
        _bp(BreathPhase.INHALE, 4.0, "Inhale through the nose, slightly constricting the glottis to create an ocean sound"),
        _bp(BreathPhase.EXHALE, 4.0, "Exhale through the nose with the same gentle constriction"),
    ],
    cycles=10,
    benefits=["Calms the mind", "Warms the body", "Improves concentration",
              "Regulates blood pressure"],
)

NADI_SHODHANA = PranayamaPattern(
    name="Alternate Nostril Breathing",
    sanskrit_name="Nadi_Shodhana",
    description="Alternating breath through left and right nostrils to balance energy channels.",
    phases=[
        _bp(BreathPhase.INHALE, 4.0, "Close right nostril, inhale through left"),
        _bp(BreathPhase.HOLD, 2.0, "Close both nostrils, retain the breath"),
        _bp(BreathPhase.EXHALE, 4.0, "Close left nostril, exhale through right"),
        _bp(BreathPhase.INHALE, 4.0, "Keep left closed, inhale through right"),
        _bp(BreathPhase.HOLD, 2.0, "Close both nostrils, retain the breath"),
        _bp(BreathPhase.EXHALE, 4.0, "Close right nostril, exhale through left"),
    ],
    cycles=5,
    benefits=["Balances left and right brain hemispheres", "Calms the nervous system",
              "Purifies energy channels", "Reduces anxiety"],
)

KAPALABHATI = PranayamaPattern(
    name="Skull Shining Breath",
    sanskrit_name="Kapalabhati",
    description="Rapid, forceful exhalations with passive inhalations to energize and cleanse.",
    phases=[
        _bp(BreathPhase.EXHALE, 0.5, "Sharply exhale through the nose, pulling the navel in"),
        _bp(BreathPhase.INHALE, 0.5, "Allow the inhale to happen passively as the belly releases"),
    ],
    cycles=30,
    benefits=["Energizes the body", "Clears the nasal passages",
              "Strengthens abdominal muscles", "Improves digestion"],
)

BHRAMARI = PranayamaPattern(
    name="Bee Breath",
    sanskrit_name="Bhramari_Pranayama",
    description="Humming exhalation to calm the mind and reduce agitation.",
    phases=[
        _bp(BreathPhase.INHALE, 4.0, "Inhale deeply through the nose"),
        _bp(BreathPhase.EXHALE, 8.0, "Exhale slowly while making a humming sound like a bee"),
    ],
    cycles=7,
    benefits=["Reduces anger and anxiety", "Improves concentration",
              "Lowers blood pressure", "Beneficial for throat ailments"],
)

DIRGA = PranayamaPattern(
    name="Three-Part Breath",
    sanskrit_name="Dirga_Pranayama",
    description="Complete yogic breath filling belly, ribs, and chest sequentially.",
    phases=[
        _bp(BreathPhase.INHALE, 3.0, "Inhale into the belly, feeling it expand"),
        _bp(BreathPhase.INHALE, 3.0, "Continue inhaling into the ribcage, feeling ribs widen"),
        _bp(BreathPhase.INHALE, 3.0, "Fill the upper chest, feeling collarbones lift"),
        _bp(BreathPhase.EXHALE, 9.0, "Exhale slowly from top to bottom, emptying completely"),
    ],
    cycles=5,
    benefits=["Maximizes oxygen intake", "Calms the mind",
              "Releases muscular tension", "Grounds awareness in the body"],
)

SAMA_VRITTI = PranayamaPattern(
    name="Equal Breathing",
    sanskrit_name="Sama_Vritti",
    description="Equal-duration inhales and exhales for balance and calm.",
    phases=[
        _bp(BreathPhase.INHALE, 4.0, "Inhale for a count of four"),
        _bp(BreathPhase.EXHALE, 4.0, "Exhale for a count of four"),
    ],
    cycles=10,
    benefits=["Reduces stress", "Improves focus",
              "Balances the nervous system", "Easy for beginners"],
)

VILOMA = PranayamaPattern(
    name="Interrupted Breathing",
    sanskrit_name="Viloma_Pranayama",
    description="Breath is paused at intervals during inhale or exhale.",
    phases=[
        _bp(BreathPhase.INHALE, 2.0, "Inhale one-third"),
        _bp(BreathPhase.HOLD, 2.0, "Pause"),
        _bp(BreathPhase.INHALE, 2.0, "Inhale two-thirds"),
        _bp(BreathPhase.HOLD, 2.0, "Pause"),
        _bp(BreathPhase.INHALE, 2.0, "Complete the inhale"),
        _bp(BreathPhase.EXHALE, 6.0, "Exhale smoothly and completely"),
    ],
    cycles=5,
    benefits=["Increases lung capacity", "Improves breath control",
              "Calms the mind", "Prepares for deeper pranayama"],
)

SITALI = PranayamaPattern(
    name="Cooling Breath",
    sanskrit_name="Sitali_Pranayama",
    description="Inhale through a curled tongue to cool the body.",
    phases=[
        _bp(BreathPhase.INHALE, 4.0, "Curl the tongue, inhale through it as if sipping cool air"),
        _bp(BreathPhase.EXHALE, 6.0, "Close the mouth, exhale slowly through the nose"),
    ],
    cycles=10,
    benefits=["Cools the body", "Reduces pitta (heat)",
              "Calms hunger and thirst", "Soothes inflammatory conditions"],
)


# ---------------------------------------------------------------------------
# Pose-specific breathing recommendations
# ---------------------------------------------------------------------------

POSE_BREATHING: dict[str, PranayamaPattern] = {
    "Tadasana": SAMA_VRITTI,
    "Virabhadrasana_I": UJJAYI,
    "Virabhadrasana_II": UJJAYI,
    "Virabhadrasana_III": UJJAYI,
    "Trikonasana": UJJAYI,
    "Utthita_Parsvakonasana": UJJAYI,
    "Vrksasana": SAMA_VRITTI,
    "Utkatasana": UJJAYI,
    "Garudasana": SAMA_VRITTI,
    "Natarajasana": UJJAYI,
    "Adho_Mukha_Svanasana": DIRGA,
    "Uttanasana": DIRGA,
    "Paschimottanasana": DIRGA,
    "Janu_Sirsasana": DIRGA,
    "Bhujangasana": UJJAYI,
    "Urdhva_Mukha_Svanasana": UJJAYI,
    "Ustrasana": UJJAYI,
    "Dhanurasana": UJJAYI,
    "Setu_Bandhasana": UJJAYI,
    "Padmasana": NADI_SHODHANA,
    "Baddha_Konasana": DIRGA,
    "Ardha_Matsyendrasana": UJJAYI,
    "Navasana": UJJAYI,
    "Savasana": DIRGA,
    "Supta_Baddha_Konasana": DIRGA,
    "Halasana": UJJAYI,
    "Chaturanga_Dandasana": UJJAYI,
    "Bakasana": UJJAYI,
    "Sirsasana": SAMA_VRITTI,
    "Sarvangasana": UJJAYI,
}


class PranayamaGuide:
    """Guide for breathing practices, both standalone and pose-specific.

    Provides recommended pranayama patterns for each asana and
    standalone breathing exercises.
    """

    def __init__(self) -> None:
        self._patterns: dict[str, PranayamaPattern] = {
            p.sanskrit_name: p
            for p in [
                UJJAYI, NADI_SHODHANA, KAPALABHATI, BHRAMARI,
                DIRGA, SAMA_VRITTI, VILOMA, SITALI,
            ]
        }
        self._pose_map = POSE_BREATHING

    def get_for_pose(self, asana_sanskrit_name: str) -> PranayamaPattern | None:
        """Get the recommended breathing pattern for a specific pose."""
        return self._pose_map.get(asana_sanskrit_name)

    def get_pattern(self, sanskrit_name: str) -> PranayamaPattern | None:
        """Get a standalone pranayama pattern by Sanskrit name."""
        return self._patterns.get(sanskrit_name)

    def list_patterns(self) -> list[PranayamaPattern]:
        """List all available pranayama patterns."""
        return list(self._patterns.values())

    def get_breathing_instructions(self, asana_name: str) -> list[str]:
        """Get a list of step-by-step breathing instructions for a pose.

        Args:
            asana_name: The Sanskrit name of the asana.

        Returns:
            List of instruction strings, one per breath phase.
        """
        pattern = self.get_for_pose(asana_name)
        if pattern is None:
            return ["Breathe naturally and steadily through the nose."]

        instructions = []
        for i, phase in enumerate(pattern.phases, 1):
            instructions.append(
                f"Step {i}: {phase.instruction} ({phase.duration_seconds:.0f}s)"
            )
        return instructions
