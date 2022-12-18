#!/bin/sh

HOME=${1}
mkdir -p $HOME/.config/nix $HOME/.config/nixpkgs
echo 'sandbox = false' >> $HOME/.config/nix/nix.conf
echo "experimental-features = nix-command flakes" >> $HOME/.config/nix/nix.conf
echo '. $HOME/.nix-profile/etc/profile.d/nix.sh' >> $HOME/.bashrc
