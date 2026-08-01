
from playwright.sync_api import Page, expect
from config import settings

INPUT_FIELDS_URL = settings.BASE_URL + "/input-fields"


def test_inp_001_text_can_be_typed_into_an_input_field(page: Page):
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
    page.goto(INPUT_FIELDS_URL)

    input_field = page.locator("id=movieNameInput")

    # Type text into the input field
    input_field.fill("Avengers: Endgame")

    submit_button = page.locator("id=submitMovieBtn")

    submit_button.click()

    result_text = page.locator("id=result-s01")

    expect(result_text).to_have_text("You entered: Avengers: Endgame")


def test_inp_003_placeholder_replaced_when_text_entered(page: Page):
    page.goto(INPUT_FIELDS_URL)

    input_field = page.locator("id=movieNameInput")

    expect(input_field).to_have_attribute("placeholder", "Enter a movie name…")

    input_field.fill("Avengers: Endgame")

    expect(input_field).not_to_be_empty()


def test_inp_004_text_appended_to_existing_content(page: Page):
    page.goto(INPUT_FIELDS_URL)
    
    input_field = page.locator("id=appendInput")
    #Playwright's fill() clears first — use click() + press_sequentially() to append
    input_field.click()
    input_field.press_sequentially(" Endgame")

    expect(input_field).to_have_value("Avengers Endgame")



def test_inp_005_tab_moves_focus_away_from_field(page: Page):
    page.goto(INPUT_FIELDS_URL)

    input_field = page.locator("id=appendInput")
    input_field.focus()

    expect(input_field).to_be_focused()

    page.keyboard.press("Tab")
    expect(input_field).not_to_be_focused()


def test_inp_006_current_field_value_can_be_read(page: Page):
    
    page.goto(INPUT_FIELDS_URL)

    read_value_input = page.locator("id=readValueInput")
    value = read_value_input.input_value()
    read_value_input_button = page.locator("id=readValueBtn")
    read_value_input_button.click()

    text_value = page.locator("id=result-s03")

    expect(text_value).to_contain_text(value)


def test_inp_007_populated_field_can_be_cleared(page: Page):
    page.goto(INPUT_FIELDS_URL)

    clearable_input_field = page.locator("id=clearInput")
    
    clearable_input_field.fill("")

    # Assert that the input field contains the expected value
    expect(clearable_input_field).to_have_value("")

    # Assert that the input field is empty after clearing
    expect(clearable_input_field).to_have_value("")


def test_inp_008_disabled_input_rejects_keyboard_input(page: Page):

    page.goto(INPUT_FIELDS_URL)
    disabled_input_field = page.locator("id=disabledInput")

    expect(disabled_input_field).to_be_disabled()


def test_inp_009_readonly_input_cannot_be_edited(page: Page):
    page.goto(INPUT_FIELDS_URL)
    readonly_input_field = page.locator("id=readonlyInput")

    expect(readonly_input_field).to_have_attribute("readonly", "")
    value = readonly_input_field.input_value()
    readonly_input_field.focus()
    page.keyboard.type("Attempted New Input")

    # Assert the value remains strictly equal to the original value
    expect(readonly_input_field).to_have_value(value)  # Assert the value remains unchanged


def test_inp_010_readonly_value_is_still_readable(page: Page):
    page.goto(INPUT_FIELDS_URL)
    readonly_input_field = page.locator("id=readonlyInput")
    
    value = readonly_input_field.input_value()
    
    
    
    expect(readonly_input_field).not_to_be_empty()


def test_inp_011_field_handles_long_string_without_truncation(page: Page):
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
    page.goto(INPUT_FIELDS_URL)

    input_field = page.locator("id=movieNameInput")
    test_text = "Avengers: Endgame"
    input_field.fill(test_text)
    expect(input_field).to_have_value(test_text)
    # Refresh the page
    page.reload()

    # After refresh, the input field should be empty
    expect(input_field).to_have_value("")

