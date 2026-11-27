r"""Python packages register tool modules as pyskills. `list_pyskills()` lists installed skills and one-line descriptions without imports. Load a module with a normal import, then read `doc(module)`.

### Finding skills

- session start, post-compaction: `list_pyskills()` and `doc()` baseline skills
- task-specific skills, modules: MUST `doc()` matching `list_pyskills()` entries (writing, review, style guides too, not only libraries) before first related task; skip while full uncompacted output in view
- load: normally `from <module> import *`    /`__all__` is the API
- `_pyskills/` in dialog's opening folder or an ancestor: listed, imported normally, where host exposes them; host fixes scope, cwd changes don't move it
- discovery grants no tool permissions
- several fit: `doc()` each    /descriptions may omit inputs: `fastcore.tools` plain text, files; `aidialog.dlgskill` notebooks, dialogs
- text editing: prefer `exhash.skill` where installed
- creating, registering a skill: `doc(pyskills.createskill)`

### Reading docs

- MUST `doc()` each function, class, method, magic in full before first use, unless full uncompacted output in view; reread when out of view, overviews too; restart alone: no reason; any module
- order: module, class or namespace, callables; batch: `doc(a, b)`
- generated or bound API: instance, then op: `doc(page)`, `doc(page.goto)`    /class lacks per-instance ops, bound defaults
- property: doc on class, unevaluated; magic: its implementing function, named in skill's docs
- overview row: ending `…`: notes omitted, else full doc; `...` in body: placeholder
- `**name` other than `**kwargs`: shared params, under `## shared params:`; pass as keywords
- too big for `doc()`: `xdir`; doc the match before calling
- signature, docstring, source: `info_md`, not `inspect.getsource`, `inspect.signature`, bare `?`, `??`

### Using results

- before post-processing output or converting args (e.g. `split`, slices, `str()`, `expanduser()`, path joins): `doc()` for a parameter or function doing it; none or undocumented: tell user, propose extending module, no ad hoc code    /tools, docs improve before workarounds
- cell ends with result bare    /`print` loses custom display
- would read better printed or reformatted: fix repr or tell user; no silent workaround
- summarize docs, results unless user needs all
"""

# inspect is unused - imported to show that non-owned submodules aren't listed in doc/xdir
import pyskills.createskill, inspect # chkstyle: ignore

__docs__ = {'Docs': ['pyskills.core', 'pyskills.llms', 'pyskills.createskill']}

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
