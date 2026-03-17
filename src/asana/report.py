"""Report: Generate practice session reports with Rich formatting."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from asana.models import PoseScore, PracticeSession, Severity


class SessionReport:
    """Generate formatted reports for yoga practice sessions."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    def _score_color(self, score: float) -> str:
        """Return a color name based on score value."""
        if score >= 90:
            return "green"
        if score >= 70:
            return "yellow"
        if score >= 50:
            return "dark_orange"
        return "red"

    def _severity_color(self, severity: Severity) -> str:
        """Return a color name for correction severity."""
        return {
            Severity.INFO: "blue",
            Severity.WARNING: "yellow",
            Severity.CRITICAL: "red",
        }[severity]

    def print_pose_score(self, score: PoseScore) -> None:
        """Print a single pose score with joint details and corrections."""
        color = self._score_color(score.overall_score)
        title = f"{score.asana_name} - Score: {score.overall_score:.1f}/100"
        panel_style = color

        # Joint scores table
        table = Table(title="Joint Alignment Scores", show_header=True)
        table.add_column("Joint", style="cyan")
        table.add_column("Score", justify="right")
        table.add_column("Status", justify="center")

        for joint, jscore in sorted(score.joint_scores.items()):
            jcolor = self._score_color(jscore)
            status = "OK" if jscore >= 85 else "Adjust"
            table.add_row(
                joint.replace("_", " ").title(),
                f"[{jcolor}]{jscore:.1f}[/{jcolor}]",
                f"[{jcolor}]{status}[/{jcolor}]",
            )

        self.console.print(Panel(table, title=title, border_style=panel_style))

        # Corrections
        if score.corrections:
            corrections_table = Table(title="Corrections", show_header=True)
            corrections_table.add_column("Priority", justify="center", width=10)
            corrections_table.add_column("Body Part", style="cyan")
            corrections_table.add_column("Instruction")
            corrections_table.add_column("Deviation", justify="right")

            for correction in score.corrections:
                sev_color = self._severity_color(correction.severity)
                corrections_table.add_row(
                    f"[{sev_color}]{correction.severity.value.upper()}[/{sev_color}]",
                    correction.body_part.title(),
                    correction.instruction,
                    f"{correction.deviation:.1f} deg",
                )

            self.console.print(corrections_table)
        else:
            self.console.print("[green]Perfect alignment! No corrections needed.[/green]")
        self.console.print()

    def print_session_summary(self, session: PracticeSession) -> None:
        """Print a complete session summary."""
        self.console.print()
        self.console.rule("[bold]Practice Session Report[/bold]")
        self.console.print()

        # Session info
        info_table = Table(show_header=False, box=None)
        info_table.add_column("Key", style="bold cyan", width=20)
        info_table.add_column("Value")

        info_table.add_row("Session ID", session.session_id[:8])
        info_table.add_row("Start Time", session.start_time.strftime("%Y-%m-%d %H:%M"))
        if session.end_time:
            info_table.add_row("End Time", session.end_time.strftime("%Y-%m-%d %H:%M"))
        info_table.add_row("Duration", f"{session.total_duration_seconds:.0f} seconds")
        info_table.add_row("Poses Practiced", str(len(session.pose_scores)))
        if session.sequence_name:
            info_table.add_row("Sequence", session.sequence_name)

        avg_color = self._score_color(session.average_score)
        info_table.add_row(
            "Average Score",
            f"[{avg_color}]{session.average_score:.1f}/100[/{avg_color}]",
        )

        self.console.print(Panel(info_table, title="Session Overview"))
        self.console.print()

        # Individual pose scores
        for score in session.pose_scores:
            self.print_pose_score(score)

        # Summary bar
        self.console.print()
        if session.average_score >= 85:
            msg = "Excellent practice! Your alignment is strong."
        elif session.average_score >= 70:
            msg = "Good practice. Focus on the corrections to improve."
        elif session.average_score >= 50:
            msg = "Keep practicing. Pay attention to the major corrections."
        else:
            msg = "Review the corrections carefully and consider simplifying poses."

        self.console.print(Panel(Text(msg, justify="center"), border_style=avg_color))

    def generate_text_report(self, session: PracticeSession) -> str:
        """Generate a plain-text report string (for file output).

        Args:
            session: The practice session to report on.

        Returns:
            A formatted plain-text report string.
        """
        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("YOGA PRACTICE SESSION REPORT")
        lines.append("=" * 60)
        lines.append(f"Session ID : {session.session_id[:8]}")
        lines.append(f"Date       : {session.start_time.strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"Duration   : {session.total_duration_seconds:.0f} seconds")
        lines.append(f"Poses      : {len(session.pose_scores)}")
        lines.append(f"Avg Score  : {session.average_score:.1f}/100")
        if session.sequence_name:
            lines.append(f"Sequence   : {session.sequence_name}")
        lines.append("-" * 60)

        for score in session.pose_scores:
            lines.append(f"\n{score.asana_name} - Score: {score.overall_score:.1f}/100")
            for joint, jscore in sorted(score.joint_scores.items()):
                lines.append(f"  {joint:25s} : {jscore:.1f}")
            if score.corrections:
                lines.append("  Corrections:")
                for c in score.corrections:
                    lines.append(
                        f"    [{c.severity.value.upper()}] {c.body_part}: {c.instruction}"
                    )
            else:
                lines.append("  No corrections needed.")

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)
