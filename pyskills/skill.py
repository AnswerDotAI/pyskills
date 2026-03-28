"""Pyskills is a plugin system allowing Python packages to register "skills" — units of LLM-usable functionality — via standard Python entry points. An LLM host (e.g. solveit) discovers available skills without importing them, reads lightweight descriptions via AST inspection, and selectively loads chosen skills into context using standard imports. To get the details: `import pyskills.skill; pyskills.skill.__doc__`

This is where we'll add more details about it."""

class F(str):
    """Some class.
    More info about it."""
    def __init__(self): ...

    def f(
        self,
        x:int=0 # the input
    )->str: # the output
        "A test method"

    @property
    def g(self)->str:
        "A test prop"

    def _g():
        "ignore me"

def f(
    x:int=0 # the input
)->str: # the output
    "A test function"

