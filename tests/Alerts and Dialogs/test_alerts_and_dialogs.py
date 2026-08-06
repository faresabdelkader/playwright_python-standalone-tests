from playwright.sync_api import Page, expect
from config import settings

ALERTS_AND_DIALOGS_URL = settings.BASE_URL + "/alerts-dialogs"

def test_ald_001_dialog_opens_on_trigger(page:Page):
    """ALD_001: Dialog opens after trigger button click.

    Expected: Dialog element is visible with role=dialog and aria-modal=true

    Steps:
    1. Navigate to /practice/alerts-dialogs
    2. Click [data-testid="open-info-dialog"]
    3. Assert [data-testid="info-alert-dialog"] is visible
    4. Assert the element has role="dialog" and aria-modal="true"
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-testid="open-info-dialog"]')
    page.locator('[data-testid="open-info-dialog"]').click()
    expect(page.locator('[data-testid="info-alert-dialog"]')).to_be_visible()
    expect(page.locator('[data-testid="info-alert-dialog"]')).to_have_attribute('role', 'dialog')
    expect(page.locator('[data-testid="info-alert-dialog"]')).to_have_attribute('aria-modal', 'true')


def test_ald_002_dialog_heading_title(page:Page):
    """ALD_002: Dialog heading matches expected title.

    Expected: Heading inside dialog reads "Session Notice" exactly

    Steps:
    1. Open the info dialog via [data-testid="open-info-dialog"]
    2. Assert getByRole("heading", { name: "Session Notice" }) is visible
    3. Verify the h2 element text matches exactly using toHaveText
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-testid="open-info-dialog"]')
    page.locator('[data-testid="open-info-dialog"]').click()
    expect(page.locator('[data-testid="info-alert-dialog"]')).to_be_visible()
    expect(page.locator('[data-testid="info-alert-dialog"]')).to_have_attribute('role', 'dialog')
    expect(page.locator('[data-testid="info-alert-dialog"]')).to_have_attribute('aria-modal', 'true')
    expect(page.locator('[data-testid="info-alert-dialog"] h2')).to_have_text('Session Notice')


def test_ald_003_close_button_dismisses_info_dialog(page:Page):
    """ALD_003: Close button dismisses the info dialog.

    Expected: Dialog disappears from the DOM after clicking the × button

    Steps:
    1. Open info dialog
    2. Click [data-testid="info-dialog-close-btn"]
    3. Assert dialog is no longer visible
    4. Assert [data-testid="result-s01"] confirms dismissal
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-testid="open-info-dialog"]')
    page.locator('[data-testid="open-info-dialog"]').click()
    expect(page.locator('[data-testid="info-alert-dialog"]')).to_be_visible()
    page.locator('[data-testid="info-dialog-close-btn"]').click()
    expect(page.locator('[data-testid="info-alert-dialog"]')).not_to_be_visible()
    expect(page.locator('[data-testid="result-s01"]')).to_have_text('Info dialog dismissed')


def test_ald_004_cancel_button_keeps_dialog_closed(page: Page):
    """ALD_004: Cancel button keeps dialog closed without triggering the action.

    Expected: Dialog closes and the confirm result is not updated

    Steps:
    1. Open confirm dialog via [data-testid="open-confirm-dialog"]
    2. Click [data-testid="confirm-cancel-btn"]
    3. Assert the dialog is no longer visible
    4. Assert [data-testid="result-s02"] still reads its initial value
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-testid="open-confirm-dialog"]')

    result = page.locator('[data-testid="result-s02"]')
    initial_result = result.text_content().strip()

    page.locator('[data-testid="open-confirm-dialog"]').click()
    confirm_dialog = page.locator('[data-testid="confirm-ok-btn"]')
    expect(confirm_dialog).to_be_visible()

    page.locator('[data-testid="confirm-cancel-btn"]').click()
    expect(confirm_dialog).not_to_be_visible()
    expect(result).to_have_text(initial_result)


def test_ald_005_confirm_button_triggers_action(page: Page):
    """ALD_005: Confirm button triggers the expected action and closes dialog.

    Expected: Result reads "Submission confirmed!" and dialog disappears

    Steps:
    1. Open confirm dialog via [data-testid="open-confirm-dialog"]
    2. Assert dialog is visible
    3. Click [data-testid="confirm-ok-btn"]
    4. Assert [data-testid="result-s02"] reads Submission confirmed!
    5. Assert dialog is no longer in the DOM
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-testid="open-confirm-dialog"]')

    page.locator('[data-testid="open-confirm-dialog"]').click()
    confirm_dialog = page.locator('[id="confirm-dialog-title"]')
    expect(confirm_dialog).to_be_visible()

    page.locator('[data-testid="confirm-ok-btn"]').click()
    expect(page.locator('[data-testid="result-s02"]')).to_have_text('Submission confirmed!')
    expect(confirm_dialog).not_to_be_visible()


def test_ald_006_destructive_confirm_via_aria_label(page: Page):
    """ALD_006: Destructive confirm button located by aria-label (no data-testid).

    Expected: Result reads "Account deleted!" after clicking the danger button

    Steps:
    1. Open delete dialog via [data-testid="open-delete-dialog"]
    2. Scope into [data-testid='delete-account-dialog']
    3. Locate the button by [aria-label="Confirm account deletion"]
    4. Click it and assert result is updated
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-testid="open-delete-dialog"]')

    page.locator('[data-testid="open-delete-dialog"]').click()
    delete_dialog = page.locator('[data-testid="delete-account-dialog"]')
    expect(delete_dialog).to_be_visible()

    delete_dialog.locator('[aria-label="Confirm account deletion"]').click()
    expect(delete_dialog).not_to_be_visible()
    expect(page.locator('[data-testid^="result-s"]').filter(has_text='Account deleted!')).to_be_visible()


