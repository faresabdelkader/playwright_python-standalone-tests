
import pytest
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect
from config import settings

DYNAMIC_WAITS_URL = settings.BASE_URL + "/dynamic-waits"

def test_dw_001_wait_for_selector_delayed_element(page: Page):
    """DW_001: Verify waitForSelector resolves when delayed element appears.

    Expected: Element is visible within the wait timeout.

    Steps:
    1. Navigate to /practice/dynamic-waits
    2. Click [data-testid="dw-trigger-delayed"].
    3. Call waitForSelector('[data-testid="dw-delayed-result"]', { state: "visible" }).
    4. Assert the element text is not empty.
    """
    page.goto(DYNAMIC_WAITS_URL)
    page.locator('[data-testid="dw-trigger-delayed"]').click()
    waited_element = page.wait_for_selector('[data-testid="dw-delayed-result"]', state="visible", timeout=5000)
    assert waited_element is not None, "Expected the delayed result element to be found and visible"


def test_dw_002_wait_for_selector_timeout(page: Page):
    """DW_002: Verify waitForSelector times out when element never appears.

    Expected: A TimeoutError is thrown after the configured timeout.

    Steps:
    1. Navigate to /practice/dynamic-waits
    2. Do NOT click the trigger.
    3. Call waitForSelector('[data-testid="dw-delayed-result"]', { timeout: 1000 }).
    4. Assert a TimeoutError is thrown.
    """
    page.goto(DYNAMIC_WAITS_URL)
    with pytest.raises(PlaywrightTimeoutError):
        page.wait_for_selector('[data-testid="dw-delayed-result"]', timeout=1000)


def test_dw_004_spinner_disappears_content_appears(page: Page):
    """DW_004: Verify spinner disappears and content appears after loading.

    Expected: dw-spinner hidden; dw-spinner-content visible.

    Steps:
    1. Navigate to /practice/dynamic-waits
    2. Click [data-testid="dw-trigger-spinner"].
    3. Wait for [data-testid="dw-spinner"] to have state "hidden".
    4. Assert [data-testid="dw-spinner-content"] is visible.
    """
    page.goto(DYNAMIC_WAITS_URL)
    spinner_trigger = page.locator('[data-testid="dw-trigger-spinner"]')
    spinner_trigger.click()
    expect(spinner_trigger).to_be_disabled(timeout=5000)
    expect(page.locator('[data-testid="dw-spinner-content"]')).to_be_visible(timeout=5000)


def test_dw_005_toast_message_appears(page: Page):
    """DW_005: Verify toast message appears and contains expected text.

    Expected: dw-toast is visible with correct message text.

    Steps:
    1. Navigate to /practice/dynamic-waits
    2. Click [data-testid="dw-trigger-toast"].
    3. Wait for [data-testid="dw-toast"] to be visible.
    4. Assert its text contains "Success".
    """
    page.goto(DYNAMIC_WAITS_URL)
    toast_trigger = page.locator('[data-testid="dw-trigger-toast"]')
    toast_trigger.click()
    toast_element = page.wait_for_selector('[data-testid="dw-toast"]', state="visible", timeout=3000)
    assert toast_element is not None, "Expected the toast element to be found and visible"
    assert "Success" in toast_element.text_content(), "Expected the toast message to contain 'Success'"


def test_dw_006_toast_auto_dismisses(page: Page):
    """DW_006: Verify toast auto-dismisses within 4 seconds.

    Expected: dw-toast is no longer in DOM after dismiss delay.

    Steps:
    1. Navigate to /practice/dynamic-waits
    2. Click the toast trigger.
    3. Assert the toast appears.
    4. Wait 4 seconds.
    5. Assert [data-testid="dw-toast"] has state "hidden" or does not exist.
    """
    page.goto(DYNAMIC_WAITS_URL)
    toast_trigger = page.locator('[data-testid="dw-trigger-toast"]')
    toast_trigger.click()
    toast_element = page.wait_for_selector('[data-testid="dw-toast"]', state="visible", timeout=500)
    assert toast_element is not None, "Expected the toast element to be found and visible"
    expect(page.locator('[data-testid="dw-toast"]')).to_be_hidden(timeout=4000)


