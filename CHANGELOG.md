# Release notes

<!-- do not remove -->

## 0.0.18

### New Features

- Refactor line-range APIs: make `replace_lines`/`str_replace` default to whole-file scope, require explicit bounds for `del_lines`, and consolidate `_norm_lines` helper ([#35](https://github.com/AnswerDotAI/pyskills/issues/35))


## 0.0.17

### New Features

- Add `__allow__` protocol, callable instance support, and audit event to `allow()` ([#34](https://github.com/AnswerDotAI/pyskills/issues/34))
- Add `view_cells` for displaying multiple cells at once; wrap `view_nb` and `find_cells` output in `PrettyString` ([#33](https://github.com/AnswerDotAI/pyskills/issues/33))


## 0.0.16

### New Features

- Add `create_notebook`, improve `str_replace` errors with context, default `find_cells` context to 1 ([#32](https://github.com/AnswerDotAI/pyskills/issues/32))


## 0.0.15

### New Features

- Add `use_regex` mode to `str_replace`/`strs_replace` ([#31](https://github.com/AnswerDotAI/pyskills/issues/31))


## 0.0.14

### New Features

- Add `find_cells` to ipynb skill with header/section/search filtering, and `view_cell`/`view_nb` truncation and range options ([#30](https://github.com/AnswerDotAI/pyskills/issues/30))


## 0.0.13

### New Features

- Add cell copy/cut/paste and `only_errors` `view_nb` ([#29](https://github.com/AnswerDotAI/pyskills/issues/29))
- Add `summary_nb` for one-line-per-cell notebook overview ([#28](https://github.com/AnswerDotAI/pyskills/issues/28))


## 0.0.12

### New Features

- Add `add_cell` and `del_cells` notebook editing functions ([#27](https://github.com/AnswerDotAI/pyskills/issues/27))


## 0.0.11

### New Features

- Remove pyskills.files module and simplify edit/ipynb docstrings ([#26](https://github.com/AnswerDotAI/pyskills/issues/26))
- clamp `file_view` endline ([#23](https://github.com/AnswerDotAI/pyskills/issues/23))


## 0.0.10

### New Features

- Use PrettyString ([#21](https://github.com/AnswerDotAI/pyskills/issues/21))
- Add `fmt_sig` helper to strip module names from signature annotations ([#20](https://github.com/AnswerDotAI/pyskills/issues/20))
- Split file search/create/view into new pyskills.files module ([#17](https://github.com/AnswerDotAI/pyskills/issues/17))
- resolve symbol strings in xdir, doc, and docfind ([#15](https://github.com/AnswerDotAI/pyskills/pull/15)), thanks to [@ncoop57](https://github.com/ncoop57)
- Split out ipynb; remove unneeded async ([#14](https://github.com/AnswerDotAI/pyskills/issues/14))


## 0.0.9

### New Features

- Wrap allowed callables with fastaudit.core.`track_call` in `allow` ([#13](https://github.com/AnswerDotAI/pyskills/issues/13))
- Refactor AllowPolicy to accept data dict instead of `ok_dests` parameter ([#12](https://github.com/AnswerDotAI/pyskills/issues/12))
- Support per-callable allow policies in dict form and resolve module via `__globals__` ([#11](https://github.com/AnswerDotAI/pyskills/issues/11))


## 0.0.8

### Bugs Squashed

- Currently `_doc_module` hardcodes function def which loses sync/async info and causes AI to not await an async function
- Added missing `shutil` import
- Removed export marker from the first note msg in `edit` dialog which was causing it to appear twice in the docstring


## 0.0.7

### New Features

- Harden `ep_desc` against import errors and filter None entries from `list_pyskills` ([#8](https://github.com/AnswerDotAI/pyskills/issues/8))

### Bugs Squashed

- fix `chk_dest` expand user ([#7](https://github.com/AnswerDotAI/pyskills/pull/7)), thanks to [@KeremTurgutlu](https://github.com/KeremTurgutlu)


## 0.0.6

### New Features

- Add pyskills.edit ([#6](https://github.com/AnswerDotAI/pyskills/issues/6))
- Improve `ensure_pyskills_dir` to try all site-packages paths with permission fallback ([#5](https://github.com/AnswerDotAI/pyskills/issues/5))


## 0.0.4

### New Features

- Add `can_render` check to doc() ([#4](https://github.com/AnswerDotAI/pyskills/issues/4))


## 0.0.3

### New Features

- Add xdir() and docfind() functions, refactor doc() and `_doc_module`() for improved module/class/instance inspection with submodule support ([#3](https://github.com/AnswerDotAI/pyskills/issues/3))


## 0.0.2

### New Features

- Add support for class method resolution in `allow()` via `__objclass__` and `__qualname__` ([#2](https://github.com/AnswerDotAI/pyskills/issues/2))


## 0.0.1

- init release


