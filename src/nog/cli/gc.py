import typer

app = typer.Typer()


@app.command()
def gc():
    """Garbage collect"""
    pass
