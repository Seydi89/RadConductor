import typer
from rich.console import Console

app = typer.Typer(
    help="RadConductor medical-imaging workflow CLI.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def version() -> None:
    """Show the installed version."""
    console.print("RadConductor 0.1.0")


@app.command()
def analyze(study: str) -> None:
    """Analyze a medical-imaging study."""
    console.print(f"Analyzing: {study}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()