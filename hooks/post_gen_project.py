import os

print("""

-------------------------
Success! Project created!
-------------------------
Configuring desired features...
""")

conda_install = '{{ cookiecutter.conda_install }}'.split(' -')[0] == 'Yes'
if conda_install:
    print(f"Installing default conda environment...")
    os.system("conda env create -f {{ cookiecutter.conda_environment_file }} --experimental-solver libmamba")
    os.system('eval "$(conda shell.bash hook)" && conda activate {{ cookiecutter.conda_environment_name}}')
else:
    print("""Not installing default conda environment - after modification install the environment:
1.  Created your conda environment (modify as needed) - `conda env create -f {{ cookiecutter.conda_environment_file }}`
2.  Activate your conda environment - `conda activate {{ cookiecutter.conda_environment_name}}`""")


init_git = '{{ cookiecutter.init_git }}'.split(' -')[0] == 'Yes'
if init_git:
    print('\nInitializing git...')
    os.system('git init')


copy_git_hooks = '{{ cookiecutter.conda_git_hooks }}'.split(' -')[0] == 'Yes'
if not copy_git_hooks:
    os.system('rm .git/hooks/pre-commit .git/hooks/post-merge')
else:
    print(f"\nSetting the conda git hooks as executable - `chmod u+x .git/hooks/pre-commit .git/hooks/post-merge`...")
    os.system('chmod u+x .git/hooks/pre-commit .git/hooks/post-merge')

dvc_init = '{{ cookiecutter.dvc_init }}'.split(' -')[0] == 'Yes'
if dvc_init:
    print(f"\nInitializing DVC...")
    os.system('dvc init')

dvc_path = '{{ cookiecutter.dvc_cache_path }}'
if '[OPTIONAL]' not in dvc_path:
    if os.path.isdir(dvc_path):
        os.system(f"dvc cache {dvc_path}")
    else:
        print(f"ERROR: Cannot change DVC cache path: {dvc_path} doesn't exist")

print(f"\nAdding {{ cookiecutter.conda_environment_file }} - `git add {{ cookiecutter.conda_environment_file }}`")
os.system('git add {{ cookiecutter.conda_environment_file }}')

print(f"Running `python setup.py develop` to install src/ as a python module...")

intialize_subrepo = '{{ cookiecutter.subrepo_name }}' if '[OPTIONAL]' not in '{{ cookiecutter.subrepo_name }}' else None
if intialize_subrepo:
    print(f"Installing git-subrepo and setup (see README.md)...")
    print("NOT IMPLEMENTED")    
print('\n')

