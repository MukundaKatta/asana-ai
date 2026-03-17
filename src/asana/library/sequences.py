"""SequenceBuilder: Pre-built and custom yoga sequences."""

from __future__ import annotations

from dataclasses import dataclass, field

from asana.library.asanas import AsanaLibrary
from asana.models import Asana


@dataclass
class SequenceStep:
    """A single step in a yoga sequence."""

    asana_name: str
    hold_seconds: float = 30.0
    repetitions: int = 1
    side: str = "both"  # "left", "right", or "both"
    transition_note: str = ""


@dataclass
class YogaSequence:
    """An ordered sequence of yoga poses."""

    name: str
    description: str
    steps: list[SequenceStep] = field(default_factory=list)
    difficulty: str = "beginner"
    total_duration_minutes: float = 0.0

    def compute_duration(self) -> float:
        """Compute total duration in minutes from step hold times."""
        total_seconds = 0.0
        for step in self.steps:
            sides = 2 if step.side == "both" else 1
            total_seconds += step.hold_seconds * step.repetitions * sides
        self.total_duration_minutes = total_seconds / 60.0
        return self.total_duration_minutes


# ---------------------------------------------------------------------------
# Pre-built sequences
# ---------------------------------------------------------------------------

SUN_SALUTATION_A = YogaSequence(
    name="Surya_Namaskar_A",
    description="Sun Salutation A: a flowing warmup sequence linking breath to movement.",
    difficulty="beginner",
    steps=[
        SequenceStep("Tadasana", hold_seconds=5, transition_note="Stand at the front of the mat"),
        SequenceStep("Uttanasana", hold_seconds=5, transition_note="Exhale, fold forward"),
        SequenceStep("Ardha_Uttanasana", hold_seconds=3, transition_note="Inhale, halfway lift"),
        SequenceStep("Chaturanga_Dandasana", hold_seconds=5, transition_note="Exhale, step back and lower"),
        SequenceStep("Urdhva_Mukha_Svanasana", hold_seconds=5, transition_note="Inhale, upward dog"),
        SequenceStep("Adho_Mukha_Svanasana", hold_seconds=25, transition_note="Exhale, downward dog, hold 5 breaths"),
        SequenceStep("Uttanasana", hold_seconds=5, transition_note="Step to front, exhale fold"),
        SequenceStep("Tadasana", hold_seconds=5, transition_note="Inhale, rise to stand"),
    ],
)

SUN_SALUTATION_B = YogaSequence(
    name="Surya_Namaskar_B",
    description="Sun Salutation B: adds Utkatasana and Virabhadrasana I to the flow.",
    difficulty="beginner",
    steps=[
        SequenceStep("Utkatasana", hold_seconds=5, transition_note="Inhale, chair pose"),
        SequenceStep("Uttanasana", hold_seconds=5, transition_note="Exhale, fold forward"),
        SequenceStep("Chaturanga_Dandasana", hold_seconds=5, transition_note="Exhale, lower"),
        SequenceStep("Urdhva_Mukha_Svanasana", hold_seconds=5, transition_note="Inhale, up dog"),
        SequenceStep("Adho_Mukha_Svanasana", hold_seconds=5, transition_note="Exhale, down dog"),
        SequenceStep("Virabhadrasana_I", hold_seconds=5, side="right", transition_note="Right foot forward, warrior I"),
        SequenceStep("Chaturanga_Dandasana", hold_seconds=5, transition_note="Exhale, lower"),
        SequenceStep("Urdhva_Mukha_Svanasana", hold_seconds=5, transition_note="Inhale, up dog"),
        SequenceStep("Adho_Mukha_Svanasana", hold_seconds=5, transition_note="Exhale, down dog"),
        SequenceStep("Virabhadrasana_I", hold_seconds=5, side="left", transition_note="Left foot forward, warrior I"),
        SequenceStep("Chaturanga_Dandasana", hold_seconds=5, transition_note="Exhale, lower"),
        SequenceStep("Urdhva_Mukha_Svanasana", hold_seconds=5, transition_note="Inhale, up dog"),
        SequenceStep("Adho_Mukha_Svanasana", hold_seconds=25, transition_note="Exhale, down dog, hold 5 breaths"),
        SequenceStep("Uttanasana", hold_seconds=5, transition_note="Step forward, fold"),
        SequenceStep("Utkatasana", hold_seconds=5, transition_note="Inhale, chair pose"),
        SequenceStep("Tadasana", hold_seconds=5, transition_note="Exhale, stand tall"),
    ],
)

WARRIOR_SERIES = YogaSequence(
    name="Warrior_Series",
    description="A standing strength sequence through all three Warrior poses.",
    difficulty="intermediate",
    steps=[
        SequenceStep("Tadasana", hold_seconds=10, transition_note="Center yourself"),
        SequenceStep("Virabhadrasana_I", hold_seconds=30, side="right", transition_note="Step right foot forward"),
        SequenceStep("Virabhadrasana_II", hold_seconds=30, side="right", transition_note="Open hips, extend arms"),
        SequenceStep("Virabhadrasana_III", hold_seconds=20, side="right", transition_note="Shift weight, extend back leg"),
        SequenceStep("Tadasana", hold_seconds=10, transition_note="Return to center"),
        SequenceStep("Virabhadrasana_I", hold_seconds=30, side="left", transition_note="Step left foot forward"),
        SequenceStep("Virabhadrasana_II", hold_seconds=30, side="left", transition_note="Open hips, extend arms"),
        SequenceStep("Virabhadrasana_III", hold_seconds=20, side="left", transition_note="Shift weight, extend back leg"),
        SequenceStep("Tadasana", hold_seconds=10, transition_note="Return to center"),
    ],
)

