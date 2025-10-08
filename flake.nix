{
  description = "Sample flake";

  inputs = {
    nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0";
    flake-utils.url = "github:numtide/flake-utils";
  };

outputs = { self, nixpkgs, flake-utils, ... }:
  flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [];
      };
    in
    {
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          uv
       ];
         shellHook = ''
          source .venv/bin/activate
          # Start the virtual environment
          echo -e "\033[1;36mPython:\033[0m $(python --version 2>&1)"
         '';
        };      
    });
}


