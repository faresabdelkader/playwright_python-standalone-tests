# Buttons Test Cases

This file documents the test intent and steps for the button test suite.

## BTN_001: Button is clickable and triggers its action
1. Navigate to `BUTTONS_URL`
2. Locate `[data-testid="btn-navigate-home"]`
3. Call `click()`
4. Assert `[data-testid="result-s01"]` contains `Home`

## BTN_002: Button displays the correct label text
1. Locate `[data-testid="btn-navigate-home"]`
2. Read text via `text_content()`
3. Assert trimmed text equals `Go To Home`

## BTN_003: Single click triggers the correct action
1. Click `[data-testid="btn-get-coordinates"]`
2. Assert `[data-testid="result-s02"]` shows X/Y values
3. Assert unrelated results were not modified

## BTN_004: Double-click button triggers a double-click action
1. Locate `[data-testid="btn-double-click"]`
2. Perform `dblclick()`
3. Assert `[data-testid="result-s07"]` reads `Double clicked!`

## BTN_005: Right-click button opens the context action
1. Locate `[data-testid="btn-right-click"]`
2. Perform `click(button='right')`
3. Assert `[data-testid="result-s08"]` confirms context action

## BTN_006: Disabled button cannot be clicked
1. Locate `[data-testid="btn-disabled"]`
2. Assert `is_enabled()` is False or `to_be_disabled()` passes
3. Confirm result area stays at initial text

## BTN_007: Enabled button reports an enabled state
1. Locate `[data-testid="btn-navigate-home"]`
2. Assert `is_enabled()` returns True
3. Assert `disabled` attribute is absent

## BTN_008: Button stays usable across viewport sizes
1. Set viewport to 375x667 (mobile) and assert visible/clickable
2. Set viewport to 1440x900 (desktop) and re-assert

## BTN_009: Button is operable via keyboard
1. Focus button via `focus()`
2. Press `Enter`
3. Assert same action fires as mouse click

## BTN_010: Button is exposed to screen readers
1. Inspect element accessibility tree via `page.accessibility.snapshot()`
2. Assert role resolves to `button`
3. Assert accessible name is non-empty

## BTN_011: Hover state is visually distinct
1. Read `background-color` before hover
2. Perform `hover()`
3. Read `background-color` after hover and assert style changed

## BTN_012: Result state resets after a page refresh
1. Click button and confirm result changed
2. Reload page via `page.reload()`
3. Assert result returns to initial value

## BTN_013: Click-and-hold completes after 1.5 seconds
1. Press and hold `[data-testid="btn-click-hold"]` via `mouse.down()`
2. Wait 1500ms, then release via `mouse.up()`
3. Assert `[data-testid="result-s06"]` confirms completed hold

## BTN_014: Button does not overlap adjacent elements
1. Read button `bounding_box()`
2. Read neighboring element `bounding_box()`
3. Assert the two rectangles do not intersect

## BTN_015: Page loads without console errors
1. Attach listeners to `console` and `pageerror` events
2. Navigate to `BUTTONS_URL`
3. Assert no error-level messages were captured
