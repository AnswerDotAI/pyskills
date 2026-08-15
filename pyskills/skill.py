"""Pyskills are tool modules that Python packages register so you can find them without importing everything. `list_pyskills()` names the ones installed, with a one-line description each, and needs no imports. Load one with a normal import, then read its docs with `doc()`.

Use `doc()` at increasing detail, module first, then the specific class or function before its first use:

    import pyskills.skill
    doc(pyskills.skill)                            # module overview: classes, functions, submodules
    doc(SkillTestClass, skill_test_func)           # symbol detail: full signatures with docments, one section each

Normally use `from <module> import *` when loading a pyskill: each pyskill's `__all__` is carefully curated, so a star import brings in exactly the intended API.

`doc()` returns a `PrettyString`. A bare final call is rendered by IPython; assigning the result is silent. Assign it when you do not want it rendered, for instance for very large docs you want to search through.

Doc the module once while its output is still visible in the conversation, then doc each class or function right before its first call. This is conversation state, not Python-process state: read it again when the earlier output is no longer visible, not merely because the kernel restarted.

In a module overview, a trailing `...` on a line means docments and usage notes exist beyond the signature and first docstring line, and only `doc(func)` shows them: read it before the first call, however complete the line looks. A line with no `...` is that function's whole doc. A `**name` collector (other than `**kwargs` itself) is a shared param group: its params are listed once under `## shared params:` and are passed as ordinary keyword args. `doc` takes several objects at once, each returned as its own section, so batch the reads.

When more than one pyskill looks like a candidate for a task, `doc()` each candidate rather than guessing from the one-line descriptions: some specialize by input type (e.g. `fastcore.tools` for plain text and files vs `aidialog.dlgskill` for notebooks and dialogs; prefer `exhash.skill` for text editing when it's available) and the short description won't always make the distinction clear.

Pyskill results are designed so the right call answers the question directly. Post-processing a result with generic Python (a `split`/`join`/slice/comprehension over its output) is a workaround smell: it usually means the call was wrong or a parameter was missed. Check `doc()` for the parameter or sibling function that answers directly; if it genuinely doesn't exist, propose extending the module rather than bridging with ad hoc code.

The same smell applies on the way in: wrapping an argument in `str()`, `expanduser()`, pre-escaping, or path-joining that the call already handles means either the docments weren't read or the tooling or its docs need fixing. Check the parameter before dressing the argument, and tell the user when the most ergonomic argument handling doesn't exist or isn't documented: improving tooling is always first priority.

Results are built to be read as their bare reprs: end the cell with the bare expression rather than `print(...)`, which flattens a tuned display to plain `str()`. If a bare result ever reads worse than a printed or reformatted version, the repr is deficient: fix it or tell the user, never quietly work around it.

Summarize what a pyskill's docs or results say rather than dumping the full output verbatim, unless the user actually needs to see all of it.

`doc()` works on *all* python modules, not only pyskills.

`xdir(sym, q=None)` complements `doc()`: it lists an object's public names, filtered by an optional case-insensitive regex. Use it when a module, class, or dynamic API surface is too big to `doc()` whole, e.g. `xdir(page.emulation, 'viewport')` on a fastcdp CDP domain, then `doc()` the match before calling it.

`info_md(obj, source=False)` (from `ipykernel_helper`, preloaded by clikernel startup where installed) is the third way to read an object: IPython's `?` -- or `??` with `source=True` -- rendered as markdown. Reach for it when you want an object's real signature, docstring, and source together, rather than `inspect.getsource`/`inspect.signature` or bare `?`/`??`.

`from pyskills import createskill; doc(createskill)` for how to build and register your own pyskill modules.
"""

# inspect is unused - imported to show that non-owned submodules aren't listed in doc/xdir
import pyskills.createskill, inspect # chkstyle: ignore

class SkillTestClass(str):
    """Some class.
    More info about it."""
    def __init__(self): ...

    def f(
        self,
        x:int=0 # the input
    )->str: # the output
        "A test method"

    @property
    def g(self)->str: "A test prop"

    def _g(): "ignore me"

def skill_test_func(
    x:int=0 # the input
)->str: # the output
    "A test function"
    return f"You call me with the arg: {x}"

async def async_skill_test_func(
    x:int=0 # the input
)->str: # the output
    "A test function"
    return f"You call me with the arg: {x}"
