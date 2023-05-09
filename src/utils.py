import os
from pyppeteer import launch


def log(message: str):
    """
    Clears console and displays message
    """
    os.system("cls")
    print(message)


def render_html_css(colors: list, top: str, image_url: str,
                    track_name: str, artist_name: str) -> tuple:
    """
    Renders html and css, and returns them as strings
    """
    replace_str = ""

    for idx, color in enumerate(colors):
        color_code = ', '.join(list(map(lambda x: str(int(x)), color)))
        replace_str += f"--color_{idx + 1}: rgb({color_code});\n"

    with open("assets/display.html", "r") as f:
        html = f.read().format(
                               top,
                               image_url,
                               track_name,
                               artist_name
                               )

    with open("assets/style.css", "r") as f:
        css = f.read()
        css = css.replace("/* colors will go here */", replace_str)

    return html, css


async def screenshot(html: str, css: str):
    """
    Takes a screenshot of the html and css
    """
    browser = await launch()
    page = await browser.newPage()

    await page.setContent(html)
    await page.addStyleTag(content=css)
    await page.addScriptTag(path="assets/load-check.js")

    await page.waitForSelector("#load-checker")
    await page.screenshot(path="out.png",
                          width=1080, height=1920, fullPage=True)

    await browser.close()
