from playwright.sync_api import Page, expect
from config import settings

DATA_TABLE_URL = settings.BASE_URL + "/data-table"

def test_dt_001_headers_presence(page:Page):
    """DT_001: All 7 column headers are present and correctly labelled.

    Expected: Headers read: Sr No., Book Name, Book Genre, Book Author,
    Book ISBN, Book Published, Actions

    Steps:
    1. Navigate to /practice/data-table
    2. Locate all th elements inside [data-testid="data-table"] thead
    3. Read each header text via allTextContents() / getText()
    4. Assert the array contains all 7 expected header labels
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    table_headers = page.locator('[data-testid="data-table"] thead th')
    expect(table_headers).to_contain_text(['Sr No.','Book Name','Book Genre','Book Author','Book ISBN','Book Published','Actions'])





def test_dt_002_initial_row_count(page:Page):
    """DT_002: Table displays exactly 5 rows on page 1 (25 total across 5 pages).

    Expected: Row count on page 1 equals 5; row-count indicator shows
    '25 books — page 1 of 5'

    Steps:
    1. Navigate to /practice/data-table
    2. Wait for [data-testid="data-table"] tbody tr to be visible
    3. Count tbody tr rows inside #dataTable
    4. Assert count() equals 5
    5. Assert [data-testid='row-count'] text contains 25 books
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    row_count = page.locator('[data-testid="data-table"] tbody tr')
    expect(row_count).to_have_count(5)
    expect(page.locator('[data-testid="row-count"]')).to_contain_text('25 books')


def test_dt_003_verify_specific_cell_value(page:Page):
    """DT_003: Row 2, Column 2 contains the book name 'Clean Code'.

    Expected: Cell text at row 2, column 2 equals 'Clean Code'

    Steps:
    1. Locate #dataTable tbody tr:nth-child(2) td:nth-child(2)
    2. Read cell text via textContent() / getText()
    3. Assert the trimmed text equals Clean Code
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    cell = page.locator('[data-testid="data-table"] tbody tr:nth-child(2) td:nth-child(2)')
    expect(cell).to_contain_text('Clean Code')
    


def test_dt_004_click_edit_for_specific_author(page:Page):
    """DT_004: Find the row for author 'George Orwell' and click its Edit button.

    Expected: The Edit button in the George Orwell row is clicked successfully

    Steps:
    1. Use Playwright: page.locator("[data-testid='book-row']").filter({
    hasText: 'George Orwell' })
    2. Scope to that row and click [data-testid='btn-edit-book']
    3. Assert the edit dialog or result panel appears
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    pagination_page_2 = page.locator('[data-testid="pagination-page-2"]')
    pagination_page_2.click()
    row = page.locator('[data-testid="data-table"] tbody tr').filter(
        has_text='George Orwell')
    edit_button = row.get_by_test_id('btn-edit-book')
    edit_button.click()
    expect(page.locator('[id="edit-dialog-title"]')).to_contain_text('Edit Book')
    


def test_dt_005_table_not_empty(page:Page):
    """DT_005: Table is not empty after initial page load.

    Expected: tbody contains at least one visible row

    Steps:
    1. Navigate to /practice/data-table
    2. Assert tbody tr count is greater than 0
    3. Assert the first row is visible
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    row_count = page.locator('[data-testid="data-table"] tbody tr')
    expect(row_count).to_have_count(5)
    expect(page.locator('[data-testid="table-body"] tr:nth-child(1)')).to_be_visible()


def test_dt_006_verify_isbn_prefix(page:Page):
    """DT_006: All values in the Book ISBN column start with 'ISBN-'.

    Expected: Every ISBN cell begins with the prefix 'ISBN-'

    Steps:
    1. Locate all td[data-col='book-isbn'] cells
    2. Read all texts via allTextContents()
    3. Assert each value starts with ISBN-
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    isbn_cells = page.locator('[data-testid="data-table"] tbody td[data-col="book-isbn"]').all_text_contents()
    for isbn in isbn_cells:
        assert isbn.startswith('ISBN-')


