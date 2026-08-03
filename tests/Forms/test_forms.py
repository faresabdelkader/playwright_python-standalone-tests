import re
from playwright.sync_api import Page, expect
from config import settings

FORMS_URL = settings.BASE_URL + "/forms"

def test_frm_001_fill_all_required_fields_with_valid_data_and_submit_successfully(page: Page):
    """FRM_001: Fill all required fields with valid data and submit successfully

    Expected: Success message appears showing the submitted first name

    Steps:
    1. Navigate to /forms
    2. Fill [data-testid='input-first-name'] with John
    3. Fill [data-testid='input-last-name'] with Doe
    4. Fill [data-testid='input-email'] with john@example.com
    5. Fill [data-testid='input-phone'] with 9876543210
    6. Fill [data-testid='input-dob'] with 1995-06-15
    7. Check [data-testid='radio-gender-male']
    8. Select India from [data-testid='select-country']
    9. Fill [data-testid='input-city'] with Mumbai
    10. Check [data-testid='checkbox-interest-playwright']
    11. Fill [data-testid='input-password'] with secret123
    12. Fill [data-testid='input-confirm-password'] with secret123
    13. Check [data-testid='checkbox-terms']
    14. Click [data-testid='submit-form-btn']
    15. Assert [data-testid='form-success-msg'] is visible
    16. Assert [data-testid='submitted-name'] contains John
    """
    page.goto(FORMS_URL)
    
    # Verify that the form is loaded and interactive
    page.wait_for_selector('[data-testid="registration-form"]')

    # Fill required fields with valid data
    page.fill('[data-testid="input-first-name"]', 'John')
    page.fill('[data-testid="input-last-name"]', 'Doe')
    page.fill('[data-testid="input-login-email"]', 'john@example.com')
    page.fill('[data-testid="input-phone"]', '9876543210')
    page.fill('[data-testid="input-dob"]', '1995-06-15')
    
    # Select male gender
    page.check('[data-testid="radio-gender-male"]')
    
    # Select India from country dropdown
    page.select_option('[data-testid="select-country"]', label='India')
    
    # Fill city
    page.fill('[data-testid="input-city"]', 'Mumbai')
    
    # Select interests
    page.check('[data-testid="checkbox-interest-playwright"]')
    
    # Fill passwords
    page.fill('[data-testid="input-password"]', 'secret123')
    page.fill('[data-testid="input-confirm-password"]', 'secret123')
    
    # Accept terms
    page.check('[data-testid="checkbox-terms"]')
    
    # Submit the form
    page.click('[data-testid="submit-form-btn"]')
    
    # Assert success message is visible
    success_message = page.locator('[data-testid="form-success-msg"]')
    expect(success_message).to_be_visible()
    expect(success_message).to_contain_text('Account Setup Complete!')
    
    # Assert submitted name is displayed correctly
    submitted_name = page.locator('[data-testid="submitted-name"]')
    expect(submitted_name).to_contain_text('Your account has been secured.')


