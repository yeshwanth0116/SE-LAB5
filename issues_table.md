# Identified Issues and Fixes

| Issue Type | File:Line(s) | Severity | Description | Suggested Fix |
|---|---:|---:|---|---|
| Dangerous mutable default | inventorysystem.py:8 | Medium (pylint W0102) | Function `addItem` used a mutable default argument `logs=[]` which is shared across calls and can lead to unexpected state. | Change default to `None` and create a new list inside the function (e.g., `if logs is None: logs = []`). Use snake_case naming (`add_item`). |
| Bare except / swallow errors | inventorysystem.py:19 | Low/Medium (bandit B110, flake8 E722) | A bare `except:` silently ignores all exceptions (including SystemExit/KeyboardInterrupt) and makes debugging difficult. | Catch specific exceptions (e.g., `except KeyError:`) and log the error. Avoid swallowing exceptions. |
| Unsafe eval usage | inventorysystem.py:59 | Medium (bandit B307) | `eval("print('eval used')")` executes arbitrary code which is dangerous and a security risk. | Remove `eval` usage or replace with `ast.literal_eval` if evaluating trusted literals; in this case replace with a safe logging call. |
| File handling without context manager / encoding | inventorysystem.py:26,32 | Medium (pylint W1514 / R1732) | Files opened with `open()` and closed manually; no explicit encoding specified which may lead to platform differences and leaks if exception occurs. | Use `with open(filename, 'r', encoding='utf-8') as f:` and `json.load`/`json.dump` to safely handle files and specify encoding. |

Notes:
- Initial reports also flagged many style issues (naming, missing docstrings, unused imports). I focused on security/functional issues and the most impactful quality problems.
