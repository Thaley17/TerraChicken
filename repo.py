import typer
import functions

app = typer.Typer()


@app.command()
def delete(name: str):
    full_name = f"Thaley17/{name}"
    typer.confirm(f"Are you sure you want to delete Thaley17/{name}?" , abort=True )
    functions.deleteRepo(full_name)

@app.command()
def list():
    pass

if __name__ == "__main__":
    app()