STANDING_SERIES = YogaSequence(
    name="Standing_Series",
    description="A comprehensive standing pose sequence building strength and flexibility.",
    difficulty="intermediate",
    steps=[
        SequenceStep("Tadasana", hold_seconds=10, transition_note="Ground through your feet"),
        SequenceStep("Utkatasana", hold_seconds=20, transition_note="Bend knees, sit back"),
        SequenceStep("Uttanasana", hold_seconds=20, transition_note="Fold forward"),
        SequenceStep("Virabhadrasana_I", hold_seconds=30, side="right"),
        SequenceStep("Virabhadrasana_II", hold_seconds=30, side="right"),
        SequenceStep("Trikonasana", hold_seconds=30, side="right", transition_note="Straighten front leg, extend"),
        SequenceStep("Utthita_Parsvakonasana", hold_seconds=30, side="right"),
        SequenceStep("Ardha_Chandrasana", hold_seconds=20, side="right"),
        SequenceStep("Prasarita_Padottanasana", hold_seconds=30, transition_note="Wide legs, fold forward"),
        SequenceStep("Virabhadrasana_I", hold_seconds=30, side="left"),
        SequenceStep("Virabhadrasana_II", hold_seconds=30, side="left"),
        SequenceStep("Trikonasana", hold_seconds=30, side="left"),
        SequenceStep("Utthita_Parsvakonasana", hold_seconds=30, side="left"),
        SequenceStep("Ardha_Chandrasana", hold_seconds=20, side="left"),
        SequenceStep("Vrksasana", hold_seconds=30, side="right", transition_note="Balance on right leg"),
        SequenceStep("Vrksasana", hold_seconds=30, side="left", transition_note="Balance on left leg"),
        SequenceStep("Tadasana", hold_seconds=10, transition_note="Return to mountain"),
    ],
)

COOL_DOWN_SERIES = YogaSequence(
    name="Cool_Down_Series",
    description="Gentle seated and supine sequence for winding down a practice.",
    difficulty="beginner",
    steps=[
        SequenceStep("Paschimottanasana", hold_seconds=60, transition_note="Seated forward fold"),
        SequenceStep("Janu_Sirsasana", hold_seconds=45, side="right"),
        SequenceStep("Janu_Sirsasana", hold_seconds=45, side="left"),
        SequenceStep("Baddha_Konasana", hold_seconds=60, transition_note="Soles of feet together"),
        SequenceStep("Ardha_Matsyendrasana", hold_seconds=30, side="right"),
        SequenceStep("Ardha_Matsyendrasana", hold_seconds=30, side="left"),
        SequenceStep("Supta_Baddha_Konasana", hold_seconds=120, transition_note="Recline"),
        SequenceStep("Savasana", hold_seconds=300, transition_note="Final relaxation"),
    ],
)


class SequenceBuilder:
    """Build and manage yoga sequences.

    Provides access to pre-built sequences and a builder API for
    constructing custom sequences from the asana library.
    """

    def __init__(self, library: AsanaLibrary | None = None) -> None:
        self.library = library or AsanaLibrary()
        self._sequences: dict[str, YogaSequence] = {}
        self._load_defaults()

    def _load_defaults(self) -> None:
        """Register all built-in sequences."""
        for seq in [
            SUN_SALUTATION_A,
            SUN_SALUTATION_B,
            WARRIOR_SERIES,
            STANDING_SERIES,
            COOL_DOWN_SERIES,
        ]:
            seq.compute_duration()
            self._sequences[seq.name] = seq

    def get(self, name: str) -> YogaSequence | None:
        """Get a sequence by name."""
        return self._sequences.get(name)

    def list_all(self) -> list[YogaSequence]:
        """List all available sequences."""
        return list(self._sequences.values())

    def resolve_sequence(self, sequence: YogaSequence) -> list[tuple[SequenceStep, Asana | None]]:
        """Resolve a sequence into (step, asana) pairs using the library.

        Returns a list of tuples where the Asana may be None if the
        pose is not found in the library (e.g. transitional poses).
        """
        result: list[tuple[SequenceStep, Asana | None]] = []
        for step in sequence.steps:
            asana = self.library.get(step.asana_name)
            result.append((step, asana))
        return result

    def create_custom(
        self,
        name: str,
        description: str,
        asana_names: list[str],
        hold_seconds: float = 30.0,
    ) -> YogaSequence:
        """Create a custom sequence from a list of asana names.

        Args:
            name: Name for the sequence.
            description: Description text.
            asana_names: List of Sanskrit names of asanas to include.
            hold_seconds: Default hold time per pose.

        Returns:
            A new YogaSequence registered in this builder.
        """
        steps = [
            SequenceStep(asana_name=aname, hold_seconds=hold_seconds)
            for aname in asana_names
        ]
        seq = YogaSequence(name=name, description=description, steps=steps)
        seq.compute_duration()
        self._sequences[name] = seq
        return seq
