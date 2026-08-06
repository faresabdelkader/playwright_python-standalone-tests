
from playwright.sync_api import Page, expect
from config import settings
import pytest

RADIO_CHECKBOXES_URL = settings.BASE_URL + "/radio-checkbox"


def test_rc_001_checkbox_toggle_states(page: Page):
    """RC_001: Verify checkbox can be checked and unchecked.

    Expected: isChecked() returns true after check(), and false after uncheck().

    Steps:
    1. Locate [data-testid="chk-accept-terms"].
    2. Call check() or click().
    3. Assert isChecked() is true.
    4. Call uncheck().
    5. Assert isChecked() is false.
    """
    page.goto(RADIO_CHECKBOXES_URL)
    checkbox = page.locator('[data-testid="chk-accept-terms"]')

    checkbox.check()
    expect(checkbox).to_be_checked()

    checkbox.uncheck()
    expect(checkbox).not_to_be_checked()


def test_rc_004_radio_group_mutual_exclusion(page: Page):
    """RC_004: Verify only one radio in a group can be selected at a time.

    Expected: Selecting a second radio automatically deselects the first.

    Steps:
    1. Scope to [data-testid="radio-plan-group"].
    2. Select "Starter" radio and assert it is checked.
    3. Select "Pro" radio.
    4. Assert "Pro" is checked.
    5. Assert "Starter" is no longer checked.
    """
    page.goto(RADIO_CHECKBOXES_URL)
    plan_group = page.locator('[data-testid="radio-plan-group"]')
    starter_radio = plan_group.get_by_label("Starter")
    pro_radio = plan_group.get_by_label("Pro")

    starter_radio.check()
    expect(starter_radio).to_be_checked()

    pro_radio.check()
    expect(pro_radio).to_be_checked()
    expect(starter_radio).not_to_be_checked()


def test_rc_005_check_all_checkboxes_in_group(page: Page):
    """RC_005: Verify all checkboxes in a group can be checked.

    Expected: All checkboxes with data-testid="chk-skill" are checked.

    Steps:
    1. Get all elements with [data-testid="chk-skill"].
    2. Loop and call check() on each.
    3. Assert all return isChecked() === true.
    """
    page.goto(RADIO_CHECKBOXES_URL)
    skill_checkboxes = page.locator('[data-testid="chk-skill"]')

    count = skill_checkboxes.count()
    for i in range(count):
        checkbox = skill_checkboxes.nth(i)
        checkbox.check()
        expect(checkbox).to_be_checked()


def test_rc_007_disabled_checkbox_interaction(page: Page):
    """RC_007: Verify disabled checkbox cannot be interacted with.

    Expected: isDisabled() returns true; check() throws or has no effect.

    Steps:
    1. Locate [data-testid="chk-disabled"].
    2. Assert isDisabled() is true.
    3. Attempt check() — assert no state change.
    """
    page.goto(RADIO_CHECKBOXES_URL)
    disabled_checkbox = page.locator('[data-testid="chk-disabled"]')

    expect(disabled_checkbox).to_be_disabled()

    with pytest.raises(Exception):
        disabled_checkbox.check(timeout=1000)


def test_rc_010_scoped_plan_card_radio_selection(page: Page):
    """RC_010: Verify scoped plan card radio can be selected.

    Expected: Radio inside the Enterprise plan card is checked after scoped selection.

    Steps:
    1. Locate [data-testid="plan-card"][data-plan="enterprise"].
    2. Find the radio input inside and call check().
    3. Assert it is checked.
    """
    page.goto(RADIO_CHECKBOXES_URL)
    enterprise_card = page.locator('[data-testid="plan-card"][data-plan="enterprise"]')
    enterprise_radio = enterprise_card.locator('input[type="radio"]')

    enterprise_radio.check()
    expect(enterprise_radio).to_be_checked()


def test_rc_012_checkbox_result_span_update(page: Page):
    """RC_012: Verify checkbox result span updates after interaction.

    Expected: The result span text changes to reflect the new checked state.

    Steps:
    1. Check a checkbox.
    2. Locate the result span by its id.
    3. Assert the span text reflects the checked state.
    """
    page.goto(RADIO_CHECKBOXES_URL)
    checkbox = page.locator('[id="chk-accept-terms"] ')
    result_span = page.locator('[id="result-s01"]')

    checkbox.check()
    expect(result_span).to_contain_text("Checked")


def test_rc_013_keyboard_accessibility_tab_space(page: Page):
    """RC_013: Verify checkbox is accessible via keyboard Tab and Space.

    Expected: Checkbox can be focused and toggled using keyboard only.

    Steps:
    1. Tab to [data-testid="chk-accept-terms"].
    2. Press Space to toggle.
    3. Assert isChecked() is true.
    """
    page.goto(RADIO_CHECKBOXES_URL)
    checkbox = page.locator('[data-testid="chk-accept-terms"]')

    checkbox.focus()
    expect(checkbox).to_be_focused()

    page.keyboard.press("Space")
    expect(checkbox).to_be_checked()