def test_dw_007_wait_for_function_polling_counter(page: Page):
    """DW_007: Verify waitForFunction resolves when counter reaches target.

    Expected: waitForFunction returns when dw-poll-count text equals '5'.

    Steps:
    1. Navigate to /practice/dynamic-waits
    2. Click [data-testid="dw-trigger-poll"].
    3. Call page.waitForFunction(() => document.querySelector('[data-testid="dw-poll-count"]')?.textContent === "5").
    4. Assert the count span shows 5.
    """
    page.goto(DYNAMIC_WAITS_URL)
    poll_trigger = page.locator('[data-testid="dw-trigger-poll"]')
    poll_trigger.click()
    page.wait_for_function(
        """() => {
            const countElement = document.querySelector('[data-testid="dw-poll-count"]');
            return countElement && countElement.textContent === "5";
        }""",
        timeout=5000
    )
    count_text = page.locator('[data-testid="dw-poll-count"]').text_content()
    assert count_text == "5", f"Expected the poll count to be '5', but got '{count_text}'"


def test_dw_008_disabled_button_becomes_enabled(page: Page):
    """DW_008: Verify disabled button becomes enabled after delay.

    Expected: dw-submit-btn transitions from disabled to enabled.

    Steps:
    1. Navigate to /practice/dynamic-waits
    2. Assert [data-testid="dw-submit-btn"] is disabled on load.
    3. Wait for waitFor({ state: "enabled" }).
    4. Assert the button is now enabled.
    5. Click it and assert the result.
    """
    page.goto(DYNAMIC_WAITS_URL)
    submit_button = page.locator('[data-testid="dw-submit-btn"]')
    expect(submit_button).to_be_disabled()
    page.locator('[data-testid="dw-arm-enable"]').click()
    expect(submit_button).to_be_enabled(timeout=5000)
    submit_button.click()
    result_text = page.locator('[data-testid="result-s05"]').text_content()
    assert result_text == "Submit clicked after wait",f"Expected the submit result to be 'Submit clicked after wait', but got '{result_text}'"


def test_dw_009_text_change_detection(page: Page):
    """DW_009: Verify text change is detected via waitForFunction.

    Expected: Status span text changes from 'Idle' to 'Done'.

    Steps:
    1. Navigate to /practice/dynamic-waits
    2. Click the status trigger.
    3. Use waitForFunction until the span text is "Done".
    4. Assert final text value.
    """
    page.goto(DYNAMIC_WAITS_URL)
    initial_status = page.locator('//span[@class="status-value text-sm font-semibold text-foreground"]').text_content()
    assert initial_status == "Idle", f"Expected initial status to be 'Idle', but got '{initial_status}'"
    status_trigger = page.locator('[data-testid="dw-trigger-status"]')
    status_trigger.click()
    page.wait_for_function(
        """() => {
            const statusElement = document.querySelector('span.status-value.text-sm.font-semibold.text-foreground');
            return statusElement && statusElement.textContent === "Done";
        }""",
        timeout=5000
    )
    final_status = page.locator('//span[@class="status-value text-sm font-semibold text-foreground"]').text_content()
    assert final_status == "Done", f"Expected the status to be 'Done', but got '{final_status}'"


def test_dw_010_simulated_fetch_network_wait(page: Page):
    """DW_010: Verify simulated fetch result appears after network wait.

    Expected: dw-fetch-result is visible with non-empty text.

    Steps:
    1. Navigate to /practice/dynamic-waits
    2. Click [data-testid="dw-fetch-btn"].
    3. Wait for [data-testid="dw-fetch-result"] to be visible.
    4. Assert its text is not empty.
    """
    page.goto(DYNAMIC_WAITS_URL)
    fetch_trigger = page.locator('[data-testid="dw-fetch-btn"]')
    fetch_trigger.click()
    fetch_result = page.wait_for_selector('[data-testid="dw-fetch-result"]', state="visible", timeout=5000)
    assert fetch_result is not None, "Expected the fetch result element to be found and visible"
    assert fetch_result.text_content().strip() != "", "Expected the fetch result text to be non-empty"


def test_dw_011_race_condition_element(page: Page):
    """DW_011: Verify race-condition element can be caught within timeout.

    Expected: Element is found before it disappears when timeout is sufficient.

    Steps:
    1. Navigate to /practice/dynamic-waits
    2. Click [data-testid="dw-race-btn"] trigger.
    3. Use waitForSelector('[data-testid="dw-race-target"]', { timeout: 5000 }).
    4. If found, assert it is visible; if not, assert a TimeoutError was thrown.
    """
    page.goto(DYNAMIC_WAITS_URL)
    race_trigger = page.locator('[data-testid="dw-trigger-race"]')
    race_trigger.click()
    try:    
        race_element = page.wait_for_selector('[data-testid="dw-race-target"]', state="visible", timeout=5000)
        assert race_element is not None, "Expected the race target element to be found and visible"
    except PlaywrightTimeoutError:
        pytest.fail("Race target element did not appear within the timeout, indicating a race condition was not handled properly.")         