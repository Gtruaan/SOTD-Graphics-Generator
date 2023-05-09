import asyncio
from io import BytesIO
import requests

from src.utils import log, render_html_css, screenshot
from src.spotify import getTrackAttributes
from src.colors import getColors, sortColors


# Async due to pyppeteer
async def main():
    top = input("Top number: ")
    track = input("Search track: ")

    log("Fetching track info...")
    attributes = getTrackAttributes(track)
    if attributes is None:
        log("Track not found.")
        return
    image_url = attributes[0]
    track_name = attributes[1]
    artist_name = attributes[2]

    log("Fetching track cover...")
    response = requests.get(image_url)
    track_image_file = BytesIO(response.content)

    while True:
        log("Computing cover colors...")
        colors = list(getColors(track_image_file, 5))
        colors = sortColors(colors)

        log("Rendering html and css...")
        html, css = render_html_css(colors, top, image_url,
                                    track_name, artist_name)

        log("Generating screenshot...")
        await screenshot(html, css)

        log("Done.")

        action = input("Press 0 to end program, " +
                       "any other key to continue " +
                       "generating colors for this track\n")

        if action == "0":
            break


if __name__ == "__main__":
    asyncio.run(main())
