import re
import pytest
from playwright.sync_api import Page, expect
from config import settings

TABS_AND_WINDOWS_URL = settings.BASE_URL+"/tabs-windows"

def test_tw_002_new_tab_url_and_creation(page: Page, context):
    """TW_002: Verify new tab opens and URL matches expected destination.

    Expected: context.pages().length increases and newPage.url() equals the expected destination.

    Steps:
    1. Set up a listener with context.expect_page() before clicking.
    2. Click [data-testid="tw-open-new-tab"].
    3. Await the new page context.
    4. Assert context pages count equals 2 and URL is correct.
    """
    page.goto(TABS_AND_WINDOWS_URL)

    with context.expect_page() as new_page_info:
        page.locator('[data-testid="tw-open-new-tab"]').click()

    new_page = new_page_info.value
    new_page.wait_for_load_state()

    assert len(context.pages) == 2
    expect(new_page).to_have_url("https://qaplayground.com/practice/tabs-windows")


def test_tw_003_new_tab_title(page: Page, context):
    """TW_003: Verify new tab title matches expected value.

    Expected: newPage.title() returns the correct page title.

    Steps:
    1. Switch to the new tab context.
    2. Wait for load state.
    3. Assert newPage.title() contains the expected text.
    """
    page.goto(TABS_AND_WINDOWS_URL)

    with context.expect_page() as new_page_info:
        page.locator('[data-testid="tw-open-new-tab"]').click()

    new_page = new_page_info.value
    new_page.wait_for_load_state()
    expect(new_page).to_have_title(re.compile("QA Playground"))


def test_tw_004_switch_back_to_original_tab(page: Page, context):
    """TW_004: Verify switching back to the original tab restores context.

    Expected: The original page URL is still correct after switching back.

    Steps:
    1. Open a new tab and switch to it.
    2. Call context.pages[0].bring_to_front().
    3. Assert the original page URL has not changed.
    """
    page.goto(TABS_AND_WINDOWS_URL)
    original_url = page.url

    with context.expect_page() as new_page_info:
        page.locator('[data-testid="tw-open-new-tab"]').click()

    new_page = new_page_info.value
    new_page.wait_for_load_state()

    page.bring_to_front()
    expect(page).to_have_url(original_url)


def test_tw_005_closing_tab_reduces_count(page: Page, context):
    """TW_005: Verify closing a tab reduces the open tab count.

    Expected: context.pages length decrements by 1 after close().

    Steps:
    1. Open a new tab — assert count is 2.
    2. Call newPage.close().
    3. Assert context.pages length === 1.
    """
    page.goto(TABS_AND_WINDOWS_URL)

    with context.expect_page() as new_page_info:
        page.locator('[data-testid="tw-open-new-tab"]').click()

    new_page = new_page_info.value
    assert len(context.pages) == 2

    new_page.close()
    assert len(context.pages) == 1


def test_tw_006_multiple_tabs_simultaneously(page: Page, context):
    """TW_006: Verify multiple tabs can be opened simultaneously.

    Expected: All three tab buttons produce independent page contexts.

    Steps:
    1. Click each of the three tab-open buttons inside [data-testid="tw-multi-tab-panel"].
    2. Assert context.pages().length === 4.
    """
    page.goto(TABS_AND_WINDOWS_URL)
    multi_panel = page.locator('[data-testid="tw-multi-tab-panel"]')
    buttons = multi_panel.locator("button")

    count = buttons.count()
    for i in range(count):
        with context.expect_page():
            buttons.nth(i).click()

    assert len(context.pages) == count + 1


def test_tw_007_popup_window_capture(page: Page):
    """TW_007: Verify window.open popup is captured in Playwright.

    Expected: page.expect_popup() resolves to the popup page.

    Steps:
    1. Register page.expect_popup() before the click.
    2. Click [data-testid="tw-popup-btn"].
    3. Await the popup page and assert its URL.
    """
    page.goto(TABS_AND_WINDOWS_URL)

    with page.expect_popup() as popup_info:
        page.locator('[data-testid="tw-popup-btn"]').click()

    popup = popup_info.value
    popup.wait_for_load_state()
    expect(popup).to_have_url("https://qaplayground.com/practice/tabs-windows")


def test_tw_009_xpath_sibling_tab_click(page: Page, context):
    """TW_009: Verify sibling-located tab button can be clicked via XPath.

    Expected: Button located by structural XPath fires the tab-open action.

    Steps:
    1. Use XPath: //div[@data-testid="tw-sibling-panel"]//button[normalize-space()="Open Tab B"].
    2. Click the located button.
    3. Assert result span updates.
    """
    page.goto(TABS_AND_WINDOWS_URL)
    original_url = page.url
    
    with context.expect_page() as new_page_info:
        page.locator('//div[@data-testid="tw-sibling-panel"]/button[2]').click()
    
    new_page = new_page_info.value
    new_page.wait_for_load_state()
    
    page.bring_to_front()
    expect(page).to_have_url(original_url)
    result_span = page.locator('[data-testid="result-s07"]')

    expect(result_span).to_have_text("Open Tab B opened via sibling locator")


def test_tw_010_dynamic_tab_row_xpath(page: Page):
    """TW_010: Verify dynamic tab registry row located by cell text.

    Expected: Focus button inside the Tab C row is clicked successfully.

    Steps:
    1. Use XPath: //tr[td[normalize-space()="Tab C"]]//button[normalize-space()="Focus"].
    2. Click the Focus button.
    3. Assert the result span shows Tab C focused.
    """
    page.goto(TABS_AND_WINDOWS_URL)
    focus_btn = page.locator(
        'xpath=//tr[td[normalize-space()="Tab C"]]//button[normalize-space()="Focus"]'
    )
    result_span = page.locator('[data-testid="result-s08"]')

    focus_btn.click()
    expect(result_span).to_contain_text("Focused: Tab C")


def test_tw_011_target_blank_security_attributes(page: Page):
    """TW_011: Verify tab with target=_blank has correct attribute.

    Expected: The anchor element has target="_blank" and rel="noopener noreferrer".

    Steps:
    1. Locate the link element.
    2. Assert getAttribute("target") === "_blank".
    3. Assert getAttribute("rel") contains "noopener".
    """
    page.goto(TABS_AND_WINDOWS_URL)
    link = page.locator('[data-testid="tw-open-new-tab"]')

    expect(link).to_have_attribute("target", "_blank")
    rel_attribute = link.get_attribute("rel")
    assert rel_attribute is not None and "noopener" in rel_attribute


def test_tw_013_closed_tab_interaction_raises_error(page: Page, context):
    """TW_013: Verify that interacting with a closed tab throws an error.

    Expected: Calling methods on a closed page context raises a Target closed error.

    Steps:
    1. Open and then close a new tab.
    2. Attempt to call newPage.url() on the closed page.
    3. Assert a Target closed error is thrown.
    """
    page.goto(TABS_AND_WINDOWS_URL)

    with context.expect_page() as new_page_info:
        page.locator('[data-testid="tw-open-new-tab"]').click()

    new_page = new_page_info.value
    new_page.close()

    with pytest.raises(Exception):
        new_page.url()