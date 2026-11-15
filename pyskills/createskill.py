# NB: this file is designed for an LLM reader, not a human. Add it to your LLM's context and ask it to explain.
"""How to create a pyskills pyskill module.

## Module and entry point

- docstring: first paragraph = catalog entry, all that's read before import; rest: through `doc(module)`
- `__all__`: optional; curate it: your public API    /consumers `import *`
- `doc()`, `xdir()` list `__all__`, else non-private names defined (not just imported) in the module; plus sibling submodules it explicitly imports
- entry point, in `pyproject.toml`:

```toml
[project.entry-points.pyskills]
my_skill = "mypackage.mymodule"    # key: any name
```

## What goes where

- module docstring: pieces, how they fit, workflow, shared constraints, which to use when; point to pieces' `doc()`; no parameters, inventories, defaults, result fields, per-operation recipes    /`doc(module)` lists the API
- skill and API docs together: every tool-specific behaviour, limit, failure mode and default
- parameter contracts: docments, beside the signature
- operation docstring: operation-wide behaviour, errors, when to use, result structure; result fields there or in the result type's docs
- explanations, executable lessons: notebook narrative; nbdev: `doc(nbdev.skill)` before editing
- say why readers must inspect the live object, in your domain's terms: browser: input events, readiness, resource ownership decide which operation fits; API client: generated parameters, bound account and repository defaults are on the instance, not the class
- custom namespace display (e.g. fastspec groups): explain how to descend

## Dynamic APIs

- `__dir__`: truthful, safe: supported names, runs no operation
- generated callable: effective signature as `__signature__`, with its name and instance-specific docs
- `Annotated` descriptions: carried with generated parameters into `docments` and delegated wrappers
- never document an operation via `type(operation).__call__`    /loses generated signature, defaults
- `_repr_markdown_`: `doc()` keeps it: use where a namespace or generated object has a useful doc view; result whose display shows data (e.g. accessibility tree): point readers to its type's docs; plain functions, methods: none needed

## Check the rendered result

- read real `doc()` output, not source: module, representative classes, bound methods, returned objects, generated operations, long operation docs in full; notes, parameter docs, async usage, result lifetimes visible where a reader needs them
- shortening a skill: each removed fact must stay findable: move missing contracts into their owning API docs first; keep the short, domain-specific discovery workflow
- discovery or rendering gap: fix it; never a manual inventory as workaround
- generated clients: check docs on locally built objects where no request is needed    /documenting mustn't spend tokens, change remote state or open a browser

## Without packaging

- folder-local, where host enabled them: each public top-level `.py` module or package (`__init__.py`) in `_pyskills/` of the opening folder or an ancestor; written like an installed skill, without `pyproject.toml`, install or entry point; package submodules: implementation; `_name`: private
- host: `enable_local_skills(opening_folder)` at startup, before its tool layer (Solveit: dialoghelper bootstrap); scope stays fixed when a live dialog moves; scope, duplicate names, conflicts, new files: `doc(enable_local_skills)`, `doc(pyskills.core)`
- user-wide (quick personal skills; skills shared across isolated environments, e.g. separate uv venvs): `pyskills_dir()`, typically `~/.local/share/pyskills/`; first `import pyskills` in an environment creates it and adds a `.pth` to `site-packages`    /its modules then import wherever pyskills is imported
- `register_pyskill('my_local.skill', docstring, code=module_source)`: adds one there; `disable_pyskill`, `enable_pyskill`: hide, show, files kept
"""
