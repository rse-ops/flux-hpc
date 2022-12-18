{
  description = "ConveyorLC Environment";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    rse-ops.url = "github:rse-ops/nix";
    flake-utils.url = "github:numtide/flake-utils";
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
  };

  outputs = { self, nixpkgs, flake-utils, flake-compat, rse-ops, mach-nix, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        rseops = rse-ops.packages.${system};
        buildInputs = [
            rseops.conveyorlc
            pkgs.python39Packages.conda
            pkgs.micromamba
            pkgs.python38
            pkgs.python38Packages.pip
        ];
        shell-inputs = pkgs: with pkgs ; [
           bash
           git
           vim
         ] ++ buildInputs;

         conveyorlc_env = pkgs.stdenv.mkDerivation {
           pname = "conveyorlc-env";
           version="0.0.1";
           src = self; 
           nativeBuildInputs = shell-inputs pkgs;
           buildInputs = buildInputs;
           format = "other";
           installPhase = ''
             mkdir -p $out
             touch $out/dinosaur.txt
           '';
          };
      in {
          devShells.default = pkgs.mkShell {
            nativeBuildInputs = shell-inputs pkgs;
            buildInputs = buildInputs ++ [conveyorlc_env];
            shellHook = ''
                export PATH=/home/flux/mamba/bin:$PATH
                ln -s /home/flux/mamba/dat/leap/cmd/oldff/leaprc.ff14SB /home/flux/mamba/dat/leap/cmd/leaprc.ff14SB || echo Link leaprc.ff14SB already exists
                ln -s /home/flux/mamba/dat/leap/cmd/oldff/leaprc.ff99SB /home/flux/mamba/dat/leap/cmd/leaprc.ff99SB || echo Link leaprc.ff99SB already exists
            '';
        };
         packages.default = conveyorlc_env;
   });
}