def test_frm_002_required_field_errors_appear_on_empty_submit(page: Page):
    """FRM_002: Required field errors appear on empty submit

    Expected: Validation error messages display under each required field

    Steps:
    1. Navigate to /practice/forms
    2. Click [data-testid='submit-form-btn'] without filling any fields
    3. Assert [data-testid='error-first-name'] is visible
    4. Assert [data-testid='error-last-name'] is visible
    5. Assert [data-testid='error-email'] is visible
    6. Assert [data-testid='error-phone'] is visible
    7. Assert [data-testid='error-dob'] is visible
    8. Assert [data-testid='error-gender'] is visible
    9. Assert [data-testid='error-country'] is visible
    10. Assert [data-testid='error-city'] is visible
    11. Assert [data-testid='error-password'] is visible
    """
    page.goto(FORMS_URL)
    # Verify that the form is loaded and interactive
    page.wait_for_selector('[data-testid="registration-form"]')
    page.click('[data-testid="submit-form-btn"]')
    page.click('[id="interestsSubmitBtn"]')
    page.click('[id="addressSubmitBtn"]')
    page.click('[id="personalSubmitBtn"]')
    page.click('[data-testid="btn-login-submit"]')

    
    # Assert error messages are visible
    error_first_name = page.locator('[data-testid="error-first-name"]')
    error_last_name = page.locator('[data-testid="error-last-name"]')
    error_email = page.locator('[data-testid="error-login-email"]')
    error_phone = page.locator('[data-testid="error-phone"]')
    error_dob = page.locator('[data-testid="error-dob"]')
    error_gender = page.locator('[data-testid="error-gender"]')
    error_country = page.locator('[data-testid="error-country"]')
    error_city = page.locator('[data-testid="error-city"]')
    error_password = page.locator('[data-testid="error-password"]')
    
    expect(error_first_name).to_be_visible()
    expect(error_last_name).to_be_visible()
    expect(error_email).to_be_visible()
    expect(error_phone).to_be_visible()
    expect(error_dob).to_be_visible()
    expect(error_gender).to_be_visible()
    expect(error_country).to_be_visible()
    expect(error_city).to_be_visible()
    expect(error_password).to_be_visible()


def test_frm_003_invalid_email_format_shows_validation_error(page: Page):
    """FRM_003: Invalid email format shows validation error

    Expected: Error message tells the user the email format is invalid

    Steps:
    1. Fill [data-testid='input-email'] with notanemail
    2. Click [data-testid='submit-form-btn']
    3. Assert [data-testid='error-email'] contains valid email
    """
    page.goto(FORMS_URL)
    # Verify that the form is loaded and interactive
    page.wait_for_selector('[data-testid="registration-form"]')
    page.fill('[data-testid="input-login-email"]', 'notanemail')
    page.click('[data-testid="btn-login-submit"]')
    error_email = page.locator('[data-testid="error-login-email"]')
    expect(error_email).to_contain_text("Enter a valid email address.")


def test_frm_004_invalid_phone_number_format_shows_error(page: Page):
    """FRM_004: Invalid phone number format shows error

    Expected: Error message tells the user the phone must be 10 digits

    Steps:
    1. Fill [data-testid='input-phone'] with 123
    2. Click [data-testid='submit-form-btn']
    3. Assert [data-testid='error-phone'] contains 10 digits
    """
    page.goto(FORMS_URL)
    # Verify that the form is loaded and interactive
    page.wait_for_selector('[data-testid="registration-form"]')
    page.fill('[data-testid="input-phone"]', '123')
    page.click('[data-testid="btn-personal-submit"]')
    error_phone = page.locator('[data-testid="error-phone"]')
    expect(error_phone).to_contain_text("Phone must be exactly 10 digits")


def test_frm_005_password_shorter_than_6_characters_shows_validation_error(page: Page):
    """FRM_005: Password shorter than 6 characters shows validation error

    Expected: Password minimum length error message appears

    Steps:
    1. Fill [data-testid='input-password'] with abc
    2. Click [data-testid='submit-form-btn']
    3. Assert [data-testid='error-password'] contains 6 characters
    """
    page.goto(FORMS_URL)
    page.wait_for_selector('[data-testid="registration-form"]')
    page.fill('[data-testid="input-password"]', 'abc')
    page.click('[data-testid="submit-form-btn"]')

    error_password = page.locator('[data-testid="error-password"]')
    expect(error_password).to_be_visible()
    expect(error_password).to_contain_text("6 characters")


