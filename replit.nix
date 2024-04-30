{pkgs}: {
  deps = [
    pkgs.postgresql
    pkgs.httpie
    pkgs.python311Packages.httpie
  ];
}
