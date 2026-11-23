# Made from pmin/templates/program/Makefile. NAME is the command; FILES ship
# beside it in a release and are installed with it.
NAME := @NAME@
FILES := @FILES@
TARGETS ?= linux/amd64 linux/arm64 darwin/amd64 darwin/arm64

.PHONY: build test install uninstall dist clean

build:
	CGO_ENABLED=0 go build -trimpath -o $(NAME) ./cmd/$(NAME)

test:
	go vet ./... && go test ./...

# Installs into ~/.local/bin; `make install FLAGS=--system` for /usr/local.
# Afterwards this folder can be deleted.
install: build
	./$(NAME) install $(FLAGS)

uninstall: build
	./$(NAME) uninstall $(FLAGS)

dist:
	NAME=$(NAME) FILES="$(FILES)" TARGETS="$(TARGETS)" sh scripts/dist.sh

clean:
	rm -rf $(NAME) dist
