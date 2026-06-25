"""
Page Inspector
Playwright ile sayfaya girer, DOM'u okur, etkileşilebilir elementleri çıkarır.
Claude'a gönderilecek ham veriyi hazırlar.
"""
from dataclasses import dataclass, field
from typing import List
from playwright.sync_api import sync_playwright


@dataclass
class PageElement:
    tag: str
    element_type: str       # button, input, link, select, text, image
    text: str
    selector: str
    attributes: dict = field(default_factory=dict)


@dataclass
class PageSnapshot:
    url: str
    title: str
    elements: List[PageElement] = field(default_factory=list)

    def to_prompt_text(self) -> str:
        """Claude'a gönderilecek formata çevir."""
        lines = [
            f"URL: {self.url}",
            f"Title: {self.title}",
            f"",
            f"Interactive elements:",
        ]
        for el in self.elements:
            attrs = ""
            if el.attributes.get("placeholder"):
                attrs += f" placeholder='{el.attributes['placeholder']}'"
            if el.attributes.get("data-test"):
                attrs += f" data-test='{el.attributes['data-test']}'"
            if el.attributes.get("type"):
                attrs += f" type='{el.attributes['type']}'"
            lines.append(
                f"  [{el.element_type.upper()}] '{el.text}' | selector: {el.selector}{attrs}"
            )
        return "\n".join(lines)


class PageInspector:
    def __init__(self, username: str = "standard_user", password: str = "secret_sauce"):
        self.username = username
        self.password = password

    def inspect(self, url: str) -> PageSnapshot:
        """Navigate to URL, extract all interactive elements."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Login first if not on login page
            if "saucedemo.com" in url and "index" not in url:
                page.goto("https://www.saucedemo.com")
                page.fill("#user-name", self.username)
                page.fill("#password", self.password)
                page.click("#login-button")
                page.wait_for_url("**/inventory.html")

            page.goto(url)
            page.wait_for_load_state("networkidle")

            title = page.title()
            elements = self._extract_elements(page)

            browser.close()

        return PageSnapshot(url=url, title=title, elements=elements)

    def _extract_elements(self, page) -> List[PageElement]:
        elements = []

        # Buttons
        for btn in page.locator("button").all():
            try:
                text = btn.inner_text().strip()
                selector = self._best_selector(btn)
                if selector:
                    elements.append(PageElement(
                        tag="button",
                        element_type="button",
                        text=text or "[no text]",
                        selector=selector,
                        attributes={
                            "data-test": btn.get_attribute("data-test") or "",
                        }
                    ))
            except Exception:
                continue

        # Inputs
        for inp in page.locator("input").all():
            try:
                selector = self._best_selector(inp)
                placeholder = inp.get_attribute("placeholder") or ""
                input_type = inp.get_attribute("type") or "text"
                inp_id = inp.get_attribute("id") or ""
                if selector:
                    elements.append(PageElement(
                        tag="input",
                        element_type="input",
                        text=inp_id or placeholder,
                        selector=selector,
                        attributes={
                            "type": input_type,
                            "placeholder": placeholder,
                            "data-test": inp.get_attribute("data-test") or "",
                        }
                    ))
            except Exception:
                continue

        # Links
        for link in page.locator("a").all():
            try:
                text = link.inner_text().strip()
                href = link.get_attribute("href") or ""
                if text and href:
                    elements.append(PageElement(
                        tag="a",
                        element_type="link",
                        text=text,
                        selector=f"a[href='{href}']",
                        attributes={"href": href}
                    ))
            except Exception:
                continue

        # Select dropdowns
        for sel in page.locator("select").all():
            try:
                selector = self._best_selector(sel)
                data_test = sel.get_attribute("data-test") or ""
                if selector:
                    elements.append(PageElement(
                        tag="select",
                        element_type="select",
                        text=data_test or "dropdown",
                        selector=selector,
                        attributes={"data-test": data_test}
                    ))
            except Exception:
                continue

        return elements

    def _best_selector(self, locator) -> str:
        """Pick the most stable selector for an element."""
        try:
            data_test = locator.get_attribute("data-test")
            if data_test:
                return f"[data-test='{data_test}']"

            el_id = locator.get_attribute("id")
            if el_id:
                return f"#{el_id}"

            name = locator.get_attribute("name")
            if name:
                tag = locator.evaluate("el => el.tagName.toLowerCase()")
                return f"{tag}[name='{name}']"

            class_name = locator.get_attribute("class")
            if class_name:
                first_class = class_name.split()[0]
                tag = locator.evaluate("el => el.tagName.toLowerCase()")
                return f"{tag}.{first_class}"
        except Exception:
            pass
        return ""
