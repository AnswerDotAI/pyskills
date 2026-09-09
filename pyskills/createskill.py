"""How to create a pyskills pyskill module.

A pyskill is a standard Python module that registers itself via entry points so LLM hosts can discover and load it.

## 1. Create your module

Your module needs:
- A docstring: first paragraph is the short description shown during discovery; the rest is read by the LLM after loading.
- `__all__` (optional): if provided, `doc()` and `xdir()` show exactly these symbols. Otherwise they fall back to non-private names defined in the module (not just imported), plus explicitly imported sibling submodules. Curate this carefully: consumers are told to `import *` from pyskill modules, so it defines your public API.

## 2. Register via entry point

In your `pyproject.toml`:

    [project.entry-points.pyskills]
    my_skill = "mypackage.mymodule"

The key is an arbitrary name; the value is the module path.

## 3. Put documentation where it is used

The module docstring teaches scope, shared constraints, and workflow. Do not repeat parameter descriptions, method inventories, defaults, result fields, or recipes for individual operations there. `doc(module)` already lists the public API.

Require readers to inspect the actual object before using it. State why this matters for your particular skill. For browser control, input events, readiness, and resource ownership change which operation is appropriate. For API clients, generated parameters and bound account/repository defaults belong to the instance, not its class.

Use progressive discovery:

    doc(skill)                       # scope and shared workflow
    doc(Client)                      # constructor and class overview
    doc(client)                      # the instantiated API
    xdir(client.group, 'query')       # names on a large surface
    doc(client.group.operation)      # full docs before the call

Class and namespace listings are overviews. Entries marked `…` have omitted detail. Read the selected callable's full docstring and docments. Custom namespace displays, such as fastspec groups, explain how to descend. Inspect properties on their class rather than evaluating them just to get documentation.

Put parameter-specific contracts in docments beside the signature. Put operation-wide behavior, errors, usage conditions, and result structure in the operation's docstring. Describe the returned object's fields or point to its type's documentation. Put explanations and executable lessons in the notebook narrative. In nbdev projects, read `nbdev.skill` before editing the source notebook; do not edit generated modules.

For dynamic APIs, keep `__dir__` truthful and safe to call. It should list supported names without doing the operations. Carry the effective signature on the callable as `__signature__`; keep its name and instance-specific documentation too. Descriptions in `Annotated` metadata travel with generated parameters into `docments` and delegated wrappers. Do not replace an operation with `type(operation).__call__` when documenting it: that loses its generated signature and defaults.

`doc()` preserves `_repr_markdown_` displays. Use that when a namespace or generated object already has a useful documentation view. A result's custom display can instead show data, such as a browser accessibility tree; direct readers to its type for API documentation. Ordinary functions and methods need no custom rendering.

## 4. Review the rendered experience

Read the actual `doc()` results, not just the source docstrings. Inspect the module, representative classes, bound methods, returned objects, and generated operations. Read long operation docs in full. Check that notes, parameter documentation, async usage, and result lifetimes are visible at the level where a reader needs them.

Before shortening an existing skill, identify where each removed fact will remain available. Move missing contracts to their owning API docs first. Fix discovery or rendering gaps instead of retaining a manual inventory as a workaround. Keep a short, domain-specific explanation of the discovery workflow in the skill.

Revise existing notebook examples to teach changed behavior. Assert the useful contract, not an entire formatted output. Verify generated clients using locally constructed objects when no request is needed; documenting an API must not require spending tokens, changing remote state, or opening a browser.

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

After import, the LLM inspects the module with `doc(module)` (overview of classes, functions, and submodules) and `xdir(module)` (filtered list of public symbols).

## 6. Folder-local skills

When the host enables folder-local skills, put a public `.py` module or a package with `__init__.py` in `PYSKILLs/` under the dialog's opening folder or one of its ancestors. Each top-level module or package is a skill. Package submodules are implementation modules; leading-underscore names are private. Supply the same module docstring and curated API as an installed skill. No `pyproject.toml`, installation, or manual entry-point registration is needed.

The nearest folder wins between local duplicates. Names conflicting with existing importable modules raise an error. Discovery reads docstrings without executing skill code. New files in the selected ancestor locations become discoverable, but imported modules retain normal Python caching.

Hosts call `enable_local_skills(opening_folder)` at startup, before loading their tool layer. Read its full docs first. Solveit's dialoghelper bootstrap does this automatically. The scope stays fixed when cwd changes or a live dialog moves; a new kernel can select a different folder. Discovery does not grant permission to execute tools.

## 7. User-wide pyskills without packaging

The entry point approach above requires a full package install. For quick personal pyskills, or pyskills shared across projects with isolated environments (e.g. separate uv venvs), pyskills provides an XDG-based pyskills directory.

When you first `import pyskills`, it creates a directory at your XDG data home (typically `~/.local/share/pyskills/`) and writes a `.pth` file into `site-packages`. This `.pth` file tells Python to add the pyskills directory to `sys.path` on startup, so any modules placed there are importable as standard Python modules without any special import machinery. This works across all Python environments on your system, even separate uv projects with isolated venvs.

You can create a pyskill programmatically with `register_pyskill`:

    from pyskills.core import register_pyskill

    register_pyskill('my_local.skill', 'A quick local pyskill.', code='''
    __all__ = ['hello']

    def hello(name: str) -> str:
        "Greet someone"
        return f"Hello, {name}!"
    ''')

This writes the module file into the XDG pyskills directory and creates a minimal dist-info entry point, so the pyskill immediately appears in `list_pyskills()`.

Use `enable_pyskill(name)` / `disable_pyskill(name)` to toggle a pyskill's visibility without deleting files. Use `pyskills_dir()` to see where the directory is.
"""
