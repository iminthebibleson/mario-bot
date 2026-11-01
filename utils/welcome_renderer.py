from pathlib import Path
from jinja2 import Template
from playwright.async_api import async_playwright
import uuid


async def generate_welcome(
    username,
    avatar,
    guild_name,
    member_count
):

    template_path = Path(
        "cogs/welcome/templates/welcome.html"
    )

    base_dir = template_path.parent.resolve()

    css_path = (base_dir / "output.css").resolve().as_uri()

    # render HTML
    html = Template(
        template_path.read_text(encoding="utf-8")
    ).render(
        username=username,
        avatar=avatar,
        guild_name=guild_name,
        member_count=member_count,
        css_path=css_path
    )

    # 🔥 create temp file (IMPORTANT FIX)
    temp_file = base_dir / f"welcome_{uuid.uuid4().hex}.html"
    temp_file.write_text(html, encoding="utf-8")

    try:
        async with async_playwright() as p:

            browser = await p.chromium.launch(headless=True)

            page = await browser.new_page(
                viewport={"width": 1200, "height": 630}
            )

            # 🔥 KEY FIX (match your working Fortnite system)
            await page.goto(
                temp_file.resolve().as_uri(),
                wait_until="networkidle"
            )

            image_bytes = await page.screenshot()

            await browser.close()

    finally:
        temp_file.unlink(missing_ok=True)

    return image_bytes