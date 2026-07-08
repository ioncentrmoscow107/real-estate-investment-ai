# Property Workflow and Manual Overrides

TASK-009 adds the first sample/UI-only concept for editable property data, manual corrections, correction history, requested documents, and deal workflow status.

## Purpose

Listing data must not be treated as final truth. Public listing fields can be incomplete, outdated, optimistic, or changed during negotiations. Investor analysis needs a place to show what was originally listed and what was later clarified.

Manual overrides help separate:

- original listing data;
- manually confirmed or corrected values;
- source of confirmation;
- correction comment;
- correction timestamp.

## Data Model

`manual_overrides` stores the current corrected value by field:

```text
manual_overrides[field]:
  label
  original_value
  override_value
  source
  comment
  updated_at
```

`correction_history` stores an audit-style list of changes:

```text
correction_history[]:
  field
  label
  old_value
  new_value
  source
  comment
  changed_at
```

`property_workflow_status` tracks where the object is in the deal workflow:

- `new`;
- `interesting`;
- `in_review`;
- `documents_requested`;
- `egrn_check`;
- `negotiation`;
- `price_negotiation`;
- `rejected`;
- `archived`;
- `deal_pipeline`.

Each property also has:

- `property_workflow_status_label`;
- `workflow_next_action`;
- `requested_documents`.

`requested_documents` keeps a lightweight document checklist:

```text
requested_documents[]:
  title
  status
  status_label
  comment
```

Document statuses:

- `received`;
- `requested`;
- `missing`;
- `not_required`.

## Current Limitations

- Sample/UI-only.
- No database persistence.
- No real edit form.
- No authentication or user attribution.
- No document upload.
- No EGRN integration.

## Future Evolution

Later versions can add:

- real edit forms;
- backend save API;
- persistent correction audit log;
- user attribution;
- document upload and storage;
- EGRN/checklist integrations;
- deal pipeline board.
