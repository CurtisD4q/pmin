# Where does my change go?

Answer these in order; the first "yes" is the place.

1. **Is it something every module could use, or a shape two modules both need?** It goes in the foundation, in the lowest layer that fits: `pmin-base` (plain helpers), `pmin-sys` (reading the system and other programs' output), `pmin-kit` (screens), `pmin-tools` (doing things safely: actions, running, audit, undo, guards) or `pmin-contracts` (shapes modules share: types and interfaces only).
2. **Is it part of one of the 15 core functions, and useful whatever the industry?** It goes in that function's module (see the table in [README.md](README.md)). This is where most work belongs.
3. **Is it specific to one industry: a check, a filter, a rule, a setting, a context, a value with a default?** It goes in that industry's framework in `pmin-industries/<industry>/<module>/`, as data and thin glue. A framework adds to a module; it never runs commands itself and never removes or weakens a built-in.
4. **Do two industries now need the same thing?** Move it out of the frameworks into the function module, and leave each framework only its own values. Note it in `pmin-industries/PROMOTE.md`.
5. **Does it put modules together into something to run?** It is a program (`pmin-hub`, `pmin-diskmap`), or a new program of its own.

## Rules that keep the layout working

- **Modules use only the foundation.** Function modules, engines, the wrap pipeline and the frameworks import pmin-base, pmin-sys, pmin-kit, pmin-tools and pmin-contracts, and nothing else from the family. They are independent: none depends on another.
- **When two modules must work together, they agree on a shape in pmin-contracts** (a type, or an interface such as `settings.Parser` or `machines.Book`), each codes against it, and a program plugs the real one in.
- **The foundation is layered:** 1 pmin-base, 2 pmin-sys, 3 pmin-kit, 4 pmin-tools, 5 pmin-contracts. Each layer uses only the ones below it, and gives its number as `layer` in `pmin.json`.
- **Tests may also use engines.** A module's tests can check it against the real engine a program will plug in (Quill's tests read real files with pmin-formats). `pmin.json` lists those under `testRequires`; the module's own code still uses only the foundation. A framework's tests may also use the function modules it extends, to show its additions working in them.
- **Every module is useful on its own.** With only the foundation and itself it does its main job; it may gain abilities when a program connects it to others (Quill edits whole files alone, and setting by setting with pmin-formats plugged in).
- **pmin-industries is a module in the structure and an add-on in practice.** Its code uses only the foundation; a program hands each module the frameworks' additions. The shapes it fills live in pmin-contracts, so changing one goes through the foundation.
- **Nothing depends on a program.** pmin's own programs (`pmin-hub`, `pmin-diskmap`; tier `program`) connect the modules and may use each other. Programs built with pmin (cairn, jobwatch, susynth; tier `example`) may use any module, engine or framework, but never a program or each other; they may copy code from pmin's programs and make it their own.
- **New things go where they are useful.** Something with broad use goes into a module; something only one program needs is built in that program.
- **Everything tracks main for now.** Versions are revisited once the programs built with pmin are rebuilt.
- The layering check in CI enforces this: a module that imports another module fails. [LAYERING.md](LAYERING.md), written by the catalogue script, lists any breach across the family; it is empty.
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

`tier` is one of `foundation`, `function`, `engine`, `wrap`, `frameworks`, `program`, `example`; a foundation repository also gives its `layer`. `requires` lists the family modules the code imports, and `testRequires` those only the tests import. Modules other than function modules give a `summary` instead of `function`, `slug`, `group` and `title`. `contributorParts` lists folders meant for people building with the library (templates, examples) rather than for people using it.
