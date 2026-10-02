"""Pyskills are tool modules that Python packages register so you can find them without importing everything. `list_pyskills()` names the ones installed, with a one-line description each, and needs no imports. Load one with a normal import, then read its docs with `doc()`.

# Finding skills

Normally load with `from <module> import *`: `__all__` selects the intended API. Hosts can also expose folder-local skills from `_pyskills/` dirs in the dialog's opening folder and its ancestors; they appear in the same listing and import normally. Their scope follows the opening folder, not a later cwd change; the host selects it, and discovery grants no tool permissions.

When several pyskills could fit, read `doc()` for each: one-line descriptions may not show which inputs they support (e.g. `fastcore.tools` for plain text/files, `aidialog.dlgskill` for notebooks/dialogs). Prefer `exhash.skill` for text editing when available. To build and register your own: `from pyskills import createskill; doc(createskill)`.

# Reading docs

You MUST read the full `doc()` of each function, class, method, and magic before its first use, unless its FULL uncompacted `doc()` output is visible in the conversation. A trailing `…` on an overview row marks omitted docments or usage notes. A row without it is the full doc. For a magic, doc the function that implements it, as named in its skill's docs. You MUST re-read any doc, module overviews included, when its earlier output is no longer visible. A kernel restart alone is no reason to re-read.

`doc()` works on any module, not just pyskills. Read at increasing detail: module, then class or namespace, then each callable. Pass several objects to one `doc()` call:

    import pyskills.skill
    doc(pyskills.skill)                            # module overview: classes, functions, submodules
    doc(SkillTestClass, skill_test_func)           # class overview and full function documentation

`doc(Class)` gives constructor docs plus a method overview. For generated or bound APIs, doc the instance (`doc(page)`, `doc(api.group)`, then `doc(page.goto)`/`doc(api.group.operation)`). A class can't show per-instance operations or their bound defaults. Doc properties on the class rather than evaluating the getter.

A literal `...` in a displayed body is a placeholder. A `**name` collector other than `**kwargs` is a shared param group: its params are listed once under `## shared params:` and passed as ordinary keyword args. Custom displays (e.g. fastspec groups) give their own drill-down guidance.

For APIs too large for `doc()`, `xdir(sym, q=None)` lists public names, filtered by an optional case-insensitive regex (e.g. `xdir(page.emulation, 'viewport')` for a fastcdp CDP domain's viewport names); `doc()` the match before calling it. `info_md(obj, source=False)` (from `ipykernel_helper`, preloaded by clikernel startup where installed) renders IPython's `?` (`??` with `source=True`) as markdown: use it for an object's real signature, docstring, and source together, not `inspect.getsource`/`inspect.signature`/bare `?`/`??`.

# Using results

Get the result you need from the API rather than post-processing its output: before `split`, `join`, slices, or comprehensions, check `doc()` for a parameter or function that answers directly; if none exists, propose extending the module rather than writing ad hoc code. Check parameter docs before converting arguments with `str()`/`expanduser()`, escaping text, or joining paths: the call may already handle them. Tell the user when convenient argument handling is missing or undocumented; improving the tool or its docs comes before working around it.

End cells with the result as a bare expression: `print(...)` stringifies it and loses its custom display. If printing or reformatting would read better, fix the repr or tell the user rather than silently working around it. Summarise what docs or results say rather than dumping them, unless the user needs it all.
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
