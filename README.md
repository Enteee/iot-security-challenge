# IoT Security

Welcome to the **IoT Security** project! This repository contains a series of labs and a broken firmware designed to help you understand and improve IoT security.

## Installation

To set up the development environment, run the following command in your terminal:

```bash
bash <(curl -L https://tinyurl.com/3tfzhavn)
```

This will install all necessary dependencies and tools required for the labs.

## Development Environment Commands

Here are some commands you can use within the development environment:

* `flash`: Flash your ESP32 with clean firmware
* `flash_erase`: Set ESP32 flash to all `0x0`
* `upload`: Upload your MicroPython code from the `src/` directory
* `upload_lab LABNAME`: Upload a lab called `LABNAME`
* `fs`: Browse the filesystem on your ESP32
* `repl_peek`: Show logs
* `repl`: Start an interactive Read-Eval-Print Loop (REPL)
* `devenv_help`: Print all available commands

**Hint**: See [ESP32.md](ESP32.md) for an overview of the ESP32's functionality.

## Working with Multiple ESP32 Devices

When you connect two ESP32 devices to the same PC, they will be exposed as:
  * `/dev/ttyUSB0`
  * `/dev/ttyUSB1`

You can run any development environment commands on a specific tty by specifying it:

```bash
flash /dev/ttyUSB0
```

To run a command on all connected ESP32 devices, use the `alltty` command:

```bash
alltty COMMAND
```

For example, to flash firmware on all connected devices:

```bash
alltty flash
```

## Top-Level Folders and Files

### `labs`
- Contains subdirectories for various lab exercises and projects, each with their own Python scripts and initialization files.

### `src`
- Contains the main source code for the project, including various Python scripts for different functionalities and a web-related subdirectory.

### `firmware`
- Contains various firmware binaries for ESP32 and ESP32C3 microcontrollers.

### `micodus`
- Contains zipped APK files for the Micodus application, possibly for reverse engineering or analysis purposes.

### `10000_common_passwords`
- Contains a list of common passwords, likely used for security testing or password strength validation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or need further assistance, feel free to open an issue or contact the project maintainers.

Happy hacking!
