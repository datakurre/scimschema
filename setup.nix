{ pkgs ? import (builtins.fetchTarball {
    url = "https://github.com/NixOS/nixpkgs-channels/archive/312a059bef8b29b4db4e73dc02ff441cab7bb26d.tar.gz";
    sha256 = "1j52yvkhw1inp6ilpqy81xv1bbwgwqjn0v9647whampkqgn6dxhk";
  }) {}
, setup ? import (builtins.fetchTarball {
    url = "https://github.com/datakurre/setup.nix/archive/9973f4f4d68776c7a3084e3e7d2635a65b33a35b.tar.gz";
    sha256 = "176y0d5h0pdf3gv6jz461l4lnz1jcjc5ns19s88yf5vwhib0jb4m";
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
