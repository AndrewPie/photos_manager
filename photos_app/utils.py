import requests


def get_photo_data(input_data: dict) -> tuple[str, requests.models.Response] | None:
    if external_photo_url := input_data.get("external_url"):
        try:
            if not input_data.get("is_from_file"):
                json_response = requests.get(external_photo_url).json()
                photo_source_url = json_response.get("url")
            else:
                photo_source_url = external_photo_url
            url_filename = photo_source_url.split("/")[-1]

            dominant_color = f"#{url_filename[0:6]}"
            photo_response = requests.get(f"{photo_source_url}.png")
            return dominant_color, photo_response

        except ValueError:
            raise ValueError("There is no link to the photo in the provided url")
        except requests.exceptions.ConnectionError:
            raise ValueError("Incorrect external url")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
