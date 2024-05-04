#!/bin/bash

# env.sh
#
# This script serves as the central repository for defining environment variables in the Devinci system.
# Environment variables are used to configure various aspects of the system and applications, providing
# flexibility and customization options.
#
# Usage:
#   Do not directly modify this script. It is automatically generated from the env.ini file
#   located in the registration.d directory. To update environment variables, follow these steps:
#   1. Modify the env.ini file in the registration.d directory to add, remove, or modify environment variables.
#   2. Run the update.sh script to generate the updated env.sh file and apply the changes.
#
# Important:
#   Do not directly modify this script. Any changes made directly to this script will be overwritten
#   the next time the update.sh script is run. Instead, modify the env.ini file and run the update.sh
#   script to apply the changes.
#
# Note:
#   The env.ini file follows a specific format. Each section represents an environment variable, with the
#   variable name enclosed in square brackets ([]). Within each section, specify the value of the variable.
#   Comments in the .ini file are indicated by a '#' symbol.
#   Example:
#     [PATH]
#     value=/usr/local/bin:/usr/bin:/bin
#
#     [EDITOR]
#     value=vim
#

# Automatically generated environment variables
# ------------------------------------------------------------
# This section contains environment variables automatically generated from the env.ini file.
# Avoid manually editing environment variables in this section, as they will be overwritten.
# ------------------------------------------------------------

export EXAMPLE_VARIABLE='example_value'
