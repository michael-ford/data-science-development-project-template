#! /bin/bash

conda env create -f {{ cookiecutter.conda_environment_file }}
eval "$(conda shell.bash hook)"
prefix=$(which python | awk -F'/' '{OFS="/"; $NF="/"; $(NF-1)=""; print $0 }' | sed 's/\/\/*$//')
conda activate {{ cookiecutter.conda_environment_name }}
python setup.py develop

if [ -d "./git-hooks" ]; then
    # Execute your command here
    cd .git/hooks && ln -s ../../git-hooks/* ./ && cd ../..
fi

python -m ipykernel install --name {{ cookiecutter.conda_environment_name }} --display-name "python3 ({{ cookiecutter.conda_environment_name }})" --prefix $prefix --env PATH $PATH

echo "Setup complete! Activate the environment by running `conda activate {{ cookiecutter.conda_environment_name }}`"
