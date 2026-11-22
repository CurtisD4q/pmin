# Layering

Modules (function, engine, wrap and frameworks) may use only the foundation: pmin-base, pmin-sys, pmin-kit, pmin-tools and pmin-contracts. Programs wire modules together. This file lists every module that still requires another module; it is written by `scripts/sync-catalogue.py` and should end empty.

Nothing left: every module uses only the foundation.