def test_ald_007_backdrop_click_closes_modal(page: Page):
    """ALD_007: Backdrop click closes the modal dialog.

    Expected: Dialog closes when clicking the overlay behind the dialog box

    Steps:
    1. Open backdrop dialog via [data-testid="open-backdrop-dialog"]
    2. Click [data-testid="backdrop-dismiss-dialog"] at { position: { x: 5, y: 5 } }
    3. Assert dialog is no longer visible
    4. Assert [data-testid="result-s05"] confirms backdrop close
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-testid="open-backdrop-dialog"]')

    page.locator('[data-testid="open-backdrop-dialog"]').click()
    backdrop_dialog = page.locator('[data-testid="backdrop-dismiss-dialog"]')
    expect(backdrop_dialog).to_be_visible()

    backdrop_dialog.click(position={"x": 150, "y": 150})
    expect(backdrop_dialog).not_to_be_visible()
    expect(page.locator('[data-testid="result-s05"]')).to_have_text('Dialog closed via backdrop')


def test_ald_008_escape_key_dismisses_dialog(page: Page):
    """ALD_008: Escape key dismisses the dialog.

    Expected: Result confirms dialog closed via keyboard; dialog disappears

    Steps:
    1. Open escape dialog via [data-testid="open-escape-dialog"]
    2. Assert dialog is visible
    3. Press Escape key (page.keyboard.press('Escape'))
    4. Assert dialog is gone and result is updated
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-testid="open-escape-dialog"]')

    page.locator('[data-testid="open-escape-dialog"]').click()
    escape_dialog = page.locator('[data-testid="escape-dismiss-dialog"]')
    expect(escape_dialog).to_be_visible()

    page.keyboard.press('Escape')
    expect(escape_dialog).not_to_be_visible()
    expect(page.locator('[data-testid^="result-s"]').filter(has_text='Escape')).to_be_visible()


def test_ald_009_dialog_body_text_without_testid(page: Page):
    """ALD_009: Dialog body text is assertable without data-testid.

    Expected: Text 'Sunday' is found inside the dialog body

    Steps:
    1. Open notification dialog via [data-testid="open-notification-dialog"]
    2. Scope into [data-testid="system-notification-dialog"]
    3. Assert getByText(/Sunday/) is visible inside the dialog
    4. Click the Acknowledge button and assert result
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-testid="open-notification-dialog"]')

    page.locator('[data-testid="open-notification-dialog"]').click()
    notification_dialog = page.locator('[class="alerts-dialogs-module__nGvyEG__dialogBodyText"]')
    expect(notification_dialog).to_be_visible()

    expect(notification_dialog.get_by_text('Sunday')).to_be_visible()
    page.locator('[data-testid="notif-ack-btn"]').click()

    expect(notification_dialog).not_to_be_visible()
    expect(page.locator('[data-testid^="result-s"]').filter(has_text='Acknowledged')).to_be_visible()


def test_ald_010_dialog_accessibility_attributes(page: Page):
    """ALD_010: Dialog has correct aria attributes for accessibility.

    Expected: role=dialog, aria-modal=true, and aria-labelledby are present

    Steps:
    1. Open any dialog, e.g. [data-testid="open-info-dialog"]
    2. Assert getAttribute("role") equals dialog
    3. Assert getAttribute("aria-modal") equals true
    4. Assert aria-labelledby points to a visible heading
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-testid="open-info-dialog"]')

    page.locator('[data-testid="open-info-dialog"]').click()
    dialog = page.locator('[data-testid="info-alert-dialog"]')

    expect(dialog).to_have_attribute('role', 'dialog')
    expect(dialog).to_have_attribute('aria-modal', 'true')

    labelledby = dialog.get_attribute('aria-labelledby')
    assert labelledby, 'Expected aria-labelledby to be present on dialog'
    expect(page.locator(f'#{labelledby}')).to_be_visible()


