"""
Temporary file to test the AI analyst plugin.
Delete after verifying the plugin works.
"""
import pytest

@pytest.mark.ai_test
def test_wrong_url_assertion(page, base_url):
    """Intentional fail: wrong URL assertion."""
    page.goto(base_url)
    assert "/inventory.html" in page.url, \
        f"Expected inventory page but got: {page.url}"

@pytest.mark.ai_test
def test_wrong_element(page, base_url):
    """Intentional fail: element that doesn't exist."""
    page.goto(base_url)
    page.click("#nonexistent-button-xyz")
