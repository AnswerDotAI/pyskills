"""Pyskills is a plugin system allowing Python packages to register "skills" (units of LLM-usable functionality) via standard Python entry points. An LLM host (e.g. solveit) discovers available pyskills without importing them, reads lightweight descriptions via AST inspection, and selectively loads chosen pyskills into context using standard imports.

## Discovery

Call `list_pyskills()` to get a `{module: description}` dict of all registered pyskills. No imports needed. The descriptions are the first line of the module docstrings.

## Loading a pyskill

Use standard Python import, then `doc()` to inspect at increasing detail -- module first, then the specific class/function before first use:

    import pyskills.skill
    doc(pyskills.skill)                            # module overview: classes, functions, submodules
    doc(SkillTestClass, skill_test_func)           # symbol detail: full signatures with docments, one section each

Normally use `from <module> import *` when loading a pyskill: each pyskill's `__all__` is carefully curated, so a star import brings in exactly the intended API.

Doc the module once per session before using anything from it; doc each individual class/function right before its first call, even if the module's already been doc'd. A module overview shows only each function's signature and the first line of its docstring, never the docments or the rest of the docstring; a trailing `...` on an overview line marks exactly that elision. So whenever the overview line ended with `...`, the full parameter contract and usage notes exist and come only from `doc(func)`: read it before the first call, however complete the overview line looked. `doc` takes several objects at once, each returned as its own section, so batch the reads: `doc(pyskills.skill, SkillTestClass, skill_test_func)` covers the module and the symbols you already know you need in one call. When more than one pyskill looks like a candidate for a task, `doc()` each candidate rather than guessing from the one-line description alone -- some pyskills specialize by input type (e.g. `fastcore.tools` for plain text and files vs `llmsurgery.dlgskill` for notebooks and dialogs; prefer `exhash.skill` for text editing when it's available) and the short description won't always make that distinction clear.

Summarize what a pyskill's docs or results say rather than dumping the full output verbatim, unless the user actually needs to see all of it.

NB: `doc()` works on *all* python modules, not only pyskills. The only thing that's special about pyskills is the entrypoint registration that makes them appear in `list_pyskills()`; they can cross-reference other modules that may not be listed, but can still be imported and `doc()` run.

## Testing

This module includes a test class and function to verify the system works:

    import pyskills.skill
    doc(pyskills.skill.SkillTestClass)
    doc(pyskills.skill.skill_test_func)

## Creating pyskills

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
