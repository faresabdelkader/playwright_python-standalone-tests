# Input Field Test Cases

| ID | Scenario | Type | Priority |
|----|----------|------|----------|
| INP_001 | Text can be typed into an input field | positive | high |
| INP_002 | Submitting the typed value updates the result | positive | high |
| INP_003 | Placeholder is replaced when text is entered | positive | medium |
| INP_004 | Text is appended to existing content | positive | high |
| INP_005 | Tab moves focus away from the field | positive | medium |
| INP_006 | Current field value can be read | positive | high |
| INP_007 | A populated field can be cleared | positive | high |
| INP_008 | Disabled input rejects keyboard input | negative | high |
| INP_009 | Readonly input cannot be edited | negative | high |
| INP_010 | Readonly value is still readable | positive | medium |
| INP_011 | Field handles a long string without truncation | edge | low |
| INP_012 | Field state resets after a page refresh | edge | low |

---

## INP_001 — Text can be typed into an input field

**Expected:** The field holds the typed value after entry  
**Type:** positive | **Priority:** high

### Steps
1. Navigate to `/practice/input-fields`
2. Locate the input `[data-testid="input-movie-name"]`
3. Type `Interstellar` via `fill()` / `sendKeys()`
4. Assert `inputValue()` equals `Interstellar`

---

## INP_002 — Submitting the typed value updates the result

**Expected:** Result reflects exactly what was entered  
**Type:** positive | **Priority:** high

### Steps
1. Type a value into `[data-testid="input-movie-name"]`
2. Click `[data-testid="btn-submit-movie"]`
3. Assert `[data-testid="result-s01"]` contains the typed value

---

## INP_003 — Placeholder is replaced when text is entered

**Expected:** Placeholder hides once the field has a value  
**Type:** positive | **Priority:** medium

### Steps
1. Read the `placeholder` attribute on `[data-testid="input-movie-name"]`
2. Type any text into the field
3. Assert the field value is non-empty (placeholder no longer shown)

---

## INP_004 — Text is appended to existing content

**Expected:** New text is added after the pre-filled value, not replacing it  
**Type:** positive | **Priority:** high

> **Note:** Playwright's `fill()` clears first — use `click()` + `keyboard.type()` to truly append.

### Steps
1. Locate `[data-testid="input-append"]` pre-filled with `Avengers`
2. Click into the field and type `Endgame`
3. Press `Tab` to blur the field
4. Assert `[data-testid="result-s02"]` shows `Avengers Endgame`

---

## INP_005 — Tab moves focus away from the field

**Expected:** Field loses focus and the blur result is recorded  
**Type:** positive | **Priority:** medium

### Steps
1. Focus `[data-testid="input-append"]`
2. Press `Tab`
3. Assert the input is no longer the active/focused element

---

## INP_006 — Current field value can be read

**Expected:** Reading returns the value currently in the field  
**Type:** positive | **Priority:** high

### Steps
1. Locate `[data-testid="input-read-value"]`
2. Click `[data-testid="btn-read-value"]`
3. Assert `[data-testid="result-s03"]` shows the field value

---

## INP_007 — A populated field can be cleared

**Expected:** Field becomes empty after clearing  
**Type:** positive | **Priority:** high

### Steps
1. Locate `[data-testid="input-clear"]` pre-filled with `Inception`
2. Click `[data-testid="btn-clear-field"]` (or call `clear()` / `fill("")`)
3. Assert `inputValue()` is empty and `[data-testid="result-s04"]` confirms it

---

## INP_008 — Disabled input rejects keyboard input

**Expected:** Field is disabled and cannot receive text  
**Type:** negative | **Priority:** high

> **Note:** Playwright throws on typing into a disabled field — assert state instead.

### Steps
1. Locate `[data-testid="input-disabled"]`
2. Assert `isEnabled()` is false / `toBeDisabled()` passes
3. Confirm typing does not change the value

---

## INP_009 — Readonly input cannot be edited

**Expected:** Field has a value that the user cannot modify  
**Type:** negative | **Priority:** high

### Steps
1. Locate `[data-testid="input-readonly"]`
2. Assert the `readonly` attribute is present
3. Attempt to type and confirm the value stays unchanged

---

## INP_010 — Readonly value is still readable

**Expected:** Value can be read even though it is not editable  
**Type:** positive | **Priority:** medium

### Steps
1. Locate `[data-testid="input-readonly"]`
2. Read `getAttribute("value")` / `inputValue()`
3. Assert the returned value is non-empty

---

## INP_011 — Field handles a long string without truncation

**Expected:** Entire long value is retained in the field  
**Type:** edge | **Priority:** low

### Steps
1. Type a 200-character string into `[data-testid="input-movie-name"]`
2. Read the value back
3. Assert the value length matches the input length

---

## INP_012 — Field state resets after a page refresh

**Expected:** Reloading restores inputs to their initial values  
**Type:** edge | **Priority:** low

> **Note:** Client-only input state should not persist across reloads.

### Steps
1. Type into a field and confirm the value changed
2. Reload the page
3. Assert the field returns to its initial value
