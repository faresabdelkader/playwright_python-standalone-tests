from playwright.sync_api import Page, expect
from config import settings

DROPDOWNS_URL = settings.BASE_URL + "/dropdowns"


def test_dd_001_select_apple_from_the_fruit_dropdown_by_visible_text(page: Page):
    """DD_001: Select Apple from the fruit dropdown by visible text

    Expected: Fruit select value is apple and the result confirms Apple

    Steps:
    1. Navigate to /practice/dropdowns
    2. Locate [data-testid="fruit-select"] or #fruitSelect
    3. Select the option with label Apple
    4. Assert [data-testid="result-s01"] contains Apple
    """
    page.goto(DROPDOWNS_URL)
    page.select_option('[data-testid="fruit-select"]', label='Apple')
    expect(page.locator('[data-testid="result-s01"]')).to_contain_text('Selected fruit: Apple')


def test_dd_002_verify_fruit_dropdown_placeholder_before_selection(page: Page):
    """DD_002: Verify fruit dropdown placeholder before selection

    Expected: Default option is selected and has an empty value

    Steps:
    1. Locate #fruitSelect
    2. Assert the current value equals an empty string
    3. Assert the visible selected option is Select Fruit
    """
    page.goto(DROPDOWNS_URL)
    fruit_select = page.locator('#fruitSelect')
    expect(fruit_select).to_have_value('')
    expect(page.locator('#fruitSelect option:checked')).to_have_text('Select Fruit')


def test_dd_003_select_india_from_the_country_dropdown_by_value(page: Page):
    """DD_003: Select India from the country dropdown by value

    Expected: Country select value is india and visible text is India

    Steps:
    1. Locate [data-testid="country-select"]
    2. Select by value india
    3. Assert the selected option text is India
    """
    page.goto(DROPDOWNS_URL)
    page.select_option('[data-testid="country-select"]', value='india')
    expect(page.locator('[data-testid="country-select"] option:checked')).to_have_text('India')


def test_dd_004_verify_the_country_dropdown_option_count(page: Page):
    """DD_004: Verify the country dropdown option count

    Expected: Country dropdown contains five options including placeholder

    Steps:
    1. Locate #countrySelect option
    2. Read all option elements
    3. Assert the count equals 5
    """
    page.goto(DROPDOWNS_URL)
    options = page.locator('#countrySelect option')
    expect(options).to_have_count(5)


def test_dd_005_select_the_last_programming_language_option(page: Page):
    """DD_005: Select the last programming language option

    Expected: Language select value is typescript

    Steps:
    1. Locate [data-testid="language-select"]
    2. Read all language options and choose the last option
    3. Assert [data-testid="result-s03"] mentions TypeScript
    """
    page.goto(DROPDOWNS_URL)
    select_elem = page.locator('[data-testid="language-select"]')
    last_value = select_elem.locator('option').last.get_attribute('value')
    page.select_option('[data-testid="language-select"]', value=last_value)
    expect(page.locator('[data-testid="result-s03"]')).to_contain_text('TypeScript')


def test_dd_006_read_all_programming_language_option_labels(page: Page):
    """DD_006: Read all programming language option labels

    Expected: All labels are available in the expected order

    Steps:
    1. Locate #languageSelect option
    2. Read text content for each option
    3. Assert the list includes Python, Java, JavaScript, and TypeScript
    """
    page.goto(DROPDOWNS_URL)
    expect(page.locator('#languageSelect option')).to_contain_text(['Python', 'Java', 'JavaScript', 'TypeScript'])

def test_dd_007_select_multiple_superheroes_in_a_native_multi_select(page: Page):
    """DD_007: Select multiple superheroes in a native multi-select

    Expected: Batman and Aquaman are selected together

    Steps:
    1. Locate [data-testid="hero-select"]
    2. Select Batman and Aquaman
    3. Assert two option:checked elements exist
    """
    page.goto(DROPDOWNS_URL)
    page.select_option('[data-testid="hero-select"]', label=['Batman', 'Aquaman'])
    checked_options = page.locator('[data-testid="hero-select"] option:checked')
    expect(checked_options).to_have_count(2)


def test_dd_008_deselect_a_selected_superhero(page: Page):
    """DD_008: Deselect a selected superhero

    Expected: Only the remaining selected hero stays checked

    Steps:
    1. Select Batman and Aquaman
    2. Change the selected values to only batman
    3. Assert Aquaman is no longer selected
    """
    page.goto(DROPDOWNS_URL)
    page.select_option('[data-testid="hero-select"]', label=['Batman', 'Aquaman'])
    page.select_option('[data-testid="hero-select"]', label=['Batman'])
    aquaman_option = page.locator('[data-testid="hero-select"] option[value="aquaman"]')
    expect(aquaman_option).not_to_be_checked()


