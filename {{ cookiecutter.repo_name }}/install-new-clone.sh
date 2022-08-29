#! /bin/bash

conda env create -f {{ cookiecutter.conda_environment_file }}
eval "$(conda shell.bash hook)"
conda activate {{ cookiecutter.conda_environment_name }}
python setup.py develop
while true; do
    read -p "Would you like to the modify the DVC cache directory for this project? " yn
    case $yn in
        [Yy]* ) read -p "Please Enter Path: " dvc_path; dvc cache $dvc_path; break ;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
echo "Setup complete! Activate the environment by running `conda activate {{ cookiecutter.conda_environment_name }}`"
