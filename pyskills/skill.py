"""Python packages register tool modules as pyskills. `list_pyskills()` lists installed skills and one-line descriptions without imports. Load a module with a normal import, then read `doc(module)`.

# Finding skills

Normally use `from <module> import *`; `__all__` selects the intended API. Hosts can expose `_pyskills/` modules from a dialog's opening folder and ancestors; they appear in the listing and import normally. The host selects that scope; later cwd changes do not change it. Discovery grants no tool permissions.

When several skills could fit, read each `doc()`: descriptions may omit supported inputs (e.g. `fastcore.tools` for plain text/files, `aidialog.dlgskill` for notebooks/dialogs). Prefer `exhash.skill` for text editing when available. To create/register skills: `from pyskills import createskill; doc(createskill)`.

# Reading docs

You MUST read full `doc()` for each function, class, method and magic before first use, unless its FULL uncompacted output is visible in the conversation. You MUST reread any doc, including module overviews, when its earlier output is no longer visible; a kernel restart alone is no reason. A trailing `…` on an overview row marks omitted docments/usage notes; rows without it contain the full doc. For magics, doc the implementing function named in the skill's docs.

`doc()` works on any module, not just pyskills. Read module, then class/namespace, then each callable. Batch objects in one call:

    import pyskills.skill
    doc(pyskills.skill)                  # classes, functions, submodules
    doc(SkillTestClass, skill_test_func) # class overview and full function docs

`doc(Class)` gives constructor docs and a method overview. For generated/bound APIs, doc the instance (`doc(page)`, `doc(api.group)`), then its operation (`doc(page.goto)`, `doc(api.group.operation)`): classes cannot show per-instance operations or bound defaults. Doc properties on the class rather than evaluating getters.

A literal `...` in a displayed body is a placeholder. A `**name` collector other than `**kwargs` is a shared param group: its params are listed once under `## shared params:` and passed as ordinary keyword args. Custom displays (e.g. fastspec groups) give their own drill-down guidance.

For APIs too large for `doc()`, `xdir(sym, q=None)` lists public names with an optional case-insensitive regex filter (`xdir(page.emulation, 'viewport')` for fastcdp CDP viewport names); doc the match before calling. `info_md(obj, source=False)` renders IPython `?` (`??` with `source=True`) as Markdown: use it for the real signature, docstring and source together, not `inspect.getsource`/`inspect.signature`/bare `?`/`??`.

# Using results

Get the needed result from the API rather than post-processing its output: before `split`, `join`, slices or comprehensions, check `doc()` for a parameter/function answering directly; if none exists, propose extending the module rather than writing ad hoc code. Before converting arguments with `str()`/`expanduser()`, escaping text or joining paths, check parameter docs: the API may handle them already. Tell the user about missing/undocumented convenient argument handling; improving tool/docs comes before workarounds.

End cells with the result bare: `print(...)` stringifies it and loses its custom display. If printing/reformatting would read better, fix the repr or tell the user rather than silently work around it. Summarize docs/results unless the user needs them all.
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
