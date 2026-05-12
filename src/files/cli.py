import typer
from .picdown import picdown

app = typer.Typer()
app.command()(picdown)

if __name__ == "__main__":
    app()