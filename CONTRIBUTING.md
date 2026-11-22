# Where does my change go?

Answer these in order; the first "yes" is the place.

1. **Is it about drawing screens, keys, themes, or how a command is described, agreed, run and recorded?** It goes in the foundation: `pmin-kit` (screens) or `pmin-tools` (actions, audit, redaction).
2. **Is it part of one of the 15 core functions, and useful whatever the industry?** It goes in that function's module (see the table in [README.md](README.md)). This is where most work belongs.
3. **Is it specific to one industry: a check, a filter, a rule, a setting, a context, a value with a default?** It goes in that industry's framework in `pmin-industries/<industry>/<module>/`, as data and thin glue. A framework adds to a module; it never runs commands itself and never removes or weakens a built-in.
4. **Do two industries now need the same thing?** Move it out of the frameworks into the function module, and leave each framework only its own values. Note it in `pmin-industries/PROMOTE.md`.
5. **Does it put modules together into something to run?** It is a program (`pmin-hub`, `pmin-diskmap`), or a new program of its own.

## Rules that keep the layout working

- The foundation imports nothing from modules, frameworks or programs.
- A function module imports the foundation and only the sibling modules in its `pmin.json` `requires`.
- A framework imports modules and the foundation, never a program.
- A module's extension type changes only with care: a breaking change needs the `breaking` label, as `mint-tools/action` does today.
- Every repository has a `pmin.json`. After adding or changing one, run `python3 scripts/sync-catalogue.py` here, with the repositories cloned side by side, and commit the result.

## pmin.json

```json
{
  "name": "pmin-lookout",
  "module": "github.com/CurtisD4q/pmin-lookout",
  "tier": "function",
  "function": 11,
  "slug": "monitor",
  "group": "Manage the system",
  "title": "Monitor and troubleshoot. Read logs, diagnose faults, and test networks and system health.",
  "audience": "user",
  "requires": ["pmin-kit", "pmin-loom", "pmin-tools"],
  "status": "v0"
}
```

`tier` is one of `foundation`, `function`, `engine`, `wrap`, `program`. Modules other than function modules give a `summary` instead of `function`, `slug`, `group` and `title`. `contributorParts` lists folders meant for people building with the library (templates, examples) rather than for people using it.
