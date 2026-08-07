import pytest
from playwright.sync_api import Page, expect

from config import settings


DATE_PICKER_URL = settings.BASE_URL + "/date-picker"

def test_dp_001_native_date_input(page: Page):
    """DP_001: Verify date can be typed into a native date input.

    Expected: Input value equals the typed date string.

    Steps:
    1. Locate [data-testid="dp-basic-input"].
    2. Fill with a valid date string (e.g. 2025-06-15).
    3. Assert inputValue() equals 2025-06-15.
    """
    page.goto(DATE_PICKER_URL)
    date_input = page.locator('[data-testid="dp-basic-input"]')

    date_input.fill("2025-06-15")
    expect(date_input).to_have_value("2025-06-15")


def test_dp_003_select_day_from_calendar(page: Page):
    """DP_003: Verify a specific day can be selected from the calendar.

    Expected: Clicking a day cell updates the displayed selected date.

    Steps:
    1. Open the calendar via [data-testid="dp-calendar-trigger"].
    2. Click [data-testid="dp-day-btn"][data-date="2026-08-31"].
    3. Assert the result display shows the selected date.
    """
    page.goto(DATE_PICKER_URL)
    trigger = page.locator('[data-testid="dp-calendar-trigger"]')
    day_btn = page.locator('[data-testid="dp-day-btn"][data-date="2026-08-31"]')
    result_display = page.locator('[data-testid="result-s02"]')

    trigger.click()
    day_btn.click()
    expect(result_display).to_contain_text("2026-08-31")


def test_dp_004_calendar_month_navigation(page: Page):
    """DP_004: Verify next-month navigation updates the calendar header.

    Expected: Month heading increments by one after clicking next.

    Steps:
    1. Open the calendar.
    2. Note the current month heading.
    3. Click [data-testid="dp-next-month"].
    4. Assert the heading now shows the following month.
    """
    page.goto(DATE_PICKER_URL)
    trigger = page.locator('[data-testid="dp-calendar-trigger"]')
    next_btn = page.locator('[data-testid="dp-next-month"]')
    month_heading = page.locator("#dp-calendar-month-heading")

    trigger.click()
    initial_month = month_heading.text_content()

    next_btn.click()
    expect(month_heading).not_to_have_text(initial_month)


def test_dp_006_date_range_selection(page: Page):
    """DP_006: Verify date range start and end inputs accept valid dates.

    Expected: Both inputs hold the correct date strings and the range summary updates.

    Steps:
    1. Fill [data-testid="dp-range-start"] with 2025-08-01.
    2. Fill [data-testid="dp-range-end"] with 2025-08-15.
    3. Assert the range summary text includes both dates.
    """
    page.goto(DATE_PICKER_URL)
    start_input = page.locator('[data-testid="dp-range-start"]')
    end_input = page.locator('[data-testid="dp-range-end"]')
    summary = page.locator('[data-testid="result-s04"]')

    start_input.fill("2025-08-01")
    end_input.fill("2025-08-15")

    expect(start_input).to_have_value("2025-08-01")
    expect(end_input).to_have_value("2025-08-15")
    expect(summary).to_contain_text("2025-08-01")
    expect(summary).to_contain_text("2025-08-15")


def test_dp_007_min_date_constraint_validation(page: Page):
    """DP_007: Verify constrained input rejects dates before min.

    Expected: Input is invalid or shows browser validation error when value < min.

    Steps:
    1. Locate [data-testid="dp-constrained-input"].
    2. Fill with a date earlier than its min attribute.
    3. Assert the input's validity state is invalid.
    """
    page.goto(DATE_PICKER_URL)
    constrained_input = page.locator('[data-testid="dp-constrained-input"]')

    constrained_input.fill("2020-01-01")

    is_valid = constrained_input.evaluate("el => el.checkValidity()")
    assert is_valid is False


def test_dp_009_xpath_ancestor_date_input(page: Page):
    """DP_009: Verify sibling date field located via XPath ancestor.

    Expected: Input fills correctly when located through a label sibling.

    Steps:
    1. Use XPath: //span[normalize-space()="Appointment Date"]/following-sibling::div/input
    2. Fill the input with a date.
    3. Assert the value updates.
    """
    page.goto(DATE_PICKER_URL)
    xpath_locator = page.locator('//span[normalize-space()="Appointment Date"]/following-sibling::div/input')

    xpath_locator.fill("2025-10-10")
    expect(xpath_locator).to_have_value("2025-10-10")


def test_dp_014_clear_date_input(page: Page):
    """DP_014: Verify clearing a date input resets the display.

    Expected: After clearing, the result shows the empty/reset state.

    Steps:
    1. Fill a date input, then clear it.
    2. Assert the displayed result reverts to the initial placeholder text.
    """
    page.goto(DATE_PICKER_URL)
    date_input = page.locator('[data-testid="dp-basic-input"]')
    result_display = page.locator('[data-testid="result-s01"]')

    date_input.fill("2025-06-15")
    date_input.clear()

    expect(date_input).to_have_value("")
    expect(result_display).to_contain_text("No date selected")