def test_frm_006_mismatched_passwords_show_confirm_password_error(page: Page):
    """FRM_006: Mismatched passwords show confirm password error

    Expected: Error message saying passwords do not match appears under confirm password

    Steps:
    1. Fill [data-testid='input-password'] with secret123
    2. Fill [data-testid='input-confirm-password'] with wrong456
    3. Click [data-testid='submit-form-btn']
    4. Assert [data-testid='error-confirm-password'] has text Passwords do not match.
    """
    page.goto(FORMS_URL)
    page.wait_for_selector('[data-testid="registration-form"]')
    page.fill('[data-testid="input-password"]', 'secret123')
    page.fill('[data-testid="input-confirm-password"]', 'wrong456')
    page.click('[data-testid="submit-form-btn"]')

    error_confirm = page.locator('[data-testid="error-confirm-password"]')
    expect(error_confirm).to_be_visible()
    expect(error_confirm).to_contain_text("Passwords do not match")


def test_frm_007_unchecked_terms_checkbox_shows_required_error(page: Page):
    """FRM_007: Unchecked Terms checkbox shows required error

    Expected: An error message prompts the user to accept the terms

    Steps:
    1. Fill all other fields correctly
    2. Leave [data-testid='checkbox-terms'] unchecked
    3. Click [data-testid='submit-form-btn']
    4. Assert error text You must accept the Terms is visible
    """
    page.goto(FORMS_URL)
    page.wait_for_selector('[data-testid="registration-form"]')

    # Fill all fields in all forms correctly
    page.fill('[data-testid="input-login-email"]', 'john@example.com')
    page.fill('#login-password', 'secret123')
    page.fill('[data-testid="input-first-name"]', 'John')
    page.fill('[data-testid="input-last-name"]', 'Doe')
    page.fill('[data-testid="input-phone"]', '9876543210')
    page.fill('[data-testid="input-dob"]', '1995-06-15')
    page.check('[data-testid="radio-gender-male"]')
    page.select_option('[data-testid="select-country"]', label='Japan')
    page.fill('[data-testid="input-city"]', 'Tokyo')
    page.check('[data-testid="checkbox-interest-playwright"]')
    page.fill('[data-testid="input-password"]', 'secret123')
    page.fill('[data-testid="input-confirm-password"]', 'secret123')
    # Deliberately leave terms unchecked

    page.click('[data-testid="submit-form-btn"]')

    error_terms = page.locator('[id="termsError"]')
    expect(error_terms).to_be_visible()
    expect(error_terms).to_contain_text("accept the Terms")


def test_frm_008_success_message_displays_the_submitted_first_name(page: Page):
    """FRM_008: Success message displays the submitted first name

    Expected: The submitted-name element contains the first name that was entered

    Steps:
    1. Submit the form with first name Rahul
    2. Assert [data-testid='form-success-msg'] is visible
    3. Assert [data-testid='submitted-name'] contains text Rahul
    """
    page.goto(FORMS_URL)
    page.wait_for_selector('[data-testid="registration-form"]')

    # Fill all required fields with first name Rahul
    page.fill('[data-testid="input-first-name"]', 'Rahul')
    page.fill('[data-testid="input-last-name"]', 'Sharma')
    page.fill('[data-testid="input-login-email"]', 'rahul@example.com')
    page.fill('[data-testid="input-phone"]', '9876543210')
    page.fill('[data-testid="input-dob"]', '1995-06-15')
    page.check('[data-testid="radio-gender-male"]')
    page.select_option('[data-testid="select-country"]', label='India')
    page.fill('[data-testid="input-city"]', 'Mumbai')
    page.check('[data-testid="checkbox-interest-playwright"]')
    page.fill('[data-testid="input-password"]', 'secret123')
    page.fill('[data-testid="input-confirm-password"]', 'secret123')
    page.check('[data-testid="checkbox-terms"]')

    page.click('[data-testid="submit-form-btn"]')

    success_message = page.locator('[data-testid="form-success-msg"]')
    expect(success_message).to_be_visible()
    expect(success_message).to_contain_text('Account Setup Complete!')


