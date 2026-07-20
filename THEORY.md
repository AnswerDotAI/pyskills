# The theory of the pyskills ecosystem

pyskills is a small plugin system with a big premise: give an LLM a real Python kernel, and let installed packages register capabilities it can discover, read about, and import. This file is the theory that follows from that premise, and a tour of the ecosystem built around it, written for people. It began as a collation of the module docstrings that agents load as their operational reference, and it evolves independently of them as we improve it.

In reading order:

- **The premise**: capabilities are importable functions in a persistent kernel, discovered without importing.
- **The media and their units**: lines, blocks, cells, and messages; what each word means, which layer it picks, and which units run.
- **Reading**: summaries locate, views read; `context=` counts the medium's units; results are reprs designed to be read bare.
- **Addressing**: edits say where by line number or by hash-verified lnhash; take addresses from the read; diffs verify the write.
- **The grammar**: two name shapes and one parameter vocabulary across every package.
- **The interpreter doctrine**: named operations carry declarative specs; anything that is code composes in code.
- **Dialogs and projections**: who each message type addresses; the `Dialog` at the center; convert in, edit at the center, project out.
- **The ecosystem**: which package owns what, where teaching lives, and why sessions open with a demonstration.

## The premise

An LLM equipped with a persistent interpreter does not need a bespoke tool for each operation. It needs capabilities as importable functions, docs it can pull on demand (`doc()`), and a discovery mechanism (`list_pyskills()`) that reports what is installed without importing anything. Hosts supply the kernel and the session rules: clikernel for terminal AIs such as Claude Code, Solveit with its own kernel and dialog tools, or a plain script. The packages are host-neutral, and everything below works the same from any of them.

## The media and their units

The toolkit's media run from plain to rich, and each has a natural semantic unit. Text is lines, and code or prose chunks further into blocks, separated by blank lines. A notebook (.ipynb) is a file of cells, and a cell is the first unit that does more than hold content: a code cell runs, keeping its outputs with it. A dialog is a notebook whose cells are messages in a conversation with an AI, and a message runs too: a prompt's output is the AI's reply. Units are what the tools address, summarize, read, and write, so knowing a medium's unit tells you how every tool will treat it.

