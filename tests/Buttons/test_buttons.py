from playwright.sync_api import Page, expect
from config import settings

BUTTONS_URL = settings.BASE_URL + "/buttons"

def test_btn_001_button_clickable_triggers_action(page: Page) -> None:
    """BTN_001: Button is clickable and triggers its action.

    Steps:
    1. Navigate to BUTTONS_URL.
    2. Locate [data-testid="btn-navigate-home"].
    3. Call click().
    4. Assert [data-testid="result-s01"] contains "Home".
    """
    page.goto(BUTTONS_URL)
    locate_button = page.locator('[data-testid="btn-navigate-home"]')
    locate_button.click()
    expect(page.locator('[data-testid="result-s01"]')).to_contain_text("Home")


def test_btn_002_button_displays_correct_label_text(page: Page) -> None:
    """BTN_002: Button displays the correct label text.

    Steps:
    1. Locate [data-testid="btn-navigate-home"].
    2. Read text via text_content().
    3. Assert trimmed text equals "Go To Home".
    """
    page.goto(BUTTONS_URL)
    btn_home = page.locator('[data-testid="btn-navigate-home"]')
    btn_home_text = btn_home.text_content().strip()
    assert btn_home_text == "Go To Home", f"Expected 'Go To Home', but got '{btn_home_text}'"


def test_btn_003_single_click_triggers_correct_action(page: Page) -> None:
    """BTN_003: Single click triggers the correct action.

    Steps:
    1. Click [data-testid="btn-get-coordinates"].
    2. Assert [data-testid="result-s02"] shows X/Y values.
    3. Assert unrelated results were not modified.
    """
    page.goto(BUTTONS_URL)
    btn_coordinates = page.locator('[data-testid="btn-get-coordinates"]')
    btn_coordinates.click()
    cordinates_result = page.locator('[data-testid="result-s02"]')
    cordinates_text = cordinates_result.text_content().strip()
    assert "X:" in cordinates_text and "Y:" in cordinates_text, f"Expected X/Y values in result, but got '{cordinates_text}'"


def test_btn_004_double_click_button_triggers_action(page: Page) -> None:
    """BTN_004: Double-click button triggers a double-click action.

    Steps:
    1. Locate [data-testid="btn-double-click"].
    2. Perform dblclick().
    3. Assert [data-testid="result-s07"] reads "Double clicked!".
    """
    page.goto(BUTTONS_URL)
    btn_double_click = page.locator('[data-testid="btn-double-click"]')
    btn_double_click.dblclick()
    result_text = page.locator('[data-testid="result-s07"]')
    expect(result_text).to_have_text("Double clicked!")


def test_btn_005_right_click_button_opens_context_action(page: Page) -> None:
    """BTN_005: Right-click button opens the context action.

    Steps:
    1. Locate [data-testid="btn-right-click"].
    2. Perform click(button='right').
    3. Assert [data-testid="result-s08"] confirms context action.
    """
    page.goto(BUTTONS_URL)
    btn_right_click = page.locator('[data-testid="btn-right-click"]')
    btn_right_click.click(button='right')
    result_text = page.locator('[data-testid="result-s08"]')
    expect(result_text).to_have_text("Context menu triggered!")


def test_btn_006_disabled_button_cannot_be_clicked(page: Page) -> None:
    """BTN_006: Disabled button cannot be clicked.

    Steps:
    1. Locate [data-testid="btn-disabled"].
    2. Assert is_enabled() is False or to_be_disabled() passes.
    3. Confirm result area stays at initial text.
    """
    page.goto(BUTTONS_URL)
    btn_disabled = page.locator('[data-testid="btn-disabled"]')
    expect(btn_disabled).to_be_disabled()
    result_text = page.locator('[data-testid="result-s05"]')
    expect(result_text).to_have_text("Button is disabled — no action fires")
    

def test_btn_007_enabled_button_reports_enabled_state(page: Page) -> None:
    """BTN_007: Enabled button reports an enabled state.

    Steps:
    1. Locate [data-testid="btn-navigate-home"].
    2. Assert is_enabled() returns True.
    3. Assert the disabled attribute is absent.
    """
    page.goto(BUTTONS_URL)
    btn_home = page.locator('[data-testid="btn-navigate-home"]')
    expect(btn_home).to_be_enabled()
    assert not btn_home.get_attribute("disabled")


def test_btn_008_button_stays_usable_across_viewport_sizes(page: Page) -> None:
    """BTN_008: Button stays usable across viewport sizes.

    Steps:
    1. Set viewport to 375x667 and assert visible and clickable.
    2. Set viewport to 1440x900 and re-assert.
    """
    page.goto(BUTTONS_URL)
    btn_home = page.locator('[data-testid="btn-navigate-home"]')

    # Test mobile viewport
    page.set_viewport_size({"width": 375, "height": 667})
    expect(btn_home).to_be_visible()
    expect(btn_home).to_be_enabled()

    # Test desktop viewport
    page.set_viewport_size({"width": 1440, "height": 900})
    expect(btn_home).to_be_visible()
    expect(btn_home).to_be_enabled()

