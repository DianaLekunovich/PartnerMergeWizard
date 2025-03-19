# Odoo Wizard Assignment

## Goal

Create a **custom Odoo module** that adds a wizard (transient model) for merging duplicate partners (`res.partner`). This wizard should allow users to select multiple partners from the list view, open a form (wizard), choose one "main" partner, and merge all the others into that main record.

## Functional Description

1. **Selecting Records:**
   - The user opens the **Contacts** (`res.partner`) list view and selects multiple partner records (duplicates) using the checkboxes.

2. **Launching the Wizard:**
   - From the **Action** menu (or a server action), the user chooses something like **"Merge Selected Partners"**.
   - This triggers an action that opens the wizard form in a popup (modal).

3. **Wizard Form:**
   - The form should show:
     - A field (Many2many) containing the selected partner records (`partner_ids`).
     - A field (Many2one) for the **Main Partner** (`main_partner_id`), which is the record into which all duplicates will be merged.
   - Optionally, display some details about each selected partner in read-only mode, if desired.

4. **Merging Logic:**
   - Once the user clicks **"Merge"** (or a similar button), the wizard should:
     - Verify that there is more than one partner in `partner_ids` (otherwise merging makes no sense).
     - Reassign any related objects (e.g., sales orders, invoices, etc.) from the duplicate partners to the main partner.  
       *In a real scenario, you’d identify all models referencing `res.partner` and update their `partner_id` fields. For the purpose of this exercise, you can demonstrate the concept by handling just one or two models—like `sale.order` or `account.move`—or provide an explanation of how you would do so.*
     - Archive (set `active = False`) or delete the duplicate partner records, except for the `main_partner_id`.
     - Return a success message or close the wizard window to indicate the operation completed.

5. **Error Handling and Validation:**
   - If the user only selects one partner, display an error (e.g., "You must select at least two partners to merge").
   - If any part of the merging process fails (for instance, if there are permissions issues or concurrency conflicts), show a user-friendly message.

## Technical Requirements

1. **Module Structure:**
   - Create a folder for your module, e.g., `partner_merge_wizard/`.
   - Include:
     - `__manifest__.py`
     - `__init__.py`
     - A `wizard/` folder containing the wizard model definition.
     - A `views/` folder containing the XML definitions for the wizard form view, actions, and menus (if needed).

2. **Server Action or Menu Item:**
   - To allow users to open the wizard from the partner tree view, define a server action that references your wizard.
   - Alternatively, you can create a dedicated menu item if that fits your workflow.

## Validation & Testing

1. **Install the Module** in your Odoo environment.
2. Navigate to **Contacts** → **Customers** (the list of partners).
3. Select 2 or more partner records that you want to merge.
4. Click **Action** → **Merge Selected Partners**.
5. In the wizard:
   - Confirm the list of selected partners (`partner_ids`).
   - Choose one partner as the **Main Partner** (`main_partner_id`).
6. Click **Merge**.
7. Verify that:
   - All references to the selected (duplicate) partners in the chosen model(s) now point to the main partner.
   - The duplicate partners are either archived or deleted.

## Additional Features (Optional)

- **Conflict Resolution:** If the selected partners have different fields (e.g., different emails), prompt the user to choose which email to keep.
- **Multi-lingual Support:** Add translations for wizard labels, error messages, and button texts.
- **Chatter Logging:** Post a message in the main partner’s chatter summarizing the merge operation.
- **Security Rules:** Restrict merging to users with certain rights (e.g., those belonging to a specific group).

---

### Evaluation Criteria

1. **Module Structure & Organization**  
   - Correct placement and naming of files (`__manifest__.py`, `__init__.py`, wizard folder, views folder).

2. **Wizard Implementation**  
   - Proper use of `TransientModel` and its context (`active_ids`).
   - Clear data flow from selected records to the wizard form.

3. **Merging Logic**  
   - Appropriate validation (at least two partners, must choose a main partner).
   - Reassignment of related data from duplicates to the main partner.
   - Archiving or removing duplicates.

4. **User Experience**  
   - Straightforward wizard interface.
   - Meaningful feedback or error messages.

5. **Readability & Maintainability**  
   - Clean code, proper comments, and descriptive variable/method names.