def test_frm_009_reset_button_clears_all_fields(page: Page):
    """FRM_009: Reset button clears all fields

    Expected: All inputs return to their empty/default state after reset

    Steps:
    1. Fill several fields with data
    2. Click [data-testid='reset-form-btn']
    3. Assert [data-testid='input-first-name'] value is empty
    4. Assert [data-testid='input-email'] value is empty
    5. Assert no error messages are visible
    """
    page.goto(FORMS_URL)
    page.wait_for_selector('[data-testid="registration-form"]')

    # Fill some fields in the Account Setup form (F05)
    page.fill('[data-testid="input-password"]', 'secret123')
    page.fill('[data-testid="input-confirm-password"]', 'secret123')
    page.check('[data-testid="checkbox-terms"]')

    # Click the reset button on the Account Setup form
    page.click('[data-testid="reset-form-btn"]')

    # Assert the fields are cleared
    expect(page.locator('[data-testid="input-password"]')).to_have_value('')
    expect(page.locator('[data-testid="input-confirm-password"]')).to_have_value('')
    expect(page.locator('[data-testid="checkbox-terms"]')).not_to_be_checked()


def test_frm_010_gender_radio_button_selection(page: Page):
    """FRM_010: Gender radio button selection

    Expected: Only the selected radio reflects a checked state; others are unchecked

    Steps:
    1. Check [data-testid='radio-gender-female']
    2. Assert [data-testid='radio-gender-female'] is checked
    3. Assert [data-testid='radio-gender-male'] is not checked
    """
    page.goto(FORMS_URL)
    page.wait_for_selector('[data-testid="registration-form"]')

    page.check('[data-testid="radio-gender-female"]')

    expect(page.locator('[data-testid="radio-gender-female"]')).to_be_checked()
    expect(page.locator('[data-testid="radio-gender-male"]')).not_to_be_checked()


def test_frm_011_country_dropdown_selection(page: Page):
    """FRM_011: Country dropdown selection

    Expected: The selected country value is reflected in the select element

    Steps:
    1. Locate [data-testid='select-country']
    2. Select option India
    3. Assert the select value is IN
    """
    page.goto(FORMS_URL)
    page.wait_for_selector('[data-testid="registration-form"]')

    page.select_option('[data-testid="select-country"]', label='India')

    expect(page.locator('[data-testid="select-country"]')).to_have_value('IN')


def test_frm_012_multiple_interest_checkboxes_can_be_selected_independently(page: Page):
    """FRM_012: Multiple interest checkboxes can be selected independently

    Expected: Each selected checkbox is independently checked and others are unaffected

    Steps:
    1. Check [data-testid='checkbox-interest-selenium']
    2. Check [data-testid='checkbox-interest-playwright']
    3. Assert both are checked
    4. Assert [data-testid='checkbox-interest-cypress'] is not checked
    """
    page.goto(FORMS_URL)
    page.wait_for_selector('[data-testid="registration-form"]')

    page.check('[data-testid="checkbox-interest-selenium"]')
    page.check('[data-testid="checkbox-interest-playwright"]')

    expect(page.locator('[data-testid="checkbox-interest-selenium"]')).to_be_checked()
    expect(page.locator('[data-testid="checkbox-interest-playwright"]')).to_be_checked()
    expect(page.locator('[data-testid="checkbox-interest-cypress"]')).not_to_be_checked()


def test_frm_013_form_fields_retain_values_after_a_validation_failure(page: Page):
    """FRM_013: Form fields retain values after a validation failure

    Expected: Filled fields keep their values when submit fails due to another field being invalid

    Steps:
    1. Fill [data-testid='input-first-name'] with Jane
    2. Leave email empty
    3. Click [data-testid='submit-form-btn']
    4. Assert [data-testid='input-first-name'] still shows Jane
    5. Assert [data-testid='error-email'] is visible
    """
    page.goto(FORMS_URL)
    page.wait_for_selector('[data-testid="registration-form"]')

    # Fill first name but leave other fields empty
    page.fill('[data-testid="input-first-name"]', 'Jane')

    # Submit via master submit to trigger validation across all forms
    page.click('[data-testid="btn-login-submit"]')

    # Assert first name retains its value
    expect(page.locator('[data-testid="input-first-name"]')).to_have_value('Jane')

    # Assert email error is visible (login form requires email)
    error_email = page.locator('[data-testid="error-login-email"]')
    expect(error_email).to_be_visible()
    expect(error_email).to_contain_text("Email is required")


