"""Pyskills are tool modules that Python packages register so you can find them without importing everything. `list_pyskills()` names the ones installed, with a one-line description each, and needs no imports. Load one with a normal import, then read its docs with `doc()`.

Use `doc()` at increasing detail: module, class or namespace, then the actual callable before its first use:

    import pyskills.skill
    doc(pyskills.skill)                            # module overview: classes, functions, submodules
    doc(SkillTestClass, skill_test_func)           # class overview and full function documentation

For generated or bound APIs, inspect the instance: `doc(page)`, `doc(api.group)`, then `doc(page.goto)` or `doc(api.group.operation)`. A class cannot show instance-generated operations or their bound defaults. `doc(Class)` includes constructor documentation and a method overview; methods still need their own read. Inspect properties on the class rather than evaluating a getter to document it.

Normally load a pyskill with `from <module> import *`. Its `__all__` selects the intended API.

`doc()` returns a `PrettyString`. A bare final call is rendered by IPython; assigning the result is silent. Assign it when you do not want it rendered, for instance for very large docs you want to search through.

Doc the module once while its output is still visible in the conversation, then doc each class or function right before its first call. This is conversation state, not Python-process state: read it again when the earlier output is no longer visible, not merely because the kernel restarted.

In an overview, a trailing `…` marks omitted docments or usage notes: read `doc(callable)` before the first call, however complete the summary looks. The literal `...` in a displayed function body is just a placeholder. Custom displays, such as fastspec groups, provide their own drill-down guidance. A `**name` collector (other than `**kwargs` itself) is a shared param group: its params are listed once under `## shared params:` and are passed as ordinary keyword args. `doc` takes several objects at once, so batch the reads.

When several pyskills could handle a task, read `doc()` for each. Their one-line descriptions may not distinguish the inputs they support. For example, use `fastcore.tools` for plain text and files, or `aidialog.dlgskill` for notebooks and dialogs. Prefer `exhash.skill` for text editing when available.

Use the pyskill API to get the result you need instead of post-processing its output. Before using `split`, `join`, slices, or comprehensions, check `doc()` for a parameter or another function that answers directly. If none exists, propose extending the module rather than writing ad hoc code.

Check the parameter docs before converting arguments with `str()` or `expanduser()`, escaping text, or joining paths. The call may already handle these. Tell the user when convenient argument handling is missing or undocumented. Prioritize improving the tool or its docs over working around the limitation.

End the cell with the result as a bare expression. `print(...)` converts the result to a string and loses its custom display. If printing or reformatting would make the result easier to read, fix its repr or tell the user. Don't work around a poor repr silently.

Summarize what a pyskill's docs or results say rather than dumping the full output verbatim, unless the user actually needs to see all of it.

`doc()` works on *all* python modules, not only pyskills.

Hosts can also expose folder-local skills from ancestor `_pyskills/` directories. These appear in the same listing and use ordinary imports. Their scope belongs to the dialog's opening folder, not its changing cwd. The host selects that scope; discovery does not grant tool permissions.

`xdir(sym, q=None)` lists an object's public names, filtered by an optional case-insensitive regex. Use it when a module, class, or dynamic API is too large to read with `doc()`. For example, `xdir(page.emulation, 'viewport')` finds viewport-related names in a fastcdp CDP domain. Read `doc()` for the matching object before calling it.

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
