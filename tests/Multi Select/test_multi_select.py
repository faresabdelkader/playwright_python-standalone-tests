from playwright.sync_api import Page, expect
from config import settings
MULTI_SELECT_URL = settings.BASE_URL + "/multi-select"

def test_ms_001_native_select_single_option(page: Page):
    """MS_001: Select a single option from a native multi-select.

    Expected: Only the selected option is highlighted; selectedOptions.length === 1.

    Steps:
    1. Navigate to /practice/multi-select.
    2. Locate [data-testid="ms-native-select"].
    3. Call selectOption('playwright').
    4. Assert selectedOptions contains only "Playwright".
    """
    page.goto(MULTI_SELECT_URL)
    options = page.get_by_test_id('scenario-ms-single').locator('[data-testid="ms-native-select"]')
    options.select_option(value='playwright')
    expect(options).to_have_value('playwright')
    


def test_ms_002_native_select_multiple_options(page: Page):
    """MS_002: Select multiple options simultaneously from native multi-select.

    Expected: Both selected options are highlighted; selectedOptions.length === 2.

    Steps:
    1. Navigate to /practice/multi-select.
    2. Locate [data-testid="ms-native-select"].
    3. Call selectOption(['playwright', 'cypress']).
    4. Assert selectedOptions contains "Playwright" and "Cypress".
    """
    page.goto(MULTI_SELECT_URL)
    options = page.get_by_test_id('scenario-ms-multi').locator('[data-testid="ms-native-select"]')
    options.select_option(value=['playwright', 'cypress'])
    expect(options).to_have_values(['playwright', 'cypress'])


def test_ms_004_native_select_deselect_option(page: Page):
    """MS_004: Deselect a specific option while keeping others selected.

    Expected: Deselected option is no longer highlighted; others remain selected.

    Steps:
    1. Navigate to /practice/multi-select.
    2. Click [data-testid="ms-deselect-trigger"] to pre-select all options.
    3. Deselect "selenium" by calling selectOption with remaining values only.
    4. Assert "Selenium" is not in selectedOptions.
    """
    page.goto(MULTI_SELECT_URL)

    page.get_by_test_id('ms-deselect-trigger').click()
    native_select = page.get_by_test_id('scenario-ms-deselect').locator('[data-testid="ms-native-select"]')

    native_select.select_option(value=['playwright', 'cypress', 'webdriverio'])
    expect(native_select).to_have_values(['playwright', 'cypress', 'webdriverio'])


def test_ms_006_custom_select_open_and_choose(page: Page):
    """MS_006: Open custom checkbox multi-select and select an option.

    Expected: Option is checked; selected count label updates.

    Steps:
    1. Navigate to /practice/multi-select.
    2. Click [data-testid="ms-custom-trigger"].
    3. Assert dropdown panel is visible: [data-testid="ms-custom-panel"].
    4. Click [data-testid="ms-custom-option"][data-value="react"].
    5. Assert option has aria-selected="true".
    """
    page.goto(MULTI_SELECT_URL)

    trigger = page.get_by_test_id('scenario-ms-custom').locator('[data-testid="ms-custom-trigger"]')
    trigger.click()
    expect(trigger).to_have_attribute('aria-expanded', 'true')
    panel = page.locator('[class="multi-select-module__ep-fQa__customPanel"]')
    expect(panel).to_be_visible()

    react_option = panel.locator('[role="option"][data-value="react"]')
    react_option.click()
    expect(react_option).to_have_attribute('aria-selected', 'true')


def test_ms_007_custom_select_close_on_outside_click(page: Page):
    """MS_007: Close custom dropdown by clicking outside.

    Expected: Panel is hidden after clicking outside the trigger area.

    Steps:
    1. Navigate to /practice/multi-select.
    2. Open the custom dropdown via the trigger.
    3. Click outside the panel (e.g., the page heading).
    4. Assert [data-testid="ms-custom-panel"] is not visible.
    """
    page.goto(MULTI_SELECT_URL)

    trigger = page.get_by_test_id('scenario-ms-custom').locator('[data-testid="ms-custom-trigger"]')
    trigger.click()
    expect(trigger).to_have_attribute('aria-expanded', 'true')
    panel = page.locator('[class="multi-select-module__ep-fQa__customPanel"]')
    expect(panel).to_be_visible()

    page.get_by_test_id('page-header').click()
    expect(panel).not_to_be_visible()


