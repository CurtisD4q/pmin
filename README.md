# pmin (peppermint)

The front door to peppermint: terminal interface libraries for business and enterprise work. This repository holds no library code. It holds the map: which repository does what, and how to add to them.

The library repositories are named `pmin-*`. Programs and folders on people's computers keep their names: the hub's command keeps its name (it is built from `cmd/mint-hub`), settings stay in folders such as `~/.config/mint-scan`, and `MINT_*` variables still work.

## How it is organised

Two axes, weighted 70 / 30:

- **Function modules (70, the primary axis).** One repository for each of the 15 core functions below. Every repository, README, catalogue entry and CI check is keyed by function first. Logic that two industries need goes into the function module.
- **Industry frameworks (30, the secondary axis).** Add-ons to the function modules, one per industry, kept in `pmin-industries`. A framework holds specifications, conditions, contexts, rules and variables for its industry. It runs nothing itself: everything still goes through the modules' one executor, with its previews, agreement and audit record.

Under both sits the foundation, in five layers: `pmin-base` (plain helpers), `pmin-sys` (reading the system), `pmin-kit` (screens), `pmin-tools` (doing things safely) and `pmin-contracts` (the shapes modules share). Modules use only the foundation, so none depends on another; programs such as `pmin-hub` connect them.

- [CATALOGUE.md](CATALOGUE.md): every repository, by tier, with what it requires
- [MATRIX.md](MATRIX.md): the 15 functions by the 12 industries, filled only where a framework has content
- [LAYERING.md](LAYERING.md): the modules that still use another module, until they have all moved to using only the foundation
- [CONTRIBUTING.md](CONTRIBUTING.md): where a change goes

Both generated files come from each repository's `pmin.json` and from `data/`; run `python3 scripts/sync-catalogue.py` with the repositories cloned side by side to refresh them.

## The 15 core functions

| # | Function | Module |
| --- | --- | --- |
| | **Work with files and text** | |
| 1 | Navigate and manage files. Move, copy, rename, delete, find, and compress files and directories. | pmin-atlas |
| 2 | Search and read text and data. View, filter, and summarize files and logs, from a short config to a multi-gigabyte dataset. | pmin-lens |
| 3 | Edit text and config. Change code, config files, and scripts without leaving the terminal. | pmin-quill |
| | **Compose and automate** | |
| 4 | Combine tools with pipes and redirection. Chain small commands so the output of one becomes the input of the next. | pmin-conduit |
| 5 | Automate with scripts and schedules. Save repeatable work as shell scripts and run it on a timer or trigger. | pmin-loom |
| | **Run and build** | |
| 6 | Write, build, and run code. Compile, test, and debug programs, and run scripts and jobs. | pmin-forge |
| 7 | Manage processes and resources. Start, background, pause, and kill programs, and check CPU, memory, and disk use. | pmin-pulse |
| 8 | Run services and containers. Start servers, databases, and containers, and manage how they run. | pmin-engine |
| | **Manage the system** | |
| 9 | Install and manage software. Add, update, and remove packages and libraries, and pin versions. | pmin-depot |
| 10 | Manage users, permissions, and security. Control who can access what, and configure firewalls and network settings. | pmin-warden |
| 11 | Monitor and troubleshoot. Read logs, diagnose faults, and test networks and system health. | pmin-lookout |
| | **Reach out and collaborate** | |
| 12 | Connect to other machines. Log in to remote servers, clusters, and devices over SSH or serial. | pmin-bridge |
| 13 | Transfer and fetch data. Download, upload, and sync files between machines and from the web. | pmin-courier |
| 14 | Track and share code. Version your work and collaborate with Git. | pmin-ledger |
| | **Learn and customize** | |
| 15 | Get help and tailor your environment. Use man pages and --help, and set up aliases, prompts, and shell config. | pmin-hearth |

## What a framework can add to each module

Every function module has an `Extension` type (in its `ext.go`) and a way to use it that adds and never replaces or loosens.

| # | Module | A framework can add |
| --- | --- | --- |
| 1 | pmin-atlas | paths never to move, trash or delete |
| 2 | pmin-lens | ready-made searches |
| 3 | pmin-quill | settings that must not change, by file and key |
| 4 | pmin-conduit | filters and source programs |
| 5 | pmin-loom | recipe templates |
| 6 | pmin-forge | kinds of project |
| 7 | pmin-pulse | programs never to stop, end or reprioritise |
| 8 | pmin-engine | sources of services and jobs |
| 9 | pmin-depot | packages never to remove |
| 10 | pmin-warden | an ssh hardening baseline |
| 11 | pmin-lookout | checks and symptoms |
| 12 | pmin-bridge | serial console presets |
| 13 | pmin-courier | places never to mirror into |
| 14 | pmin-ledger | branches never to delete, force-push or hard reset |
| 15 | pmin-hearth | prompts (text only, never commands) |

pmin-scan, the disk engine under Function 7, takes a framework's known places as a places file.

## The 12 target industries

| # | Industry | Slug |
| --- | --- | --- |
| 1 | Cloud Computing/DevOps/IT Infrastructure | devops |
| 2 | Software Engineering/Web Development | webdev |
| 3 | Cybersecurity/Penetration Testing | cyber |
| 4 | Data Science/AI/Machine Learning | datasci |
| 5 | Banking/FinTech/Stock Exchanges | fintech |
| 6 | Film/Animation/VFX | vfx |
| 7 | Scientific Research/Bioinformatics | science |
| 8 | Telecommunications/IoT/Embedded Systems | telecom |
| 9 | Retail/Logistics/E-Commerce | retail |
| 10 | Automotive/Aerospace | auto |
| 11 | Healthcare/Medical Imaging | health |
| 12 | Energy/Utilities | energy |

Slugs are short codes for folder names and ids (a cell is written `health.lookout`); the names above are the industries.

## Built with pmin

`cairn` (security work) and `jobwatch` (backup and job health) are programs made with these libraries. They are left as they are for now and will be brought up to date with this layout later.

## Spearmint

`smin-` is reserved for spearmint, a future family for tinkerers and experiments. Nothing is built there yet.

## Licence

Apache 2.0.
