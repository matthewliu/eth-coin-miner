# Sets the python path to include the python directory
# of this project, so that imports can be written as relative,
# but you can still run scripts interactively from the commandline.
# Also activates the virtualenv for this project.

# Adaptation for Zsh
if [[ -n "$ZSH_VERSION" ]]; then
    # For Zsh
    echo "Current script: ${(%):-%N}"
    ENV_DIR=$(cd "$(dirname "${(%):-%N}")" && pwd)
else
    # For Bash
    echo "Current BASH_SOURCE: ${BASH_SOURCE[0]}"
    ENV_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
fi

export PROJECTPATH=$ENV_DIR
if type deactivate &>/dev/null || whence -p deactivate &>/dev/null; then
    deactivate
fi
source "$ENV_DIR/../bin/activate"
if [[ $PYTHONPATH != *"$ENV_DIR"* ]]
then
    export PYTHONPATH="$ENV_DIR/python:$PYTHONPATH"
fi
cd $ENV_DIR

echo "Using virtual environment $VIRTUAL_ENV with project path $PROJECTPATH."