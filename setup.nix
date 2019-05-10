{ pkgs ? import (builtins.fetchTarball {
    url = "https://github.com/NixOS/nixpkgs-channels/archive/312a059bef8b29b4db4e73dc02ff441cab7bb26d.tar.gz";
    sha256 = "1j52yvkhw1inp6ilpqy81xv1bbwgwqjn0v9647whampkqgn6dxhk";
  }) {}
, setup ? import (builtins.fetchTarball {
    url = "https://github.com/datakurre/setup.nix/archive/24c4a09aa069f03cfac4f19e1ef13f048718cffc.tar.gz";
    sha256 = "1l8wjibv35wyrc0m8cpcav8ixjdskhdl2piy1pa6fi01z94lwr9n";
  })
, python ? "python3"
, pythonPackages ? builtins.getAttr (python + "Packages") pkgs
, requirements ?  ./. + "/requirements-${python}.nix"
}:

let overrides = self: super: {
  "testfixtures" = super."testfixtures".overridePythonAttrs(old: {
    patches = [];
  });
};

in setup {
  inherit pkgs pythonPackages overrides;
  src = ./.;
  requirements = requirements;
}
