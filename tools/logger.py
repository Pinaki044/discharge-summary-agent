from rich.console import Console

console = Console()


def log_step(step, reasoning, action, result):

    console.print(f"\n[bold blue]STEP {step}[/bold blue]")

    console.print(f"[yellow]Reasoning:[/yellow] {reasoning}")

    console.print(f"[green]Action:[/green] {action}")

    console.print(f"[magenta]Result:[/magenta] {result}")