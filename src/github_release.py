import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

API_URL = "https://api.github.com/repos/elvezjp/IXV-util-MarkItDown/releases/latest"


def fetch_latest_release():
    """Fetch latest release information from GitHub Releases API.

    Returns:
        dict: A dictionary with release information.

    Raises:
        RuntimeError: If the API request fails or returns invalid data.
    """
    try:
        with urlopen(API_URL) as response:
            data = json.load(response)
    except (HTTPError, URLError, json.JSONDecodeError) as e:  # pragma: no cover - network errors
        raise RuntimeError(f"Failed to fetch release info: {e}") from e

    return {
        "tag_name": data.get("tag_name"),
        "name": data.get("name"),
        "html_url": data.get("html_url"),
    }
