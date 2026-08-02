
from playwright.sync_api import Page, expect
from config import settings

INPUT_FIELDS_URL = settings.BASE_URL + "/input-fields"


def test_inp_001_text_can_be_typed_into_an_input_field(page: Page):
    """INP_001: Text can be typed into an input field.

    Steps:
    1. Navigate to /practice/input-fields.
    2. Locate [data-testid="input-movie-name"].
    3. Type "Interstellar" via fill() or send_keys().
    4. Assert input_value() equals "Interstellar".
    """
    page.goto(INPUT_FIELDS_URL)

    # Locate the input field using a selector (e.g., by ID, class, or name)
    input_field = page.locator("id=movieNameInput")

    # Type text into the input field
    input_field.fill("Avengers: Endgame")

    # Assert that the input field contains the expected value
    expect(input_field).to_have_value("Avengers: Endgame")

    # Clear the input field
    input_field.fill("")

    # Assert that the input field is empty
    expect(input_field).to_have_value("")


def test_inp_002_submitting_typed_value_updates_result(page: Page):
    """INP_002: Submitting the typed value updates the result.

    Steps:
    1. Type a value into [data-testid="input-movie-name"].
    2. Click [data-testid="btn-submit-movie"].
    3. Assert [data-testid="result-s01"] contains the typed value.
    """
    page.goto(INPUT_FIELDS_URL)

    input_field = page.locator("id=movieNameInput")

    # Type text into the input field
    input_field.fill("Avengers: Endgame")

    submit_button = page.locator("id=submitMovieBtn")

    submit_button.click()

    result_text = page.locator("id=result-s01")

    expect(result_text).to_have_text("You entered: Avengers: Endgame")


def test_inp_003_placeholder_replaced_when_text_entered(page: Page):
    """INP_003: Placeholder is replaced when text is entered.

    Steps:
    1. Read the placeholder attribute on [data-testid="input-movie-name"].
    2. Type any text into the field.
    3. Assert the field value is non-empty.
    """
    page.goto(INPUT_FIELDS_URL)

    input_field = page.locator("id=movieNameInput")

    expect(input_field).to_have_attribute("placeholder", "Enter a movie name…")

    input_field.fill("Avengers: Endgame")

    expect(input_field).not_to_be_empty()


def test_inp_004_text_appended_to_existing_content(page: Page):
    """INP_004: Text is appended to existing content.

    Steps:
    1. Locate [data-testid="input-append"] pre-filled with "Avengers".
    2. Click into the field and type "Endgame".
    3. Press Tab to blur the field.
    4. Assert [data-testid="result-s02"] shows "Avengers Endgame".
    """
    page.goto(INPUT_FIELDS_URL)
    
    input_field = page.locator("id=appendInput")
    #Playwright's fill() clears first — use click() + press_sequentially() to append
    input_field.click()
    input_field.press_sequentially(" Endgame")

    expect(input_field).to_have_value("Avengers Endgame")



def test_inp_005_tab_moves_focus_away_from_field(page: Page):
    """INP_005: Tab moves focus away from the field.

    Steps:
    1. Focus [data-testid="input-append"].
    2. Press Tab.
    3. Assert the input is no longer focused.
    """
    page.goto(INPUT_FIELDS_URL)

    input_field = page.locator("id=appendInput")
    input_field.focus()

    expect(input_field).to_be_focused()

    page.keyboard.press("Tab")
    expect(input_field).not_to_be_focused()


def test_inp_006_current_field_value_can_be_read(page: Page):
    """INP_006: Current field value can be read.

    Steps:
    1. Locate [data-testid="input-read-value"].
    2. Click [data-testid="btn-read-value"].
    3. Assert [data-testid="result-s03"] shows the field value.
    """
    
    page.goto(INPUT_FIELDS_URL)

    read_value_input = page.locator("id=readValueInput")
    value = read_value_input.input_value()
    read_value_input_button = page.locator("id=readValueBtn")
    read_value_input_button.click()

    text_value = page.locator("id=result-s03")

    expect(text_value).to_contain_text(value)


