# pmin (peppermint)

The front door to peppermint: terminal interface libraries for business and enterprise work. This repository holds no library code. It holds the map: which repository does what, and how to add to them.

The repositories are still named `mint-*`; they will be renamed `pmin-*` in one step later.

## How it is organised

Two axes, weighted 70 / 30:

- **Function modules (70, the primary axis).** One repository for each of the 15 core functions below. Every repository, README, catalogue entry and CI check is keyed by function first. Logic that two industries need goes into the function module.
- **Industry frameworks (30, the secondary axis).** Add-ons to the function modules, one per industry, kept in `pmin-industries`. A framework holds specifications, conditions, contexts, rules and variables for its industry. It runs nothing itself: everything still goes through the modules' one executor, with its previews, agreement and audit record.

Under both sits the foundation (`mint-kit` for screens, `mint-tools` for the action contract and audit). Programs such as `mint-hub` assemble the modules.

- [CATALOGUE.md](CATALOGUE.md): every repository, by tier, with what it requires
- [MATRIX.md](MATRIX.md): the 15 functions by the 12 industries, filled only where a framework has content
- [CONTRIBUTING.md](CONTRIBUTING.md): where a change goes

Both generated files come from each repository's `pmin.json` and from `data/`; run `python3 scripts/sync-catalogue.py` with the repositories cloned side by side to refresh them.

## The 15 core functions

| # | Function | Module |
| --- | --- | --- |
| | **Work with files and text** | |
| 1 | Navigate and manage files. Move, copy, rename, delete, find, and compress files and directories. | mint-atlas |
| 2 | Search and read text and data. View, filter, and summarize files and logs, from a short config to a multi-gigabyte dataset. | mint-lens |
| 3 | Edit text and config. Change code, config files, and scripts without leaving the terminal. | mint-quill |
| | **Compose and automate** | |
| 4 | Combine tools with pipes and redirection. Chain small commands so the output of one becomes the input of the next. | mint-conduit |
| 5 | Automate with scripts and schedules. Save repeatable work as shell scripts and run it on a timer or trigger. | mint-loom |
| | **Run and build** | |
| 6 | Write, build, and run code. Compile, test, and debug programs, and run scripts and jobs. | mint-forge |
| 7 | Manage processes and resources. Start, background, pause, and kill programs, and check CPU, memory, and disk use. | mint-pulse |
| 8 | Run services and containers. Start servers, databases, and containers, and manage how they run. | mint-engine |
| | **Manage the system** | |
| 9 | Install and manage software. Add, update, and remove packages and libraries, and pin versions. | mint-depot |
| 10 | Manage users, permissions, and security. Control who can access what, and configure firewalls and network settings. | mint-warden |
| 11 | Monitor and troubleshoot. Read logs, diagnose faults, and test networks and system health. | mint-lookout |
| | **Reach out and collaborate** | |
| 12 | Connect to other machines. Log in to remote servers, clusters, and devices over SSH or serial. | mint-bridge |
| 13 | Transfer and fetch data. Download, upload, and sync files between machines and from the web. | mint-courier |
| 14 | Track and share code. Version your work and collaborate with Git. | mint-ledger |
| | **Learn and customize** | |
| 15 | Get help and tailor your environment. Use man pages and --help, and set up aliases, prompts, and shell config. | mint-hearth |

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