def test_dt_007_search_by_book_name(page: Page):
    """DT_007: Searching by a book name filters the visible rows.

    Expected: Only rows matching the search term remain visible

    Steps:
    1. Locate [data-testid='table-search']
    2. Type Clean Code into the search input
    3. Assert row count drops to 2 (matching rows)
    4. Assert the visible row contains text Clean Code
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    page.locator('[data-testid="table-search"]').fill('Clean Code')
    rows = page.locator('[data-testid="data-table"] tbody tr')
    expect(rows).to_have_count(2)
    expect(rows.first).to_contain_text('Clean Code')


def test_dt_008_genre_filter(page: Page):
    """DT_008: Genre filter reduces visible rows to the selected genre only.

    Expected: Only books in the chosen genre are shown after filtering

    Steps:
    1. Locate [data-testid='genre-filter']
    2. Select Technology from the dropdown
    3. Assert all visible rows contain Technology in the genre cell
    4. Assert rows from other genres are not present
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    page.locator('[data-testid="genre-filter"]').select_option('Technology')
    genre_cells = page.locator('[data-testid="data-table"] tbody td[data-col="book-genre"]').all_text_contents()
    assert len(genre_cells) > 0
    for genre in genre_cells:
        assert genre.strip() == 'Technology'


def test_dt_009_locate_delete_via_aria_label(page: Page):
    """DT_009: Delete button for a row has no data-testid — located via aria-label.

    Expected: Delete button is found and accessible via aria-label or XPath

    Steps:
    1. Locate the row for book 'Dune' using filter({ hasText: 'Dune' })
    2. Find Delete button via getByRole("button", { name: /Delete Dune/ })
    3. Assert the button is visible
    4. XPath: //tr[.//td[normalize-space()='Dune']]//button[contains(@aria-label,'Delete')]
    """
    
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    dune_row = page.locator('[data-testid="data-table"] tbody tr').filter(has_text='Dune')
    delete_btn = page.get_by_role("button", name="Delete Dune")
    expect(delete_btn).to_be_visible()


def test_dt_010_locate_row_by_book_id(page: Page):
    """DT_010: Row can be located by its data-book-id attribute.

    Expected: Row with data-book-id='book-004' contains 'The Hobbit'

    Steps:
    1. Locate [data-testid='book-row'][data-book-id='book-004']
    2. Assert the row contains text The Hobbit
    3. XPath: //tr[@data-book-id='book-004']
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    row = page.locator('[data-testid="book-row"][data-book-id="book-004"]')
    expect(row).to_contain_text('The Hobbit')


def test_dt_011_clear_search_restores_rows(page: Page):
    """DT_011: Clearing the search input restores all rows and resets pagination.

    Expected: After clearing search, page 1 shows 5 rows and pagination shows
    5 pages

    Steps:
    1. Type a search term to filter rows down to fewer than 5
    2. Clear the search input via clear() or triple_click + type('')
    3. Assert tbody tr count returns to 5 (page 1)
    4. Assert [data-testid='pagination'] shows 5 page buttons
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    search_input = page.locator('[data-testid="table-search"]')
    search_input.fill('Clean Code')
    rows = page.locator('[data-testid="data-table"] tbody tr')
    expect(rows).to_have_count(2)
    search_input.clear()
    expect(rows).to_have_count(5)
    page_buttons = page.locator('[data-testid^="pagination-page-"]')
    expect(page_buttons).to_have_count(5)


def test_dt_012_row_count_updates_on_filter(page: Page):
    """DT_012: Row-count display updates after filtering.

    Expected: The row-count indicator reflects the filtered count

    Steps:
    1. Note initial [data-testid='row-count'] text (should include '25 books')
    2. Apply a genre filter
    3. Assert [data-testid='row-count'] reflects the new filtered count
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    row_count_el = page.locator('[data-testid="row-count"]')
    expect(row_count_el).to_contain_text('25 books')
    page.locator('[data-testid="genre-filter"]').select_option('Technology')
    expect(row_count_el).not_to_contain_text('25 books')


def test_dt_013_page_2_navigation(page: Page):
    """DT_013: Clicking page 2 loads the next set of rows.

    Expected: Page 2 shows rows 6-10 and the active page button is highlighted

    Steps:
    1. Locate [data-testid='pagination']
    2. Click [data-testid='pagination-page-2']
    3. Assert tbody tr count equals 5
    4. Assert first visible row Sr No. value is 6
    5. Assert [data-testid='pagination-page-2'] has aria-current='page'
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    page.locator('[data-testid="pagination-page-2"]').click()
    rows = page.locator('[data-testid="data-table"] tbody tr')
    expect(rows).to_have_count(5)
    expect(rows.first.locator('td').first).to_have_text('6')
    expect(page.locator('[data-testid="pagination-page-2"]')).to_have_attribute('aria-current', 'page')


