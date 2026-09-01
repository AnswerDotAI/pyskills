"""Python-native skills system

pyskills is a plugin system that lets Python packages register "skills" (units of LLM-usable functionality) via standard [entry points](https://packaging.python.org/en/latest/specifications/entry-points/). An LLM harness (e.g. solveit) discovers available pyskills without importing them, reads lightweight descriptions via AST inspection, and selectively loads chosen pyskills into context using standard imports.

It includes `list_pyskills()` for discovery, `doc()` for rendering module/class/function documentation in LLM-friendly format, `xdir()` for listing a module or class's public symbols, and an `allow()` system for registering safe callable access in sandboxed environments. Skills can be installed as regular packages with entry points, or dropped into an XDG data directory for quick local use.

Modules:

- `pyskills.core`: Skill discovery, LLM-friendly doc rendering, the allow registry, and pyskill registration
- `pyskills.createskill`: How to create a pyskills pyskill module.
- `pyskills.skill`: Pyskills are tool modules that Python packages register so you can find them without importing everything. `list_pyskills()` names the ones installed, with a one-line description each, and needs no imports. Load one with a normal import, then read its docs with `doc()`."""

__version__ = "0.0.29"
from .core import *