def test_btn_009_button_operable_via_keyboard(page: Page) -> None:
    """BTN_009: Button is operable via keyboard.

    Steps:
    1. Focus the button via focus().
    2. Press Enter.
    3. Assert the same action fires as a mouse click.
    """
    page.goto(BUTTONS_URL)
    btn_home = page.locator('[data-testid="btn-navigate-home"]')

    btn_home.focus()
    page.keyboard.press("Enter")
    expect(page.locator('[data-testid="result-s01"]')).to_contain_text("Home")
    


def test_btn_010_button_exposed_to_screen_readers(page: Page) -> None:
    """BTN_010: Button is exposed to screen readers.

    Steps:
    1. Inspect the accessibility tree via page.accessibility.snapshot().
    2. Assert the role resolves to button.
    3. Assert the accessible name is non-empty.
    """
    ##TODO: re-do this test
    page.goto(BUTTONS_URL)
    snapshot = page.accessibility.snapshot()
    button_node = next((node for node in snapshot['children'] if node.get('name') == 'Go To Home'), None)
    
    assert button_node is not None, "Button not found in accessibility tree"
    assert button_node.get('role') == 'button', f"Expected role 'button', but got '{button_node.get('role')}'"
    assert button_node.get('name'), "Accessible name is empty"


def test_btn_011_hover_state_visually_distinct(page: Page) -> None:
    """BTN_011: Hover state is visually distinct.

    Steps:
    1. Read background-color before hover.
    2. Perform hover().
    3. Read background-color after hover and assert the style changed.
    """
    page.goto(BUTTONS_URL)
    btn_home = page.locator('[data-testid="btn-get-coordinates"]')
    initial_bg_color = btn_home.evaluate("element => getComputedStyle(element).backgroundColor")
    btn_home.hover()
    hovered_bg_color = btn_home.evaluate("element => getComputedStyle(element).backgroundColor")
    assert initial_bg_color != hovered_bg_color, "Background color did not change on hover"


def test_btn_012_result_state_resets_after_page_refresh(page: Page) -> None:
    """BTN_012: Result state resets after a page refresh.

    Steps:
    1. Click the button and confirm the result changed.
    2. Reload the page via page.reload().
    3. Assert the result returns to its initial value.
    """
    page.goto(BUTTONS_URL)
    locate_button = page.locator('[data-testid="btn-navigate-home"]')
    locate_button.click()
    expect(page.locator('[data-testid="result-s01"]')).to_contain_text("Home")
    page.reload()
    result_text_after_reload = page.locator('[data-testid="result-s01"]')
    assert result_text_after_reload.text_content().strip() == "No navigation yet", "Result did not reset after page reload"


def test_btn_013_click_and_hold_completes_after_time(page: Page) -> None:
    """BTN_013: Click-and-hold completes after 1.5 seconds.

    Steps:
    1. Press and hold [data-testid="btn-click-hold"] via mouse.down().
    2. Wait 1500 ms, then release via mouse.up().
    3. Assert [data-testid="result-s06"] confirms the completed hold.
    """
    page.goto(BUTTONS_URL)
    btn_click_hold = page.locator('[data-testid="btn-click-hold"]')
    btn_click_hold.hover()
    page.mouse.down()
    page.wait_for_timeout(1500)  # Wait for 1.5 seconds
    page.mouse.up()
    result_text = page.locator('[data-testid="result-s06"]')
    expect(result_text).to_have_text("Held for 1.5s")


def test_btn_014_button_does_not_overlap_adjacent_elements(page: Page) -> None:
    """BTN_014: Button does not overlap adjacent elements.

    Steps:
    1. Read the button bounding_box().
    2. Read the neighboring element bounding_box().
    3. Assert the two rectangles do not intersect.
    """
    page.goto(BUTTONS_URL)
    btn_home = page.locator('[data-testid="btn-navigate-home"]')
    adjacent_element = page.locator('[data-testid="result-s01"]')

    btn_box = btn_home.bounding_box()
    adjacent_box = adjacent_element.bounding_box()

    assert btn_box is not None and adjacent_box is not None, "Bounding boxes could not be retrieved"

    
    overlap = not (btn_box['x'] + btn_box['width'] < adjacent_box['x'] or
                   adjacent_box['x'] + adjacent_box['width'] < btn_box['x'] or
                   btn_box['y'] + btn_box['height'] < adjacent_box['y'] or
                   adjacent_box['y'] + adjacent_box['height'] < btn_box['y'])

    assert not overlap, "Button overlaps with adjacent element"


def test_btn_015_page_loads_without_console_errors(page: Page) -> None:
    """BTN_015: Page loads without console errors.

    Steps:
    1. Attach listeners to console and pageerror events.
    2. Navigate to BUTTONS_URL.
    3. Assert no error-level messages were captured.
    """
    console_errors = []
    page_errors = []

    def handle_console(msg):
        if msg.type == "error":
            console_errors.append(msg.text)

    def handle_page_error(exception):
        page_errors.append(str(exception))

    page.on("console", handle_console)
    page.on("pageerror", handle_page_error)

    page.goto(BUTTONS_URL)

    assert not console_errors, f"Console errors found: {console_errors}"
    assert not page_errors, f"Page errors found: {page_errors}"