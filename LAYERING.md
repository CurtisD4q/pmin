# Layering

Modules (function, engine, wrap and frameworks) may use only the foundation: pmin-base, pmin-sys, pmin-kit, pmin-tools and pmin-contracts. Programs wire modules together. This file lists every module that still requires another module; it is written by `scripts/sync-catalogue.py` and should end empty.

10 modules still require another module.

| Module | Tier | Still requires |
|---|---|---|
| pmin-appkit | wrap | pmin-spec (wrap) |
| pmin-bridge | function | pmin-serial (engine) |
| pmin-courier | function | pmin-bridge (function) |
| pmin-gen | wrap | pmin-appkit (wrap), pmin-spec (wrap) |
| pmin-industries | frameworks | pmin-conduit (function), pmin-forge (function), pmin-lookout (function), pmin-scan (engine) |
| pmin-lookout | function | pmin-loom (function) |
| pmin-loom | function | pmin-jobhealth (engine) |
| pmin-quill | function | pmin-formats (engine) |
| pmin-warden | function | pmin-netfilter (engine) |
| pmin-wrap | wrap | pmin-gen (wrap), pmin-spec (wrap) |
