"""How to create a pyskills pyskill module.

A pyskill is a standard Python module that registers itself via entry points so LLM hosts can discover and load it.

## 1. Module

- Docstring: its first paragraph is the discovery description; the rest is read after loading.
- `__all__` (optional): `doc()`/`xdir()` show these plus sibling submodules the module explicitly imports; without it, non-private names defined (not just imported) in the module plus those submodules. Consumers `import *` from pyskills, so `__all__` is your public API: curate it.

## 2. Entry point

In `pyproject.toml` (key: any name; value: module path):

    [project.entry-points.pyskills]
    my_skill = "mypackage.mymodule"

## 3. Documentation where it's used

The module docstring gives the higher-level picture (pieces, how they fit, workflow, shared constraints, when to use which) and points to each piece's `doc()`. Function-specific detail goes in that function's docstring and docments: don't repeat parameter descriptions, method inventories, defaults, result fields, or per-operation recipes in the module docstring (`doc(module)` already lists the API). Together, the module docstring and API docs must cover every tool-specific behaviour, including limits, failure modes, and defaults.

Tell readers to inspect the actual object before using it, and say why for your skill (browser control: input events, readiness, and resource ownership change which operation fits; API clients: generated parameters and bound account/repository defaults belong to the instance, not its class). Progressive discovery:

    doc(skill)                       # scope and shared workflow
    doc(Client)                      # constructor and class overview
    doc(client)                      # the instantiated API
    xdir(client.group, 'query')       # names on a large surface
    doc(client.group.operation)      # full docs before the call

Class and namespace listings are overviews: `…` marks omitted detail, so read the chosen callable's full docstring and docments. Custom namespace displays (e.g. fastspec groups) explain how to descend. Inspect properties on their class rather than evaluating them for docs.

Placement: parameter-specific contracts in docments beside the signature; operation-wide behaviour, errors, usage conditions, and result structure in the operation's docstring; returned fields described there or via the type's docs; explanations and executable lessons in the notebook narrative. In nbdev projects, read `nbdev.skill` before editing the source notebook; never edit generated modules.

Dynamic APIs: keep `__dir__` truthful and safe to call (supported names, without doing the operations); carry the effective signature on the callable as `__signature__`, with its name and instance-specific docs. `Annotated` metadata descriptions travel with generated parameters into `docments` and delegated wrappers. Don't document an operation via `type(operation).__call__`: that loses its generated signature and defaults.

`doc()` preserves `_repr_markdown_`: use it when a namespace or generated object already has a useful doc view. A result's custom display can show data instead (e.g. a browser accessibility tree); point readers to its type for API docs. Ordinary functions and methods need no custom rendering.

## 4. Review the rendered experience

Read actual `doc()` output, not just source docstrings: the module, representative classes, bound methods, returned objects, and generated operations, with long operation docs in full. Check that notes, parameter docs, async usage, and result lifetimes are visible where a reader needs them.

Before shortening a skill, identify where each removed fact will stay available, and move missing contracts to their owning API docs first. Fix discovery or rendering gaps rather than keeping a manual inventory as a workaround. Keep a short, domain-specific explanation of the discovery workflow in the skill.

Revise existing notebook examples to teach changed behaviour. Assert the useful contract, not a whole formatted output. Verify generated clients with locally constructed objects when no request is needed: documenting an API must not spend tokens, change remote state, or open a browser.

## 5. Module contract example

    '''Short description for discovery.

    Detailed docs read by the LLM after import.
    '''

    __all__ = ['my_func', 'MyClass']

    def my_func(x: int) -> str:
        "Does something useful"
        ...

    class MyClass:
        "A useful class"
        def method(self) -> str:
            "Does something"
            ...

After import, the LLM runs `doc(module)` (classes, functions, submodules) and `xdir(module)` (filtered public symbols).

## 6. Folder-local skills

With the host's folder-local skills enabled, put a public `.py` module, or a package with `__init__.py`, in `_pyskills/` under the dialog's opening folder or an ancestor. Each top-level module or package is a skill; package submodules are implementation modules, and leading-underscore names are private. Supply the same docstring and curated API as an installed skill; no `pyproject.toml`, install, or entry point is needed. `doc(pyskills.core)` covers duplicate names, conflicts with other modules, and picking up new files.

Hosts call `enable_local_skills(opening_folder)` at startup, before loading their tool layer (read its full docs first); Solveit's dialoghelper bootstrap does this. The scope stays fixed when cwd changes or a live dialog moves; a new kernel can select another folder. Discovery grants no permission to execute tools.

## 7. User-wide pyskills without packaging

For quick personal pyskills, or ones shared across projects with isolated environments (e.g. separate uv venvs), without a package install: the first `import pyskills` in an environment creates an XDG pyskills dir (typically `~/.local/share/pyskills/`) and writes a `.pth` into that environment's `site-packages` putting it on `sys.path`, so modules there import normally, with no special machinery. Every environment that imports pyskills adds the same dir, so its modules are shared across environments.

Create one with `register_pyskill`:

    from pyskills.core import register_pyskill

    register_pyskill('my_local.skill', 'A quick local pyskill.', code='''
    __all__ = ['hello']

    def hello(name: str) -> str:
        "Greet someone"
        return f"Hello, {name}!"
    ''')

`enable_pyskill(name)`/`disable_pyskill(name)` toggle visibility without deleting files; `pyskills_dir()` shows the directory.
"""
