"Command-line access to pyskills documentation."

import pydoc
from fastcore.script import call_parse
from .core import doc


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
