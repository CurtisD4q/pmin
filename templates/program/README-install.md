## Install

Download, check and install the latest release in one go (Linux and macOS):

```
gh api repos/CurtisD4q/@NAME@/contents/install.sh -H 'Accept: application/vnd.github.raw' | sh
```

While the repository is private this needs the [GitHub CLI](https://cli.github.com), logged in (`gh auth login`). Once it is public, `curl -fsSL https://raw.githubusercontent.com/CurtisD4q/@NAME@/main/install.sh | sh` does the same. Add `-s -- --system` after `sh` to install for everyone in `/usr/local`.

Or by hand: download the archive for your machine from Releases, check it against `SHA256SUMS`, unpack it and run `./@NAME@ install`. Either way @NAME@ ends up in `~/.local/bin`, and the download can be deleted.

To remove it: `@NAME@ uninstall`. Your settings and data are kept.

### Build from source

Needs Go and access to the private pmin libraries:

```
git clone https://github.com/CurtisD4q/@NAME@
cd @NAME@
export GOPRIVATE='github.com/CurtisD4q/*'
make install        # builds, then installs into ~/.local/bin
```

After `make install` the cloned folder can be deleted. To clone and fetch the libraries over SSH instead of HTTPS, tell git once: `git config --global url."git@github.com:".insteadOf "https://github.com/"`, and clone `git@github.com:CurtisD4q/@NAME@.git`.