def test_ald_011_aria_labelledby_references_heading(page: Page):
    """ALD_011: aria-labelledby attribute references the visible heading.

    Expected: The heading element ID matches the dialog aria-labelledby value

    Steps:
    1. Open the info dialog and read aria-labelledby attribute
    2. Locate element by that ID
    3. Assert the element is the visible h2 heading
    4. Assert its text is non-empty
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-testid="open-info-dialog"]')

    page.locator('[data-testid="open-info-dialog"]').click()
    dialog = page.locator('[data-testid="info-alert-dialog"]')
    labelledby = dialog.get_attribute('aria-labelledby')

    assert labelledby, 'Expected aria-labelledby to be present on dialog'

    heading = page.locator(f'#{labelledby}')
    expect(heading).to_be_visible()
    expect(heading).to_have_text('Session Notice')
    assert heading.text_content().strip(), 'Expected non-empty heading text'


def test_ald_012_target_notification_from_repeated_buttons(page: Page):
    """ALD_012: Correct notification targeted from repeated Dismiss buttons.

    Expected: The 'Session Expiring Soon' notification is dismissed, not the others

    Steps:
    1. Locate [data-notif-id="notif-2"] [data-testid="notif-dismiss-btn"]
    2. Click it and confirm the dialog opens for Session Expiring Soon
    3. Assert the dialog data-notif-id="notif-2"
    4. Click confirm and assert result shows the correct notification title
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-notif-id="notif-2"] [data-testid="notif-dismiss-btn"]')

    page.locator('[data-notif-id="notif-2"] [data-testid="notif-dismiss-btn"]').click()

    scoped_dialog = page.locator('[data-testid="dismiss-confirm-dialog"][data-notif-id="notif-2"]')
    expect(scoped_dialog).to_be_visible()
    expect(scoped_dialog).to_contain_text('Session Expiring Soon')

    scoped_dialog.locator('[aria-label*="Confirm dismiss"]').click()
    expect(page.locator('[data-testid^="result-s"]').filter(has_text='Session Expiring Soon')).to_be_visible()


def test_ald_013_scoped_dismiss_confirm_dialog(page: Page):
    """ALD_013: Dismiss confirm dialog scoped by data-notif-id.

    Expected: Confirm button inside scoped dialog is clicked without ambiguity

    Steps:
    1. Trigger dismiss for notif-2
    2. Assert [data-testid="dismiss-confirm-dialog"][data-notif-id="notif-2"] is visible
    3. Click [aria-label*="Confirm dismiss"] inside that dialog
    4. Assert result confirms the correct notification
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-notif-id="notif-2"] [data-testid="notif-dismiss-btn"]')

    page.locator('[data-notif-id="notif-2"] [data-testid="notif-dismiss-btn"]').click()
    scoped_dialog = page.locator('[data-testid="dismiss-confirm-dialog"][data-notif-id="notif-2"]')
    expect(scoped_dialog).to_be_visible()

    scoped_dialog.locator('[aria-label*="Confirm dismiss"]').click()
    expect(scoped_dialog).not_to_be_visible()
    expect(page.locator('[data-testid^="result-s"]').filter(has_text='Session Expiring Soon')).to_be_visible()


def test_ald_014_dialog_box_click_does_not_close(page: Page):
    """ALD_014: Clicking dialog box does not fire backdrop close handler.

    Expected: Dialog remains open after clicking inside the dialog box

    Steps:
    1. Open backdrop dialog via [data-testid="open-backdrop-dialog"]
    2. Click the centered dialog box ([data-testid="backdrop-dialog-box"])
    3. Assert the dialog is still visible — click did not close it
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-testid="open-backdrop-dialog"]')

    page.locator('[data-testid="open-backdrop-dialog"]').click()
    backdrop_dialog = page.locator('[data-testid="backdrop-dismiss-dialog"]')
    expect(backdrop_dialog).to_be_visible()

    page.locator('[data-testid="backdrop-dialog-box"]').click()
    expect(backdrop_dialog).to_be_visible()


def test_ald_015_escape_key_idle_page_no_op(page: Page):
    """ALD_015: Escape key has no effect when no dialog is open.

    Expected: Page state remains unchanged when pressing Escape with no active dialog

    Steps:
    1. Ensure no dialog is currently open (initial page state)
    2. Press Escape on the page
    3. Assert no errors occur and no results change
    """
    page.goto(ALERTS_AND_DIALOGS_URL)
    page.wait_for_selector('[data-testid="open-info-dialog"]')

    all_results = page.locator('[data-testid^="result-s"]')
    initial_results = [text.strip() for text in all_results.all_text_contents()]

    expect(page.locator('[role="dialog"]')).to_have_count(0)
    page.keyboard.press('Escape')
    expect(page.locator('[role="dialog"]')).to_have_count(0)

    current_results = [text.strip() for text in all_results.all_text_contents()]
    assert current_results == initial_results, 'Expected no result text changes when Escape is pressed on idle page'


def test_ald_016_page_load_console_errors(page: Page):
    """ALD_016: Page loads without console errors.

    Expected: No uncaught errors are logged during initial load

    Steps:
    1. Attach listener to browser console and pageerror events
    2. Navigate to /practice/alerts-dialogs
    3. Assert no error-level messages were captured
    """
    console_errors = []
    page_errors = []

    def handle_console(msg):
        if msg.type == 'error':
            console_errors.append(msg.text)

    def handle_page_error(exception):
        page_errors.append(str(exception))

    page.on('console', handle_console)
    page.on('pageerror', handle_page_error)

    page.goto(ALERTS_AND_DIALOGS_URL)

    assert not console_errors, f'Console errors found: {console_errors}'
    assert not page_errors, f'Page errors found: {page_errors}'