def test_dt_014_next_button_navigation(page: Page):
    """DT_014: Clicking Next navigates to the following page.

    Expected: Next button advances pagination by one page

    Steps:
    1. Assert current page is 1 (page-1 button has aria-current='page')
    2. Click [data-testid='pagination-next']
    3. Assert [data-testid='pagination-page-2'] now has aria-current='page'
    4. Assert Previous button is now enabled
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    expect(page.locator('[data-testid="pagination-page-1"]')).to_have_attribute('aria-current', 'page')
    page.locator('[data-testid="pagination-next"]').click()
    expect(page.locator('[data-testid="pagination-page-2"]')).to_have_attribute('aria-current', 'page')
    expect(page.locator('[data-testid="pagination-prev"]')).not_to_be_disabled()


def test_dt_015_previous_button_state(page: Page):
    """DT_015: Previous button is disabled on page 1 and enabled on page 2+.

    Expected: Prev is disabled on first page, enabled on all others

    Steps:
    1. On page 1, assert [data-testid='pagination-prev'] has disabled attribute
    2. Click page 2 button
    3. Assert Prev button is no longer disabled
    4. Assert Next button is still enabled (not on last page)
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    expect(page.locator('[data-testid="pagination-prev"]')).to_be_disabled()
    page.locator('[data-testid="pagination-page-2"]').click()
    expect(page.locator('[data-testid="pagination-prev"]')).not_to_be_disabled()
    expect(page.locator('[data-testid="pagination-next"]')).not_to_be_disabled()


def test_dt_016_column_sorting_toggle(page: Page):
    """DT_016: Clicking a sortable column header sorts rows ascending then descending.

    Expected: First click sorts A to Z, second click sorts Z to A, third click
    resets sort

    Steps:
    1. Click [data-testid='col-book-name'] column header
    2. Assert aria-sort='ascending' is set on that header
    3. Assert first visible book name is alphabetically first
    4. Click the same header again
    5. Assert aria-sort='descending' is set
    6. Click a third time and assert aria-sort='none' and original order returns
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    col_header = page.locator('[data-testid="col-book-name"]')
    
    col_header.click()
    expect(col_header).to_have_attribute('aria-sort', 'ascending')
    
    col_header.click()
    expect(col_header).to_have_attribute('aria-sort', 'descending')
    
    col_header.click()
    expect(col_header).to_have_attribute('aria-sort', 'none')


def test_dt_017_sorting_resets_to_page_1(page: Page):
    """DT_017: Sorting resets to page 1 when a different page is active.

    Expected: Changing sort while on page 3 jumps back to page 1

    Steps:
    1. Navigate to page 3 via [data-testid='pagination-page-3']
    2. Click a column header to sort
    3. Assert [data-testid='pagination-page-1'] has aria-current='page'
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    page.locator('[data-testid="pagination-page-3"]').click()
    page.locator('[data-testid="col-book-name"]').click()
    expect(page.locator('[data-testid="pagination-page-1"]')).to_have_attribute('aria-current', 'page')