def test_inp_007_populated_field_can_be_cleared(page: Page):
    """INP_007: A populated field can be cleared.

    Steps:
    1. Locate [data-testid="input-clear"] pre-filled with "Inception".
    2. Click [data-testid="btn-clear-field"] or clear via fill("").
    3. Assert input_value() is empty and [data-testid="result-s04"] confirms it.
    """
    page.goto(INPUT_FIELDS_URL)

    clearable_input_field = page.locator("id=clearInput")
    
    clearable_input_field.fill("")

    # Assert that the input field contains the expected value
    expect(clearable_input_field).to_have_value("")

    # Assert that the input field is empty after clearing
    expect(clearable_input_field).to_have_value("")


def test_inp_008_disabled_input_rejects_keyboard_input(page: Page):
    """INP_008: Disabled input rejects keyboard input.

    Steps:
    1. Locate [data-testid="input-disabled"].
    2. Assert is_enabled() is False or to_be_disabled() passes.
    3. Confirm typing does not change the value.
    """

    page.goto(INPUT_FIELDS_URL)
    disabled_input_field = page.locator("id=disabledInput")

    expect(disabled_input_field).to_be_disabled()


def test_inp_009_readonly_input_cannot_be_edited(page: Page):
    """INP_009: Readonly input cannot be edited.

    Steps:
    1. Locate [data-testid="input-readonly"].
    2. Assert the readonly attribute is present.
    3. Attempt to type and confirm the value stays unchanged.
    """
    page.goto(INPUT_FIELDS_URL)
    readonly_input_field = page.locator("id=readonlyInput")

    expect(readonly_input_field).to_have_attribute("readonly", "")
    value = readonly_input_field.input_value()
    readonly_input_field.focus()
    page.keyboard.type("Attempted New Input")

    # Assert the value remains strictly equal to the original value
    expect(readonly_input_field).to_have_value(value)  # Assert the value remains unchanged


def test_inp_010_readonly_value_is_still_readable(page: Page):
    """INP_010: Readonly value is still readable.

    Steps:
    1. Locate [data-testid="input-readonly"].
    2. Read get_attribute("value") or input_value().
    3. Assert the returned value is non-empty.
    """
    page.goto(INPUT_FIELDS_URL)
    readonly_input_field = page.locator("id=readonlyInput")
    
    value = readonly_input_field.input_value()
    
    
    
    expect(readonly_input_field).not_to_be_empty()


def test_inp_011_field_handles_long_string_without_truncation(page: Page):
    """INP_011: Field handles a long string without truncation.

    Steps:
    1. Type a 200-character string into [data-testid="input-movie-name"].
    2. Read the value back.
    3. Assert the value length matches the input length.
    """
    page.goto(INPUT_FIELDS_URL)
    long_string = "A" * 200
    
    # Step 1: Type a 200-character string into [data-testid="input-movie-name"]
    movie_input = page.locator('id=movieNameInput')
    movie_input.fill(long_string)
    
    # Step 2: Read the value back
    actual_value = movie_input.input_value()
    
    # Step 3: Assert the value length matches the input length
    assert len(actual_value) == 200
    
    # Additional verification using Playwright's expect assertion
    expect(movie_input).to_have_value(long_string)


def test_inp_012_field_state_resets_after_page_refresh(page: Page):
    """INP_012: Field state resets after a page refresh.

    Steps:
    1. Type into a field and confirm the value changed.
    2. Reload the page.
    3. Assert the field returns to its initial value.
    """
    page.goto(INPUT_FIELDS_URL)

    input_field = page.locator("id=movieNameInput")
    test_text = "Avengers: Endgame"
    input_field.fill(test_text)
    expect(input_field).to_have_value(test_text)
    # Refresh the page
    page.reload()

    # After refresh, the input field should be empty
    expect(input_field).to_have_value("")

