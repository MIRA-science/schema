{
  description = "MIRA schema development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            python314
            uv
            nodejs
            plantuml
            stdenv.cc.cc.lib
            pre-commit
          ];

          env = {
            # Prevent uv from downloading its own Python; use the one from Nix
            UV_PYTHON_DOWNLOADS = "never";
            UV_PYTHON = "${pkgs.python314}/bin/python3.14";
            LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
          };

          shellHook = ''
            uv sync
            pre-commit install
          '';
        };
      }
    );
}
