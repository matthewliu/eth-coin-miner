#!/bin/bash
# Sets the python path to include the python directory
# of this project, so that imports can be written as relative,
# but you can still run scripts interactively from the commandline.
# Also activates the virtualenv for this project.

set -x
echo "Starting env.sh script"

# Determine the project root directory (one level up from the script location)
if [[ -n "$ZSH_VERSION" ]]; then
    # For Zsh
    SCRIPT_PATH="${(%):-%N}"
else
    # For Bash
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi

PROJECTPATH=$(cd "$(dirname "$SCRIPT_PATH")" && pwd)
ENV_DIR=$(dirname "$PROJECTPATH")

echo "PROJECTPATH: $PROJECTPATH"
echo "ENV_DIR: $ENV_DIR"

# Deactivate any existing virtual environment
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "Deactivating current virtual environment: $VIRTUAL_ENV"
    deactivate
    echo "Deactivation complete"
fi

# Activate the virtual environment
ACTIVATE_SCRIPT="$ENV_DIR/bin/activate"
echo "Attempting to activate virtual environment from: $ACTIVATE_SCRIPT"
if [[ -f "$ACTIVATE_SCRIPT" ]]; then
    source "$ACTIVATE_SCRIPT"
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo "Virtual environment activated: $VIRTUAL_ENV"
    else
        echo "Error: Virtual environment activation failed"
        exit 1
    fi
else
    echo "Error: Cannot find activate script at $ACTIVATE_SCRIPT"
    exit 1
fi

# Set PYTHONPATH
if [[ $PYTHONPATH != *"$PROJECTPATH"* ]]; then
    export PYTHONPATH="$PROJECTPATH:$PYTHONPATH"
fi

# Change to the project directory
cd "$PROJECTPATH"

echo "Current directory: $(pwd)"
echo "PYTHONPATH: $PYTHONPATH"
echo "PATH: $PATH"
which python
python --version
