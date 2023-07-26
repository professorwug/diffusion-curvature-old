{
  description = "Fast Pointwise Graph Curvature";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
  };


  outputs = { self, nixpkgs, flake-utils }: (flake-utils.lib.eachSystem [
    "x86_64-linux"
    "x86_64-darwin"
    "aarch64-linux"
    "aarch64-darwin"
  ] (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in
    rec {
      packages.jonathansenv = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = ./.;
      };

      defaultPackage = packages.diffusion_curvature;

      devShell = pkgs.mkShell {
        buildInputs = [
          pkgs.poetry
        ];
      };
    }));
}