def test_dd_009_open_the_custom_priority_dropdown_by_role(page: Page):
    """DD_009: Open the custom priority dropdown by role

    Expected: The listbox appears with three priority options

    Steps:
    1. Locate the button with role button and name Choose priority
    2. Click the trigger
    3. Assert a listbox is visible
    """
    page.goto(DROPDOWNS_URL)
    trigger = page.locator('[data-testid="priority-dropdown-trigger"]')
    trigger.click()
    listbox = page.locator('[data-testid="priority-dropdown-list"]')
    expect(listbox).to_be_visible()


def test_dd_010_choose_high_priority_from_the_custom_dropdown(page: Page):
    """DD_010: Choose High Priority from the custom dropdown

    Expected: Trigger text and result update to High Priority

    Steps:
    1. Click [data-testid="priority-dropdown-trigger"]
    2. Within the priority listbox, click the option named High Priority
    3. Assert [data-testid="result-s05"] confirms the selected priority
    """
    page.goto(DROPDOWNS_URL)
    page.click('[data-testid="priority-dropdown-trigger"]')
    listbox = page.locator('[data-testid="priority-dropdown-list"]')
    listbox.get_by_role('option', name='High Priority').click()
    expect(page.locator('[data-testid="result-s05"]')).to_contain_text('High Priority')


def test_dd_011_locate_custom_dropdown_option_with_a_scoped_data_attribute(page: Page):
    """DD_011: Locate custom dropdown option with a scoped data attribute

    Expected: The correct repeated option is clicked without relying on index

    Steps:
    1. Open [data-testid="priority-dropdown-trigger"]
    2. Scope to [data-testid="priority-dropdown-list"]
    3. Click [role="option"][data-priority-id="priority-high"]
    """
    page.goto(DROPDOWNS_URL)
    page.click('[data-testid="priority-dropdown-trigger"]')
    dropdown_list = page.locator('[data-testid="priority-dropdown-list"]')
    dropdown_list.locator('[role="option"][data-priority-id="priority-high"]').click()


def test_dd_012_search_city_combobox_filters_options(page: Page):
    """DD_012: Search city combobox filters options

    Expected: Typing Pun shows Pune as a selectable option

    Steps:
    1. Locate [data-testid="city-combobox"]
    2. Fill the combobox with Pun
    3. Assert the option named Pune is visible
    """
    page.goto(DROPDOWNS_URL)
    combobox_input = page.locator('[data-testid="city-combobox"] input')
    if combobox_input.count() == 0:
        combobox_input = page.locator('[data-testid="city-combobox"]')
    combobox_input.fill('Pun')
    pune_option = page.get_by_role('option', name='Pune')
    expect(pune_option).to_be_visible()


def test_dd_013_select_a_city_using_a_dynamic_city_id(page: Page):
    """DD_013: Select a city using a dynamic city id

    Expected: City result confirms Pune with city-pune as the business id

    Steps:
    1. Fill the City combobox with Pu
    2. Locate [role="option"][data-city-id="city-pune"]
    3. Click the option and assert the result mentions Pune
    """
    page.goto(DROPDOWNS_URL)
    combobox_input = page.locator('[data-testid="city-combobox"] input')
    if combobox_input.count() == 0:
        combobox_input = page.locator('[data-testid="city-combobox"]')
    combobox_input.fill('Pu')
    option = page.locator('[role="option"][data-city-id="city-pune"]')
    option.click()
    expect(page.locator('[data-testid="result-s06"]')).to_contain_text('Pune')


def test_dd_014_use_xpath_sibling_traversal_for_the_city_combobox(page: Page):
    """DD_014: Use XPath sibling traversal for the City combobox

    Expected: The input is found from the nearby City label

    Steps:
    1. Use XPath //label[normalize-space()="City"]/following-sibling::div//input
    2. Fill the located combobox with Mum
    3. Select Mumbai and assert the result
    """
    page.goto(DROPDOWNS_URL)
    input_elem = page.locator('xpath=//label[normalize-space()="City"]/following-sibling::div//input')
    input_elem.fill('Mum')
    mumbai_option = page.get_by_role('option', name='Mumbai')
    mumbai_option.click()
    expect(page.locator('[data-testid="result-s06"]')).to_contain_text('Mumbai')
