"""How to create a pyskills pyskill module.

A pyskill is a standard Python module that registers itself via entry points so LLM hosts can discover and load it.

## 1. Create your module

Your module needs:
- A docstring: first paragraph is the short description shown during discovery; the rest is read by the LLM after loading.
- `__all__`: lists the symbols available to the LLM.
- `allow()` calls: declares what the LLM is permitted to call.

## 2. Register via entry point

In your `pyproject.toml`:

    [project.entry-points.pyskills]
    my_skill = "mypackage.mymodule"

The key is an arbitrary name; the value is the module path.

## 3. Use `allow()` to declare permissions

`allow()` populates `__pytools__`, a `defaultdict(set)` mapping modules/classes to permitted callable names. The LLM host enforces these at call time.

    from pyskills.core import allow

    allow(func1, func2)                          # register standalone functions
    allow({SomeClass: ['method1', 'method2']})    # register specific methods
    allow({SomeClass: ...})                       # register all public methods

## 4. Allow policies for write-guarded operations

For operations that write to the filesystem, attach an `AllowPolicy` to constrain calls by destination path:

    from pyskills.core import allow, PosAllowPolicy, PathWritePolicy, OpenWritePolicy

    allow(my_write_func, allow_policy=PosAllowPolicy(0))

Three built-in policies:
- `PosAllowPolicy(pos, kw)`: check that a positional or keyword arg is under allowed destination paths.
- `PathWritePolicy(target_pos, target_kw)`: check the Path object itself, and optionally a target arg.
- `OpenWritePolicy()`: check open() calls only when mode includes w/a/x/+.

Policies are stored as `(name, AllowPolicy)` tuples in `__pytools__`. The host passes its allowed destination list at call time.

## 5. Module contract summary

    '''Short description for discovery.

    Detailed docs read by the LLM after import.
    '''

    from pyskills.core import allow

    __all__ = ['my_func', 'MyClass']

    def my_func(x: int) -> str:
        "Does something useful"
        ...

    class MyClass:
        "A useful class"
        def method(self) -> str:
            "Does something"
            ...

    allow(my_func, {MyClass: ...})

## 6. Local pyskills without packaging

The entry point approach above requires a full package install. For quick personal pyskills, or pyskills shared across projects with isolated environments (e.g. separate uv venvs), pyskills provides an XDG-based pyskills directory.

When you first `import pyskills`, it creates a directory at your XDG data home (typically `~/.local/share/pyskills/`) and writes a `.pth` file into `site-packages`. This `.pth` file tells Python to add the pyskills directory to `sys.path` on startup, so any modules placed there are importable as standard Python modules without any special import machinery. This works across all Python environments on your system, even separate uv projects with isolated venvs.

You can create a pyskill programmatically with `register_pyskill`:

    from pyskills.core import register_pyskill

    register_pyskill('my_local.skill', 'A quick local pyskill.', code='''
    from pyskills.core import allow

    __all__ = ['hello']

    def hello(name: str) -> str:
        "Greet someone"
        return f"Hello, {name}!"

    allow(hello)
    ''')

This writes the module file into the XDG pyskills directory and creates a minimal dist-info entry point, so the pyskill immediately appears in `list_pyskills()`.

Use `enable_pyskill(name)` / `disable_pyskill(name)` to toggle a pyskill's visibility without deleting files. Use `pyskills_dir()` to see where the directory is.
"""
