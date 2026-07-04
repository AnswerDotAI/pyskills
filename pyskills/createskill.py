"""How to create a pyskills pyskill module.

A pyskill is a standard Python module that registers itself via entry points so LLM hosts can discover and load it.

## 1. Create your module

Your module needs:
- A docstring: first paragraph is the short description shown during discovery; the rest is read by the LLM after loading.
- `__all__` (optional): if provided, `doc()` and `xdir()` show exactly these symbols. Otherwise they fall back to non-private names defined in the module (not just imported), plus explicitly imported sibling submodules.

## 2. Register via entry point

In your `pyproject.toml`:

    [project.entry-points.pyskills]
    my_skill = "mypackage.mymodule"

The key is an arbitrary name; the value is the module path.

## 3. Module contract summary

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

## 4. Local pyskills without packaging

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
