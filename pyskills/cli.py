"Command-line access to pyskills documentation and host skill stubs."

import pydoc
from fastcore.script import call_parse
from fastcore.meta import delegates
from .core import doc, export_skills


def _locate(sym):
    if (res := pydoc.locate(sym)) is None: raise SystemExit(f"Symbol not found: {sym}")
    return res


@call_parse
def doc_cli(
    sym:str, # Dotted Python symbol
    all:bool=False, # Include module symbol listings normally elided from `doc()`?
):
    "Render LLM-friendly documentation for importable Python symbols."
    print(doc(_locate(sym), all=all))


@call_parse
@delegates(export_skills)
def export_cli(
    dest:str, # Host skills directory, such as ~/.claude/skills
    **kwargs
):
    for k,names in export_skills(dest, **kwargs).items():
        if names: print(f'{k}: {" ".join(names)}')