def test_dt_018_add_new_book(page: Page):
    """DT_018: Add new book via the Add Book dialog and verify it appears in the table.

    Expected: New book row appears on the last page and persists after reload

    Steps:
    1. Click [data-testid='btn-add-book']
    2. Assert [data-testid='add-book-dialog'] is visible
    3. Fill [data-testid='add-input-book-name'] with a unique book title
    4. Fill [data-testid='add-input-book-author'] with an author name
    5. Select a genre from [data-testid='add-select-genre']
    6. Click [data-testid='add-dialog-save']
    7. Navigate to the last page and assert the new row is visible
    8. Reload the page and confirm the new book persists (localStorage)
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    page.locator('[data-testid="btn-add-book"]').click()
    expect(page.locator('[data-testid="add-book-dialog"]')).to_be_visible()
    
    unique_title = 'Unique Test Book'
    page.locator('[data-testid="add-input-book-name"]').fill(unique_title)
    page.locator('[data-testid="add-input-book-author"]').fill('Test Author')
    page.locator('[data-testid="add-select-genre"]').select_option('Fiction')
    page.locator('[data-testid="add-dialog-save"]').click()
    
    page.locator('[data-testid^="pagination-page-"]').last.click()
    expect(page.locator('[data-testid="data-table"] tbody')).to_contain_text(unique_title)
    
    page.reload()
    page.wait_for_selector('[data-testid="data-table"]')
    page.locator('[data-testid^="pagination-page-"]').last.click()
    expect(page.locator('[data-testid="data-table"] tbody')).to_contain_text(unique_title)


def test_dt_019_add_book_validation_errors(page: Page):
    """DT_019: Add Book dialog shows validation errors when required fields are empty.

    Expected: Submitting with empty Name or Author shows inline error messages

    Steps:
    1. Click [data-testid='btn-add-book']
    2. Leave Book Name and Author blank
    3. Click [data-testid='add-dialog-save']
    4. Assert [data-testid='add-name-error'] is visible
    5. Assert [data-testid='add-author-error'] is visible
    6. Assert dialog is still open (no premature close)
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    page.locator('[data-testid="btn-add-book"]').click()
    page.locator('[data-testid="add-dialog-save"]').click()
    expect(page.locator('[data-testid="add-name-error"]')).to_be_visible()
    expect(page.locator('[data-testid="add-author-error"]')).to_be_visible()
    expect(page.locator('[data-testid="add-book-dialog"]')).to_be_visible()


def test_dt_020_edit_book_values(page: Page):
    """DT_020: Edit a book and verify the updated values are saved.

    Expected: Edited fields reflect new values in the table row and persist
    after reload

    Steps:
    1. Click [data-testid='btn-edit-book'] in the row for 'Clean Code'
    2. Assert [data-testid='edit-book-dialog'] is visible
    3. Clear and type a new value in [data-testid='edit-input-book-name']
    4. Click [data-testid='edit-dialog-save']
    5. Assert the row now shows the new book name
    6. Reload and confirm the edit persists
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    row = page.locator('[data-testid="data-table"] tbody tr').filter(has_text='Clean Code')
    row.get_by_test_id('btn-edit-book').click()
    expect(page.locator('[data-testid="edit-book-dialog"]')).to_be_visible()
    
    new_name = 'Clean Code Updated'
    name_input = page.locator('[data-testid="edit-input-book-name"]')
    name_input.clear()
    name_input.fill(new_name)
    page.locator('[data-testid="edit-dialog-save"]').click()
    
    expect(page.locator('[data-testid="data-table"] tbody')).to_contain_text(new_name)
    page.reload()
    page.wait_for_selector('[data-testid="data-table"]')
    expect(page.locator('[data-testid="data-table"] tbody')).to_contain_text(new_name)


def test_dt_021_delete_book(page: Page):
    """DT_021: Delete a book and verify the row is removed from all pages.

    Expected: Deleted book no longer appears and row count decreases by 1

    Steps:
    1. Locate the row for 'Dune' using filter({ hasText: 'Dune' })
    2. Click its Delete button via getByRole('button', { name: /Delete Dune/ })
    3. Assert [data-testid='delete-book-dialog'] is visible
    4. Click the Confirm button via aria-label='Confirm delete Dune'
    5. Assert no row with text 'Dune' exists across any page
    6. Assert [data-testid='row-count'] decreased by 1
    """
    page.goto(DATA_TABLE_URL)
    page.wait_for_selector('[data-testid="data-table"]')
    
    dune_row = page.locator('[data-testid="data-table"] tbody tr').filter(has_text='Dune')
    if dune_row.count() == 0:
        page.locator('[data-testid="table-search"]').fill('Dune')
        dune_row = page.locator('[data-testid="data-table"] tbody tr').filter(has_text='Dune')
        
    delete_btn = dune_row.get_by_role('button', name='Delete Dune')
    delete_btn.click()
    
    expect(page.locator('[data-testid="delete-book-dialog"]')).to_be_visible()
    confirm_btn = page.locator('[aria-label="Confirm delete Dune"]')
    confirm_btn.click()
    
    expect(page.locator('[data-testid="data-table"] tbody')).not_to_contain_text('Dune')