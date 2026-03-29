"""Pyskills is a plugin system allowing Python packages to register "skills" (units of LLM-usable functionality) via standard Python entry points. An LLM host (e.g. solveit) discovers available pyskills without importing them, reads lightweight descriptions via AST inspection, and selectively loads chosen pyskills into context using standard imports.

## Discovery

Call `list_pyskills()` to get a `{module: description}` dict of all registered pyskills. No imports needed. The descriptions are the first line of the module docstrings.

## Loading a pyskill

Use standard Python import, then `doc()` to inspect at increasing detail:

    import pyskills.skill
    doc(pyskills.skill)        # module overview: classes, functions, and what's callable
    doc(SkillTestClass)        # class detail: bases, __init__, methods, properties
    doc(skill_test_func)       # function detail: full signature with docments

NB: `doc()` works on *all* python modules, not only pyskills. The only thing that's special about pyskills is the entrypoint registration that makes them appear in `list_pyskills()`; they can cross-reference other modules that may not be listed, but can still be imported and `doc()` run.

## Permissions

The module-level `doc()` output ends with an `allows:` section listing exactly which functions and classes you may call. Calling anything not listed will raise an error. The allows notation:

- `allow(func, func2)` : `func` and `func2` are callable
- `allow({SomeClass: ['method1', 'method2']})` : those specific methods of SomeClass
- `allow({SomeClass: ...})` : all public methods of `SomeClass`

## Testing

This module includes a test class and function to verify the system works:

    import pyskills.skill
    doc(pyskills.skill.SkillTestClass)
    doc(pyskills.skill.skill_test_func)

## Creating pyskills

`from pyskills import createskill; doc(createskill)` for how to build and register your own pyskill modules, including the allow/policy system.
"""

from pyskills.core import allow

__all__ = ['allow', 'SkillTestClass', 'skill_test_func']

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

allow(skill_test_func, SkillTestClass)

