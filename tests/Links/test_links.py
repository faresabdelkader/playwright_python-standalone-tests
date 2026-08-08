import pytest
from playwright.sync_api import Page, expect
from config import settings

LINKS_URL = settings.BASE_URL + "/links"

def test_lnk_001_navigation(page: Page):
    """LNK_001: Verify link navigates to the correct URL on click.

    Expected: Page URL should update to the target URL.

    Steps:
    1. Locate the link element using an appropriate selector.
    2. Click the link.
    3. Assert that the current page URL matches the link's expected destination.
    """
    page.goto(LINKS_URL)
    link = page.locator('[data-testid="link-internal-home"]')

    link.click()
    page.wait_for_load_state()
    expect(page).to_have_url("https://qaplayground.com/")


def test_lnk_002_label_verification(page: Page):
    """LNK_002: Verify link text matches expected label.

    Expected: Link text should match the expected visible text.

    Steps:
    1. Locate the link element.
    2. Retrieve its visible text.
    3. Assert the text matches the expected label.
    """
    page.goto(LINKS_URL)
    link = page.locator('[data-testid="link-internal-about"]')
    expect(link).to_have_text("About Us")


def test_lnk_003_external_link_new_tab(page: Page, context):
    """LNK_003: Verify external link opens in a new tab.

    Expected: A new window/tab should open with the correct URL.

    Steps:
    1. Locate the external link element.
    2. Assert that it has the target="_blank" attribute.
    3. Click the link and switch to the new window handle/context.
    4. Assert the URL in the new tab.
    """
    page.goto(LINKS_URL)
    external_link = page.locator('[data-testid="link-external-course"]')

    expect(external_link).to_have_attribute("target", "_blank")

    with context.expect_page() as new_page_info:
        external_link.click()

    new_page = new_page_info.value
    new_page.wait_for_load_state()
    expect(new_page).to_have_url("https://www.udemy.com/course/selenium-real-time-examplesinterview-questions/")


def test_lnk_004_internal_link_same_tab(page: Page):
    """LNK_004: Verify internal link stays in the same tab.

    Expected: Navigation should occur in the same window/tab.

    Steps:
    1. Locate an internal link element.
    2. Assert that it does NOT have target="_blank".
    3. Click the link.
    4. Assert the URL changes in the current context.
    """
    page.goto(LINKS_URL)
    internal_link = page.locator('[data-testid="link-internal-home"]')

    expect(internal_link).not_to_have_attribute("target", "_blank")

    internal_link.click()
    page.wait_for_load_state()
    expect(page).to_have_url("https://qaplayground.com/")


def test_lnk_005_broken_link_http_status(page: Page):
    """LNK_005: Verify broken link returns HTTP error status.

    Expected: An HTTP request to the link's href should return an error status (e.g., 404, 500).

    Steps:
    1. Extract the href attribute from the link.
    2. Send an HTTP GET request to the extracted URL.
    3. Assert that the response status code is >= 400.
    """
    page.goto(LINKS_URL)
    broken_link = page.locator('[data-testid="link-broken-same"]')
    href = broken_link.get_attribute("href")

    response = page.request.get(href)
    assert response.status == 500


def test_lnk_006_keyboard_accessibility(page: Page):
    """LNK_006: Verify link is keyboard accessible.

    Expected: Link can be focused and activated via keyboard.

    Steps:
    1. Simulate the Tab key to focus the link.
    2. Simulate the Enter key.
    3. Assert that the link click action is triggered.
    """
    page.goto(LINKS_URL)
    link = page.locator('[data-testid="link-internal-home"]')

    link.focus()
    expect(link).to_be_focused()

    page.keyboard.press("Enter")
    expect(page).to_have_url("https://qaplayground.com/")


def test_lnk_007_href_attribute_validation(page: Page):
    """LNK_007: Verify link href attribute contains the correct URL.

    Expected: The href attribute must contain the exact expected URL.

    Steps:
    1. Locate the link element.
    2. Retrieve the href attribute.
    3. Assert the attribute value equals the expected URL.
    """
    page.goto(LINKS_URL)
    link = page.locator('[data-testid="link-internal-about"]')

    expect(link).to_have_attribute("href", "/about-us")


def test_lnk_008_accessible_label(page: Page):
    """LNK_008: Verify link has accessible label for screen readers.

    Expected: Link should have an aria-label or descriptive text.

    Steps:
    1. Locate the link element.
    2. Check for an aria-label or visually hidden text if the link has no visible text (like an image link).
    3. Assert the accessibility text is present and correct.
    """
    page.goto(LINKS_URL)
    icon_link = page.locator('[data-testid="link-image-ironman"]')

    expect(icon_link).to_have_attribute("aria-label", "Iron Man image link")


def test_lnk_012_navigation_without_console_errors(page: Page):
    """LNK_012: Verify link page loads without console errors.

    Expected: Clicking a link and navigating should not produce JavaScript errors.

    Steps:
    1. Attach a listener to the browser console.
    2. Click the target link.
    3. Wait for the new page to load and assert no console errors are thrown.
    """
    page.goto(LINKS_URL)
    console_errors = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

    link = page.locator('[data-testid="link-internal-home"]')
    link.click()

    page.wait_for_load_state("networkidle")
    assert len(console_errors) == 0