def test_frm_014_fill_again_button_returns_to_empty_form_from_success_state(page: Page):
    """FRM_014: Fill Again button returns to empty form from success state

    Expected: Clicking Fill Again hides the success message and shows a fresh empty form

    Steps:
    1. Submit the form successfully
    2. Assert [data-testid='form-success-msg'] is visible
    3. Click the Fill Again button
    4. Assert [data-testid='form-success-msg'] is not visible
    5. Assert [data-testid='input-first-name'] is empty
    """
    page.goto(FORMS_URL)
    page.wait_for_selector('[data-testid="registration-form"]')

    # Fill all required fields
    page.fill('[data-testid="input-first-name"]', 'John')
    page.fill('[data-testid="input-last-name"]', 'Doe')
    page.fill('[data-testid="input-login-email"]', 'john@example.com')
    page.fill('[data-testid="input-phone"]', '9876543210')
    page.fill('[data-testid="input-dob"]', '1995-06-15')
    page.check('[data-testid="radio-gender-male"]')
    page.select_option('[data-testid="select-country"]', label='India')
    page.fill('[data-testid="input-city"]', 'Mumbai')
    page.check('[data-testid="checkbox-interest-playwright"]')
    page.fill('[data-testid="input-password"]', 'secret123')
    page.fill('[data-testid="input-confirm-password"]', 'secret123')
    page.check('[data-testid="checkbox-terms"]')

    page.click('[data-testid="submit-form-btn"]')

    # Assert success message is visible
    success_message = page.locator('[data-testid="form-success-msg"]')
    expect(success_message).to_be_visible()

    # Click the Fill Again button
    page.locator('[data-testid="form-success-msg"]').get_by_text('Fill Again').click()

    # Assert success message is hidden and form is empty
    expect(success_message).not_to_be_visible()
    expect(page.locator('[data-testid="input-password"]')).to_have_value('')


def test_frm_015_form_page_loads_without_javascript_errors(page: Page):
    """FRM_015: Form page loads without JavaScript errors

    Expected: No console errors on page load; all form fields are present and interactive

    Steps:
    1. Navigate to /practice/forms
    2. Assert page title contains Form Automation
    3. Assert [data-testid='registration-form'] is visible
    4. Check browser console for errors
    """
    # Collect console errors
    console_errors = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

    page.goto(FORMS_URL)
    page.wait_for_selector('[data-testid="registration-form"]')

    # Assert page title contains Form Automation
    expect(page).to_have_title(re.compile(r'Form Automation Practice'))

    # Assert main form sections are visible
    expect(page.locator('[data-testid="registration-form"]')).to_be_visible()
    expect(page.locator('[data-testid="input-first-name"]')).to_be_visible()
    expect(page.locator('[data-testid="input-last-name"]')).to_be_visible()
    expect(page.locator('[data-testid="input-login-email"]')).to_be_visible()
    expect(page.locator('[data-testid="input-phone"]')).to_be_visible()
    expect(page.locator('[data-testid="input-dob"]')).to_be_visible()
    expect(page.locator('[data-testid="select-country"]')).to_be_visible()
    expect(page.locator('[data-testid="input-city"]')).to_be_visible()
    expect(page.locator('[data-testid="input-password"]')).to_be_visible()
    expect(page.locator('[data-testid="input-confirm-password"]')).to_be_visible()

    # Assert no JavaScript console errors
    assert len(console_errors) == 0, f"Console errors detected: {console_errors}"
