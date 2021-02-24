import os

init_git = '{{ cookiecutter.init_git }}'.split(' -')[0] == 'Yes'
if init_git:
    print('\nInitializing git...')
    os.system('git init')

print("""

-------------------------
Success! Project created!
-------------------------
Before you start working, dont forget to head to your project and:
1.  Created your conda environment (modify as needed) - `conda env create -f {{ cookiecutter.conda_environment_file }}`
2.  Activate your conda environment - `conda activate {{ cookiecutter.conda_environment_name}}`""")
info_counter = 3

copy_git_hooks = '{{ cookiecutter.conda_git_hooks }}'.split(' -')[0] == 'Yes'
if not copy_git_hooks:
    os.system('rm .git/hooks/pre-commit .git/hooks/post-merge')
else:
    if not init_git:
        print(f"{info_counter}.  Initialize the project as a git repo - `git init`")
        info_counter +=1
        
    print(f"{info_counter}.  Set the conda git hooks as executable - `chmod u+x .git/hooks/pre-commit .git/hooks/post-merge`")
    info_counter +=1

    print(f"{info_counter}.  Add and commit {{ cookiecutter.conda_environment_file }} - `git add {{ cookiecutter.conda_environment_file }} && git`")
    info_counter +=1

print(f"{info_counter}.  Run `python setup.py develop` to install src/ as a python module")
info_counter +=1

print('subrepo_name')
print('{{ cookiecutter.subrepo_name }}')
intialize_subrepo = '{{ cookiecutter.subrepo_name }}' if '[OPTIONAL]' not in '{{ cookiecutter.subrepo_name }}' else None
if intialize_subrepo:
    print(f"{info_counter}.  Install git-subrepo and setup (see README.md)")
    info_counter +=1
    
print('\n')

