"""CLI interface for Asana-AI using Click and Rich."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from asana.library.asanas import AsanaLibrary
from asana.library.breathing import PranayamaGuide
from asana.library.sequences import SequenceBuilder
from asana.report import SessionReport
from asana.simulator import PoseSimulator

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="asana-ai")
def main() -> None:
    """Asana-AI: AI Yoga Pose Corrector.

    Detect, analyze, and correct yoga poses using deep learning.
    """


@main.command()
@click.option("--image", type=click.Path(exists=False), help="Path to a pose image.")
@click.option("--asana", type=str, default=None, help="Sanskrit name of the target asana.")
def analyze(image: str | None, asana: str | None) -> None:
    """Analyze a yoga pose from an image or simulation."""
    library = AsanaLibrary()
    simulator = PoseSimulator(seed=42)
    report = SessionReport(console)

    if asana:
        ref = library.get(asana)
        if ref is None:
            console.print(f"[red]Asana '{asana}' not found in library.[/red]")
            return
    else:
        ref = library.get("Tadasana")
        assert ref is not None

    console.print(f"[bold]Analyzing pose: {ref.english_name} ({ref.sanskrit_name})[/bold]")
    console.print()

    from asana.pose.corrector import AsanaCorrector

    corrector = AsanaCorrector()
    pose = simulator.generate_pose(asana=ref, noise_std=0.03)
    score = corrector.correct_pose(pose, ref)
    report.print_pose_score(score)


@main.command()
@click.option("--name", type=str, required=True, help="Name of the sequence.")
def sequence(name: str) -> None:
    """Start a guided yoga sequence."""
    builder = SequenceBuilder()
    guide = PranayamaGuide()

    seq = builder.get(name)
    if seq is None:
        console.print(f"[red]Sequence '{name}' not found.[/red]")
        console.print("[bold]Available sequences:[/bold]")
        for s in builder.list_all():
            console.print(f"  - {s.name}: {s.description}")
        return

    console.print(f"[bold]{seq.name}[/bold]: {seq.description}")
    console.print(f"Duration: ~{seq.total_duration_minutes:.1f} minutes\n")

    table = Table(title="Sequence Steps", show_header=True)
    table.add_column("#", justify="right", width=4)
    table.add_column("Asana", style="cyan")
    table.add_column("Hold", justify="right")
    table.add_column("Side")
    table.add_column("Breathing")
    table.add_column("Transition")

    for i, step in enumerate(seq.steps, 1):
        breathing = guide.get_for_pose(step.asana_name)
        breath_name = breathing.name if breathing else "Natural"
        table.add_row(
            str(i),
            step.asana_name.replace("_", " "),
            f"{step.hold_seconds:.0f}s",
            step.side,
            breath_name,
            step.transition_note,
        )

    console.print(table)


@main.command()
@click.option("--asana", type=str, default="Tadasana", help="Asana to simulate.")
@click.option("--duration", type=int, default=30, help="Hold duration in seconds.")
@click.option("--noise", type=float, default=0.03, help="Noise level (0-0.1).")
def simulate(asana: str, duration: int, noise: float) -> None:
    """Simulate a practice session with synthetic poses."""
    library = AsanaLibrary()
    simulator = PoseSimulator(seed=42)
    report = SessionReport(console)

    ref = library.get(asana)
    if ref is None:
        console.print(f"[red]Asana '{asana}' not found.[/red]")
        return

    console.print(f"[bold]Simulating {ref.english_name} practice...[/bold]\n")

    session = simulator.simulate_session(
        asana_names=[asana],
        noise_std=noise,
        library=library,
    )
    report.print_session_summary(session)


@main.command(name="list")
@click.option("--difficulty", type=str, default=None, help="Filter by difficulty level.")
@click.option("--category", type=str, default=None, help="Filter by category.")
def list_asanas(difficulty: str | None, category: str | None) -> None:
    """List all available asanas."""
    library = AsanaLibrary()

    asanas = library.list_all()
    if difficulty:
        from asana.models import DifficultyLevel
        try:
            level = DifficultyLevel(difficulty.lower())
            asanas = [a for a in asanas if a.difficulty == level]
        except ValueError:
            console.print(f"[red]Invalid difficulty: {difficulty}[/red]")
            return

    if category:
        asanas = [a for a in asanas if a.category == category]

    table = Table(title=f"Asana Library ({len(asanas)} poses)", show_header=True)
    table.add_column("Sanskrit Name", style="cyan")
    table.add_column("English Name")
    table.add_column("Difficulty", justify="center")
    table.add_column("Category")
    table.add_column("Benefits")

    for a in asanas:
        table.add_row(
            a.sanskrit_name,
            a.english_name,
            a.difficulty.value,
            a.category,
            "; ".join(a.benefits[:2]),
        )

    console.print(table)


@main.command()
@click.option("--session", type=str, default="demo", help="Session ID or 'demo'.")
def report(session: str) -> None:
    """Generate a practice report."""
    simulator = PoseSimulator(seed=42)
    library = AsanaLibrary()
    reporter = SessionReport(console)

    console.print("[bold]Generating demo practice report...[/bold]\n")

    demo_asanas = [
        "Tadasana", "Virabhadrasana_I", "Virabhadrasana_II",
        "Trikonasana", "Adho_Mukha_Svanasana",
    ]

    practice = simulator.simulate_session(
        asana_names=demo_asanas,
        noise_std=0.03,
        library=library,
    )
    practice.sequence_name = "Demo Standing Flow"

    reporter.print_session_summary(practice)


if __name__ == "__main__":
    main()
