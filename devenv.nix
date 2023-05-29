{ pkgs, ... }:

{

  # https://devenv.sh/basics/
  env.GREET = "devenv";


  # https://devenv.sh/packages/
  packages = [
    pkgs.git
    pkgs.micropython
    pkgs.esptool
    pkgs.picocom
    pkgs.rshell
    pkgs.mpfshell
    pkgs.parallel

    pkgs.squashfsTools
    pkgs.zip
    pkgs.binwalk
    pkgs.black

    pkgs.thc-hydra
    pkgs.nmap
  ];

  scripts.erase_flash.exec = ''
    tty="''${1:-/dev/ttyUSB0}"
    esptool.py \
      --port "''${tty}" \
      erase_flash
  '';
  scripts.getchip.exec = ''
    tty="''${1:-/dev/ttyUSB0}"
    esptool.py \
      --port "''${tty}" \
      read_mac \
    | sed -nre 's/Chip is ([^ ]+).*/\1/p' \
    | tr '[:upper:]' '[:lower:]'
  '';

  scripts.flash.exec = ''
    tty="''${1:-/dev/ttyUSB0}"
    (
      cd "''${DEVENV_ROOT}"
      set -x

      chip_id="''$(getchip)"

      declare -A chip_name=( \
        ["esp32-c3"]="esp32-c3" \
        ["esp32-d0wd"]="esp32" \
      )

      declare -A chip_fw=( \
        ["esp32-c3"]="${./firmware/esp32c3-20230426-v1.20.0.bin}" \
        ["esp32-d0wd"]="${./firmware/esp32-20230426-v1.20.0.bin}" \
      )

      declare -A chip_addr=( \
        ["esp32-c3"]="0x0" \
        ["esp32-d0wd"]="0x1000" \
      )

      esptool.py \
        --chip "''${chip_name["''$chip_id"]}" \
        --port "''${tty}" \
        --baud 460800 \
        write_flash \
          --compress \
          "''${chip_addr["''$chip_id"]}" \
          "''${chip_fw["''$chip_id"]}"
    )
  '';

  scripts.repl.exec = ''
    tty="''${1:-/dev/ttyUSB0}"
    picocom \
      "''${tty}" \
      -b115200
  '';

  scripts.fs.exec = ''
    tty="''${1:-/dev/ttyUSB0}"
    mpfshell \
      "''${tty}"
  '';

  scripts.alltty.exec = ''
    parallel \
      --will-cite \
      --tagstring "[{/.}]" \
      --line-buffer \
      "''${@} {}" ::: /dev/ttyUSB*
  '';

  scripts.upload.exec = ''
    tty="''${1:-/dev/ttyUSB0}"
    (
      cd "''${DEVENV_ROOT}"
      rshell \
        --port "''${tty}" \
        --file ./flash.cmds
    )
  '';

  scripts.mkfirmware.exec = ''
    (
      cd "''${DEVENV_ROOT}/src"

      rm \
        ota_firmware.bin \
        ota_firmware.zip

      mksquashfs \
        *.py www/ \
        ota_firmware.bin

      zip \
        ota_firmware.zip \
        ota_firmware.bin

      rm \
        ota_firmware.bin
    )
  '';

  scripts.clean_setup.exec = ''
    erase_flash
    flash
    mkfirmware
    upload
  '';

  scripts.doalll.exec = ''
    clean_setup
    repl
  '';

  scripts.portmap.exec = ''
    (
      cd "''${DEVENV_ROOT}"
      set -x
      nmap 192.168.4.1
    )
  '';

  scripts.extracfw.exec = ''
    set -x
    nc -w 1 192.168.4.1 880 > fw
    binwalk -M -e fw
    rm -rf fw
  '';

  scripts.bforce.exec = ''
    (
      cd "''${DEVENV_ROOT}"
      set -x
      hydra \
        -I \
        -t 1 \
        -l admin \
        -P "${./10000_common_passwords}" \
        http-get://192.168.4.1
    )
  '';



  enterShell = ''
  '';

  # https://devenv.sh/languages/
  #languages.nix.enable = true;
  #languages.python.enable = true;

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # https://devenv.sh/processes/
  # processes.ping.exec = "ping example.com";

  # See full reference at https://devenv.sh/reference/options/
}