def test_ms_008_custom_select_select_all(page: Page):
    """MS_008: Use Select All button to check all custom options.

    Expected: All options gain aria-selected=true; count label shows full count.

    Steps:
    1. Navigate to /practice/multi-select.
    2. Open the custom multi-select panel.
    3. Click [data-testid="ms-select-all-btn"].
    4. Assert all [data-testid="ms-custom-option"] elements have aria-selected="true".
    """
    page.goto(MULTI_SELECT_URL)

    scenario = page.get_by_test_id('scenario-ms-select-all')
    scenario.get_by_test_id('ms-custom-trigger').click()

    panel = page.locator('[class="multi-select-module__ep-fQa__customPanel"]')
    expect(panel).to_be_visible()

    panel.get_by_test_id('ms-select-all-btn').click()
    all_options = panel.locator('[data-testid="ms-custom-option"]')
    selected_options = panel.locator('[data-testid="ms-custom-option"][aria-selected="true"]')
    expect(selected_options).to_have_count(all_options.count())


def test_ms_009_custom_select_clear_all(page: Page):
    """MS_009: Use Clear All button to deselect every custom option.

    Expected: All options lose aria-selected; count label resets to 0.

    Steps:
    1. Navigate to /practice/multi-select.
    2. Select all options via Select All button.
    3. Click [data-testid="ms-clear-all-btn"].
    4. Assert no option has aria-selected="true".
    """
    page.goto(MULTI_SELECT_URL)

    scenario = page.get_by_test_id('scenario-ms-select-all')
    scenario.get_by_test_id('ms-custom-trigger').click()

    panel = page.locator('[class="multi-select-module__ep-fQa__customPanel"]')
    panel.get_by_test_id('ms-select-all-btn').click()
    panel.get_by_test_id('ms-clear-all-btn').click()

    selected_options = panel.locator('[data-testid="ms-custom-option"][aria-selected="true"]')
    expect(selected_options).to_have_count(0)


def test_ms_010_remove_tag_by_child_button(page: Page):
    """MS_010: Remove a tag by clicking its close button (no data-testid on button).

    Expected: The removed tag no longer appears in the tag list.

    Steps:
    1. Navigate to /practice/multi-select.
    2. Pre-select tags using the tag scenario controls.
    3. Locate [data-tag-value="javascript"] inside [data-testid="ms-tag-list"].
    4. Click its child button using getByRole('button') or XPath //li[@data-tag-value="javascript"]//button.
    5. Assert the tag is no longer in the DOM.
    """
    page.goto(MULTI_SELECT_URL)

    tag_list = page.get_by_test_id('ms-tag-list')
    javascript_tag = tag_list.locator('[data-tag-value="javascript"]')
    expect(javascript_tag).to_be_visible()

    javascript_tag.get_by_role('button').click()
    expect(tag_list.locator('[data-tag-value="javascript"]')).to_have_count(0)


def test_ms_011_searchable_select_filter_options(page: Page):
    """MS_011: Filter options in searchable multi-select by typing.

    Expected: Only matching options appear in the results listbox.

    Steps:
    1. Navigate to /practice/multi-select.
    2. Fill [data-testid="ms-search-input"] with "vue".
    3. Assert [data-testid="ms-search-results"] contains exactly one option.
    4. Assert that option is "Vue.js".
    """
    page.goto(MULTI_SELECT_URL)

    search_input = page.get_by_test_id('ms-search-input')
    search_input.fill('vue')

    search_results = page.get_by_test_id('ms-search-results')
    matching_options = search_results.get_by_role('option')
    expect(matching_options).to_have_count(1)
    expect(matching_options.first).to_contain_text('Vue.js')


def test_ms_014_native_optgroup_selection(page: Page):
    """MS_014: Select an option from a grouped optgroup in native multi-select.

    Expected: Option from the specified group is selected.

    Steps:
    1. Navigate to /practice/multi-select.
    2. Locate [data-testid="ms-grouped-select"].
    3. Use XPath: //select[@data-testid="ms-grouped-select"]//optgroup[@label="Backend"]//option[@value="node"].
    4. Assert the option "Node.js" is selected.
    """
    page.goto(MULTI_SELECT_URL)

    grouped_select = page.get_by_test_id('ms-grouped-select')
    grouped_select.select_option(value='node')

    expect(grouped_select).to_have_value('node')