Each editing function works on one carrier: text (a str in memory), a file (a path on disk), a cell (one cell's source in an .ipynb file, addressed by `path, cell_id`), or a notebook (the parsed .ipynb). These are the representation layer: an .ipynb is a file of cells, whatever produced it. The dialog layer above adds the msg and dlg carriers: a Solveit dialog is an .ipynb whose cells are messages (notes, runnable code, prompt/reply pairs), and `llmsurgery.dlgskill` and `dialoghelper` provide the message tools, following the conventions here with their own nouns. The word picks the layer: cell tools answer representation questions ("why does Jupyter reject this file?"), msg tools answer content questions ("what does this message say?").

Dialogs and Jupyter notebooks both serialize to the ipynb format, but they are not the same thing. A notebook has cells. A dialog has messages. Messages can be *prompts*, which notebooks cannot express, and they make structure explicit that notebooks leave implicit. E.g a heading opens a section that runs to the next heading of the same level; an export directive marks the code that belongs to a module. The shared file format means the same tools read both. The word tells you which layer you are on. File-level tools such as `fastcore.nbio` and `exhash` speak of cells and notebooks. Everything in this library speaks of messages and dialogs.

Work on a dialog file happens at three levels, and picking the right level is most of the craft:

- Content (`llmsurgery.dlgskill`, `dialoghelper`): what the messages say and how they change. `summary_dlg`, `find_msgs`, `view_dlg`, the message editing operations, and `reply2dlg`/`dlg2reply` for a prompt's reply.
- Representation (`fastcore.nbio`, formerly `execnb.nbio`): which keys exist, whether a file is schema-valid, whether bytes changed. Start with `validate_nb`/`validate_cell`, which name the offending cell; use `read_nb` directly when the question is about the dict itself.
- Raw text: only when the file will not parse at all.

Dropping a level is correct exactly when the question is about the representation rather than the content ("why does Jupyter reject this file?", "did that write change any bytes?"). Treat each drop as a signal, though: needing nbio or raw JSON to answer a content question means a higher-level tool was missing. Re-read the skill docs to check it truly is missing, and then propose adding it rather than repeating the workaround.

## Reading

When you don't yet know where to edit, locate with a summary first: `rgapi`'s `rg(summary=True)` and `nbrg`, and llmsurgery's `summary_dlg`, each show one line per natural unit of their medium (block, cell, message), carrying the unit's address. Summaries locate, views read, addresses edit, diffs confirm.

- `context=` counts the medium's own units: lines (or blocks in summary mode) for files, cells for notebooks, messages for dialogs. Dialog search defaults to context 1 because the neighbouring note usually explains the match: the why lives next to the what.
- Results display through tuned reprs designed to be read as-is: end the cell with the bare call and read what comes back - never join, slice, or otherwise reformat a result by hand. If a result is too big to take in full, narrow it with the function's own parameters (`max_results`, `paths=True`, `count=True`, tighter filters), not by post-processing the output.
- `doc()` a module before using anything from it, and each function before its first call. Docs are pulled on demand rather than preloaded, so reading them is part of the workflow, not preparation for it.

## Addressing

Edits say where with line numbers or lnhash addresses. Take addresses from the read you were already doing instead of with a second look: views accept `nums=True` or `lnhashs=True`, and searches return addresses directly (`rg(lnhashs=True)`). Prefer lnhash addresses whenever `exhash` is installed: they are verified against current content at edit time, so a stale address fails loudly instead of editing nearby text, which is exactly what makes taking addresses early safe. Plain line numbers are unverified and shift as edits apply, so re-view after each edit and apply multi-edits bottom-to-top. `exhash.skill` owns the address format and the verified editor.

Exhash's purpose is to make edits precise and auditable. First view a file as `lineno|hash|text` (line numbers may be space-padded for alignment); then issue ex-style commands against those exact addresses. Every addressed line's hash is checked immediately before the command runs, so stale context or wrong targets fail instead of editing nearby text. Hashes are checked immediately before each command and lines shift as edits apply; for multiple edits in one call always work *backwards* (bottom-to-top).

Prefer exhash over ad hoc patching for text file modifications, and prefer reading with `lnhashview_file` over plain file reads whenever an edit may follow: the view doubles as the address book, so the edit needs no second read.

Any `m` (cut+paste) or `t` (copy+paste) address can carry a target prefix: `path:` for another file, or `path.ipynb:cellid:` for one cell's source (`cellid` exact or unique prefix). This is THE way to transfer existing lines between locations: the lines never pass through your output, so opaque content (base64 blobs, hashes, long literals) cannot be mistyped. Take source addresses from `lnhashview_file`/`lnhashview_cell` of each target as usual.

Every editor returns a diff ("none: No changes." when nothing changed). The diff is the verification: read it instead of re-viewing the target.

## The grammar

### Naming

Two name shapes cover the toolkit, and the pivot is the verb's direct object:

- An operation on a whole carrier takes the carrier as its noun: verb_carrier. `view_file`, `create_file`, `read_nb`, `write_nb`, `view_cell`, `validate_nb`; in the dialog layer `view_msg`, `add_msg`, `find_msgs`. Coined verbs follow the same shape: `exhash_file` and `lnhashview_cell` are "exhash this file" and "lnhashview this cell".
- An operation within a carrier already owns its noun (`insert_line`, `del_lines`, `replace_lines`, `str_replace`), so the carrier prefixes as a namespace and the op name survives intact: carrier_op, as in `file_del_lines`, `cell_del_lines`, `msg_del_lines`. The bare op names are the text-level primitives, and every carrier version keeps the identical signature after its address arguments, so each family is learned once and recognized everywhere.

The exceptions are deliberate and closed. `str_replace` keeps the name and argument order established by Anthropic's text editor tool. `ast_replace` puts the instrument first: the AST pattern is how the edit finds its target, not what it replaces. Converters are named x2y (`nb2dict`, `cell2xml`; in llmsurgery, `dlg` on exactly one side of every converter). Plural marks arity: `view_cell` takes one cell, `lnhashview_cells` several, `del_msgs` many.

### Parameters

One vocabulary, identical wherever it appears:

- The carrier's address comes first (`text`; `path`; `path, cell_id`; a message `id`), the payload next, and ambient context last as keyword-only (message tools name their dialog that way).
- `start_line`/`end_line`: 1-based, inclusive, `None` for first/last, negative counting from the end. Destructive ops (`del_lines`) accept no defaults: state the range.
- `re_filter`/`invert_filter`: restrict an edit to lines matching (or not matching) a regex, like ex's `g//` and `g!//`; combines with the range.
- Searches read patterns as regex by default; editors read them as literal text until `use_regex=True`. Searching is read-only, so its default favors power; editing favors safety.
- `nums` and `lnhashs` on any view: line numbers, or `lineno|hash|` addresses. `maxlen` caps characters per summary line; `trunc_out`/`trunc_in` truncate outputs and sources in dialog views.
- Search tools share one filter vocabulary: `pattern` first, `root='.'`, and the same include/exclude/ext/hidden/ignore block across `fd`, `ls`, `rg`, and `nbrg`. Variants differ by defaults, not API: `ls` is `fd` with listing defaults. Boolean filters narrow as `only_*` and widen as `include_*`.

## The interpreter doctrine

Because the AI writes code, a wrapper whose only content is "run this code" is a wrapper around the language itself. Two such functions existed (`python_msgs` in llmsurgery, `msg_python` in dialoghelper), from the era when hosts offered fixed tool rosters and code-as-string was the only escape hatch; both are being removed. What earns a name instead is carrying a *declarative* edit spec to a carrier: `msg_str_replace` and its family add addressing, persistence routing, and a returned diff around arguments that are data, auditable in a way code-as-string is not. Anything whose input is code composes in code: live `Message` objects from `find_msgs` edited in a loop, `str -> str` transforms mapped over sources.

The ast tools split exactly on this line, and remold arrived at it independently. `astmap` takes declarative ast-grep rules, so it has carrier forms (`ast_replace`, `file_ast_replace`, and the message form in llmsurgery); `cstmap` takes a matcher and a Python function, so it has none: you call it like any other transform. The same doctrine gives search its extension point: `find_msgs(pred=)` accepts a callable, and the `*_finder` factories (`symdef_finder`, `symref_finder`, `ast_finder`) build them, so search grows by composing predicates rather than by adding parameters.

## Dialogs and projections

A dialog is a conversation between a human, an AI, and an interpreter. Each message type addresses one of them and expects a certain kind of answer:

- A **prompt** asks the AI a question and holds its reply.
- A **code** message gives the interpreter source and holds its outputs.
- A **note** is read by everyone and answered by nobody.
- A **raw** message addresses no one. It is inert matter the conversation carries along.

A reply may itself contain runnable code with results, so a whole dialog can live inside one message. `reply2dlg` opens a reply up as a dialog and `dlg2reply` puts it back.

The `Dialog` is the center of the library. Everything else is a projection of it. A storage projection must preserve everything that means something. What it does not understand it carries verbatim in metadata, and what is broken it heals rather than rejects. A transmission projection normalizes on purpose, and what it drops is written into its contract. A display projection only goes one way. The rule is to convert in, edit at the center, and project out. The function names say the same thing. Every converter has `dlg` on exactly one side.

| projection | contract | in | out |
|---|---|---|---|
| ipynb file | storage, pragmatically lossless | `read_ipynb` | `write_ipynb` |
| Claude Code session | storage | `sess2dlg` | `dlg2sess` |
| Codex thread | storage (write-only so far) | | `dlg2thread` |
| fastllm chat (`Msg`/`Part`) | transmission, normalizing | `chat2dlg` | `dlg2chat` |
| fastllm hist (live call input) | transmission, one-way | | `dlg2hist` |
| a prompt's reply | self-similar | `reply2dlg` | `dlg2reply` |
| XML views | display, one-way | | `view_dlg`, `msg2xml` |

The session codecs route through chat on their way to the wire: ant's `dlg2msgs` and oai's `dlg2items` are each `denorm_msgs(dlg2chat(...))`.

## The ecosystem

### What's where

- `fastcore.tools`: text primitives, file tools, and `line_hash`/`lnhash`/`lnhash_at` for creating addresses without exhash installed.
- `fastcore.nbio`: notebook read/write/validate/repair, cell construction, cell editors.
- `exhash.skill`: hash-verified editing for files and cells; prefer it for edits where installed.
- `rgapi.skill`: `rg`/`fd`/`ls`/`nbrg` search with lnhash output.
- `remold`: structural search and rewrite for Python source (declarative ast-grep rules, LibCST matcher transforms, symbol queries); the engine behind `ast_replace`.
- `llmsurgery.dlgskill`, `dialoghelper`: the dialog layer, including its own theory of dialogs and projections.

### Where teaching lives

Packages whose primary users are AI agents teach in the module docstring, where `doc()` and pyskills discovery reach it. The README keeps the human jobs: pitch, install, development notes, and a pointer to the skill docs (remold is the model). Usage prose duplicated between the two leaves an unmaintained copy, and unmaintained copies teach wrong names.

A separate `skill.py` earns its place only when a package's import surface and its LLM surface differ, so that a curated teaching module pays for itself: exhash, rgapi, and llmsurgery each have machinery their skill module selects from, and fastcore's is `editskill`. When the whole package is the LLM surface, register the package module itself as the pyskill (remold, `toolslm.read_md`). Either way, the docstring's first line doubles as the `list_pyskills()` description, so it should name the capability and when to reach for it.

### Demonstrations over instructions

Session-start instructions tell a model what to do; its context shows it what gets done, and the showing wins. llmdojo's DEV.md states the observation that drives the host machinery: "A fresh session gets its tooling *instructions* up front but no *examples*, and models imitate what their context shows far more reliably than what it tells." So hosts open sessions with a completed, curated practice round already in history (claudedojo, codexdojo), and the round is held to a higher bar than correct: whatever it demonstrates, sessions repeat. Templates are rebuilt when the tooling changes, since a stale demonstration teaches stale names.
