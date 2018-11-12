import click

from simple_stocks.app import app


@click.command()
@click.option("--host", default="0.0.0.0", help="Host to run on", type=str)
@click.option("--port", default=8080, help="Port to run on", type=int)
@click.option("--debug", default=True, help="Use debug", is_flag=True)
@click.option("--auto-reload", default=False, help="Use auto reload (breaks debugger)", is_flag=True)
def run(host: str, port: int, debug: bool, auto_reload: bool):
    app.run(host=host, port=port, debug=debug, auto_reload=auto_reload)


if __name__ == "__main__":
    run()
