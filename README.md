# Devinci Configuration Management

This project facilitates the management of configuration files, aliases, environment variables, and custom paths in the Devinci system. It automates the generation and updating of configuration files based on modifications made to the corresponding `.ini` files located in the `registration.d` directory.

## Overview

The Devinci Configuration Management project consists of several components:

1. **Aliases Management**: Automatically generates and updates the `aliases.sh` file based on modifications made to the `alias.ini` file in the `registration.d` directory.

2. **Environment Variables Management**: Automatically generates and updates the `env.sh` file based on modifications made to the `env.ini` file in the `registration.d` directory.

3. **Custom Paths Management**: Automatically generates and updates the `path.sh` file based on modifications made to the `path.ini` file in the `registration.d` directory.

4. **Configuration Update Script**: The `update.sh` script serves as an automated updater for configuration files. It performs integrity checks to ensure that modifications made to essential scripts do not prevent successful updates.

## Features

### Aliases Management

The `aliases.sh` script serves as the central repository for defining shell aliases in the Devinci system. It automatically generates aliases from the `alias.ini` file and provides guidelines for managing aliases effectively.

### Environment Variables Management

The `env.sh` script serves as the central repository for defining environment variables in the Devinci system. It automatically generates environment variables from the `env.ini` file and provides guidelines for managing environment variables efficiently.

### Custom Paths Management

The `path.sh` script serves as the central repository for defining custom paths in the Devinci system. It automatically generates custom paths from the `path.ini` file and provides guidelines for managing custom paths conveniently.

### Configuration Update Script

The `update.sh` script automates the process of updating configuration files based on modifications made to the `.ini` files in the `registration.d` directory. It performs integrity checks to ensure the stability and functionality of the system configuration.

## Usage

1. **Adding or Modifying Configurations**:
   - Edit the corresponding `.ini` file in the `registration.d` directory to add, remove, or modify configurations.
   - Follow the guidelines provided in the docstrings of each `.ini` file for proper formatting and syntax.

2. **Applying Changes**:
   - Execute the `update.sh` script to automatically update configuration files with the latest changes made to the `.ini` files.
   - The script ensures integrity and stability by performing necessary checks before applying updates.

3. **Managing Aliases, Environment Variables, and Paths**:
   - Use the provided scripts (`aliases.sh`, `env.sh`, `path.sh`) to manage aliases, environment variables, and custom paths effectively.
   - Avoid direct modifications to these scripts to prevent conflicts and ensure consistency.

## Directory Structure

The project directory structure is organized as follows:

- `aliases.d`: Contains generated alias scripts.
- `compiler`: Contains scripts for compiling configuration files.
- `custom_env_vars.d`: Directory for custom environment variables (not implemented yet).
- `docs`: Documentation files including markdown files and docstrings.
- `language_specific.d`: Directory for language-specific configurations.
- `management`: Scripts for initializing and updating configurations.
- `registration.d`: Contains `.ini` files for defining configurations.
- `startup_scripts.d`: Directory for startup scripts.
- `stubs.d`: Contains stub files for generating scripts.
- `update.sh`: Script for updating configurations.

## Author

- [devinci-it](https://github.com/devinci-it)

