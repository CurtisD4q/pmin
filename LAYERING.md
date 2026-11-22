# Layering

Modules (function, engine, wrap and frameworks) may use only the foundation: pmin-base, pmin-sys, pmin-kit, pmin-tools and pmin-contracts. Programs wire modules together. This file lists every module that still requires another module; it is written by `scripts/sync-catalogue.py` and should end empty.

4 modules still require another module.

| Module | Tier | Still requires |
|---|---|---|
| pmin-appkit | wrap | pmin-spec (wrap) |
| pmin-gen | wrap | pmin-appkit (wrap), pmin-spec (wrap) |
| pmin-industries | frameworks | pmin-conduit (function), pmin-forge (function), pmin-lookout (function), pmin-scan (engine) |
| pmin-wrap | wrap | pmin-gen (wrap), pmin-spec (wrap) |
