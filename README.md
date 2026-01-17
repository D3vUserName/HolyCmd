# HolyCMD 🚀

<!-- If you want to use a banner, first add an image to the 'assets/' folder in your repository, then use this link: -->
<!-- ![HolyCMD Banner](https://raw.githubusercontent.com/D3vUserName/HolyCmd/main/assets/banner.png) -->

**A powerful, feature-rich terminal with package management, themes, and developer tools**

<!-- SHIELDS.IO BADGES -->
[![Python Version](https://img.shields.io/badge/python-3.8+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20|%20Linux%20|%20macOS-0066CC?logo=windowsterminal&logoColor=white)](https://github.com/D3vUserName/HolyCmd)
[![License](https://img.shields.io/badge/license-Proprietary-8A2BE2)](https://github.com/D3vUserName/HolyCmd/blob/main/LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg?logo=black)](https://github.com/psf/black)
[![Discord](https://img.shields.io/badge/discord-Join%20Community-5865F2?logo=discord&logoColor=white)](https://discord.gg/holycmd)

---

## Overview

**HolyCMD** is a powerful, feature-rich interactive terminal that combines system commands, package management, themes, translations, aliases, and many developer tools. Built in Python, it is designed for users who want a customizable, all-in-one environment.

---

## Features

- Interactive shell with autocomplete and command history
- Customizable themes and translations
- Command aliasing and unaliasing
- Package manager for installing/removing/updating packages
- Support for multiple programming languages and tools
- Repository management for packages
- Built-in help and documentation
- Automatic detection of interactive processes
- Operator and command handling
- Modular extension system (packages)
- Dynamic translations and themes

---

## Installation

### Requirements

- Python 3.8+
- pip

---

## Configuration

### Files

HolyCMD stores configuration files in `~/.holycmd/`:

| File               | Purpose                                              |
|--------------------|------------------------------------------------------|
| `aliases.json`     | User-defined command aliases                         |
| `theme.json`       | Current theme selection                              |
| `language.json`    | Selected language                                    |
| `packages.json`    | Installed packages manifest                          |
| `repositories.json`| Package repositories                                 |

### Changing themes and language

```bash
theme list
theme <name>
language list
language <code>
```

### Managing aliases

```bash
alias
alias name=command
unalias name
```

### Example

```bash
> alias ll='ls -la'
> theme dark
> language en
> help
```

---

## Usage

After starting, you can use:

- Autocomplete and command history
- Built-in commands: `help`, `exit`, `cd`, `pkg`, `theme`, `alias`, `history`, `env`, `set`, `which`, and more
- Package management: install, remove, update packages
- Theme and language switching
- Alias management
- Dynamic translation support

### Examples

```bash
> pkg install package_name
> alias ll='ls -la'
> theme dark
> language en
> help
> which python
> exit
```

---

## Development & Support

Source code available on GitHub: [https://github.com/D3vUserName/HolyCMD](https://github.com/D3vUserName/HolyCMD)
