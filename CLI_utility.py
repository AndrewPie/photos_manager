from pathlib import Path

import requests
import typer
from requests.models import Response

photo_sources = {1: "API", 2: "local and proper JSON file"}


class CLIUtility:
    def __init__(self):
        self.photo_source: int | None = None
        self.api_input_data: dict[str | None, str | int | None] = {}
        self.json_input_data: dict[str | None, str | int | Path | None] = {}

    def __select_source(self):
        typer.echo("Select photo source")
        for number, source in photo_sources.items():
            typer.echo(f"[{number}] {source}")
        source_number = int(typer.prompt("Your choice?"))
        if source_number in photo_sources:
            self.photo_source = source_number
        else:
            return self.__select_source()

    def __get_API_data(self):
        title = typer.prompt("Enter photo title")
        album_id = int(typer.prompt("Enter photo album ID"))
        external_url = typer.prompt("Enter photo external url")
        self.api_input_data = {
            "title": title,
            "album_ID": album_id,
            "external_url": external_url,
        }

    def __get_file_data(self):
        title = typer.prompt("Enter photo title")
        album_id = int(typer.prompt("Enter photo album ID"))
        json_path = Path(typer.prompt("Enter file path"))
        if json_path.exists() and json_path.is_file():
            self.json_input_data = {
                "title": title,
                "album_ID": album_id,
                "json_path": json_path,
            }
        else:
            typer.echo(f"Incorrect json file path")
            return self.__get_file_data()

    def __get_api_response(self) -> Response:
        match self.photo_source:
            case 1:
                self.__get_API_data()
                api_post_response = requests.post(
                    "http://127.0.0.1:8000/api/photos/", json=self.api_input_data
                )
            case 2:
                self.__get_file_data()
                url = "http://127.0.0.1:8000/api/photos/from_json"
                json_file = self.json_input_data.get("json_path")

                file = {"json_file": open(json_file, "rb")}
                payload = {
                    "title": self.json_input_data.get("title"),
                    "album_ID": self.json_input_data.get("album_ID"),
                }
                api_post_response = requests.post(url, files=file, data=payload)
        return api_post_response

    def run_photo_import(self):
        typer.echo("PHOTO IMPORT UTILITY")
        if not self.photo_source:
            self.__select_source()
        api_post_response = self.__get_api_response()
        if api_post_response.status_code in (200, 201):
            typer.echo(f"Photo added\n" f"url: {api_post_response.json().get('url')}")
        else:
            typer.echo(f"Exception: {api_post_response.content}")
            return self.run_photo_import()


if __name__ == "__main__":
    typer.run(CLIUtility().run_photo_import)
