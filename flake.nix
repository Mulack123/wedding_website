
{
  description = "Wedding website";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, ... }: let
    system = "x86_64-linux"; # Change to your system if needed
    pkgs = import nixpkgs {
      inherit system;
    };
  in {
    #### Sample for building a package ####
    # packages.${system}.default = pkgs.buildGoModule {
    #   name = "Wedding_website";
    #   src = ./.;
    #   vendorHash = null;
    # };

    devShells.${system}.default = pkgs.mkShell {
      buildInputs = with pkgs; [
	python3
      ];

      shellHook = ''
        echo "🐍 Welcome to the Wedding_website dev shell!"

        # Optional: Automatically create venv in ./.venv
        if [ ! -d .venv ]; then
          echo "🔧 Creating virtual environment in ./.venv"
          python3 -m venv .venv
        fi
        source ./.venv/bin/activate
        echo "✅ Virtualenv activated"
'';
    };
  };
}
