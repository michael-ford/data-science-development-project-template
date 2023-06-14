# Data Science Development Project Template

_A logical, reasonably standardized, but flexible project structure for doing and sharing data science work **while developing a software tool**._


A project template for data science projects that uses [Cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/) for easy deployment. It is a direct modification of [Cookiecutter Data Science](https://github.com/drivendata/cookiecutter-data-science) to serve a use case common to research sciences (especially computational biology / bioinformatics) where a data science project is developed *alongside a software development project*.

It utilizes many new tools and best practices to data science:

- Reproducibility and data version control through [DVC](https://dvc.org/doc)
- Integration of a software development project using [git-subrepo](https://github.com/ingydotnet/git-subrepo)
- Experiment development and communication using [Jupyter-lab](https://jupyterlab.readthedocs.io/en/stable/)
- Environment reproducability and package management using [Conda](https://docs.conda.io/en/latest/) and [git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)

## Requirements to use the cookiecutter template:
-----------
 - Python 2.7 or 3.5
 - [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0: This can be installed with pip by or conda depending on how you manage your Python packages:

``` bash
$ pip install cookiecutter
```

or

``` bash
$ conda install -c conda-forge cookiecutter
```


## Setting up the new CoookieCutter project

```
cookiecutter https://github.com/michael-ford/data-science-development-project-template.git
```

Just follow the prompts to populate and build the new project!

## Final steps

After building the project, you'll want to do the following:

### Create Conda Environment

Conda is used to create a independent environment, isolated from your system intallations (especially python). Included is a basic python 3.7 conda environment containing standard DS tools (including everything mentioned here), and by default saved to `<YOUR-PROJECT-NAME>.yml`.

1. Create environment with `conda env create --file <YOUR-ENVIRONMENT-FILE-NAME>.yml`. 
2. Activate the environment with `conda activate <YOUR-ENV-NAME>`
3. Add the environment yml file to git and commit

### Set the conda git hooks as executable

By running `chmod u+x .git/hooks/pre-commit .git/hooks/post-merge`. 

The `pre-commit` hook overwrites the environment yml file with the current state of the conda environment using the following command:
```
conda env export -n <YOUR-ENV-NAME> --from-history | grep -v "^prefix" > <YOUR-ENVIRONMENT-FILE-NAME>
```
The `--from-history` argument prevents dependencies and binary versions from being included in the export, and `grep -v "^prefix"` removes the system-specific conda prefix to ensure cross-platform compatibility.

If the environment.yml file hasn't it hasn't changed, the commit proceeds. If it has changed, the commit aborts and the environment file is added to the index.

The `post-merge` hook checks the merged version of the environment yml, and if it has changed it updates the conda environment with 
```
conda env update -n <YOUR-ENV-NAME> -f <YOUR-ENVIRONMENT-FILE-NAME> --prune
```
Note: the `--prune` parameter removes unneeded dependencies, but due to a [bug in the current version of Conda (> 4.4)](https://github.com/conda/conda/issues/7279) any package removed from the yml will **not* be removed from the environment.

### Connect to github
First, [setup a bare repository](https://help.github.com/en/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line) elsewhere (e.g. Github) to serve as your remote. Then run the following:
```
git remote add origin <REMOTE-REPO-URL>
git remote -v
```

### Init DVC

    dvc init

### Setup software development project as a subrepo
If your DS project is supporting the development of some software development project, I recommend using [git-subrepo](https://github.com/ingydotnet/git-subrepo) to include it's repo in the project by cloning it as follows:

Install [git-subrepo](https://github.com/ingydotnet/git-subrepo): 
```
git clone https://github.com/ingydotnet/git-subrepo </PATH/TO/INSTALL-LOCATION>
echo 'source </PATH/TO/INSTALL-LOCATION>/git-subrepo/.rc' >> ~/.bashrc
```

Clone the software repo as a subrepo:
```
git subrepo clone <REPO-REMOTE-URL> src/<REPO-NAME> -b <DESIRED-BRANCH-NAME>
```
If you are starting off a software development project from scratch, consider using [Pyscaffold](https://pyscaffold.org/en/latest/). You can follow the following instructions to setup and configure the repo. Note if you want to use a remote (e.g. Github repo), set up a bare repo there first.

```
cd src/
putup <PROJECT-NAME>
cd ..
git subrepo init src/<PROJECT-NAME> -r <REMOTE-PATH>
```

Note if you would to use a branch other than `master`, checkout that branch before the `git subrepo init` and add `-b <BRANCH-NAME>` to the `git subrepo init` command (see [note about git subrepo branches](#develop-your-software-project-within-the-ds-project-using-git-subrepo) below).

#### Install code in src/ as a python package

`pip install -e .` will setup the `src/` directory as a python package. 

Note it is recommended to install your subrepo as a python package [independent from other code in src/](#process-and-generate-data-through-standalone-scripts-stored-in-src). By default your subrepo is excluded from the package install of `src/` (as defined in `setup.py`), so you have to install is seperately by running `pip install -e .` in the subrepo.


## The resulting directory structure
------------

The directory structure of your new project will look something like this: 

```
├── data
│   ├── external                        <- Data from third party sources.
|   |   └── SOURCE.tsv                  <- Record of data sources when not using `dvc run`
│   ├── interim                         <- Intermediate data that has been transformed.
│   ├── raw                             <- The original, immutable data dump.
│   └── results                         <- Final results
|
├── environment.yml                     <- Conda environment definition for reproducing 
|
├── experiments                         <- Experiments devided by subdirectory
│   └── 03-04-14.sample-experiment      <- Sample demonstrating the structure
│       ├── data -> ../../data/         <- Softlink to data/ for code cleanliness
│       ├── notebooks                   <- Jupyter notebooks for experiment
|       |   └── template.ipynb          <- Sample notebook containing useful code
│       └── results                     <- Final reports for communication (e.g. html 
|           |                              version of jupyter nb)
│           └── figures                 <- Figures for reports
|
├── LICENSE
├── README.md                           <- The top-level README for developers using 
|                                          this project.
├── setup.py                            <- Configuration for installing src/ as python package
|
└── src                                 <- Source code for use in this project.
    ├── data                            
    │   └── __init__.py
    └── __init__.py                     <- Makes src a Python module
```

## Workflow
-----------

### Process and generate data through standalone scripts stored in src/
Any step in an experiment that *fetches raw data*, *generates data* or *creates results* that is **longer than a one-liner** should be developed as a standalone script. This keeps your notebooks clean, but also helps ensure **data reproducability** later (see below).

The `setup.py` script installs yout `src/` directory as a package in the conda environment, so can import any python code stored in src/ module. For example:
```
from src.data.clean import clean_raw_dataset
``` 


### Version Control, Backup Data and Reproducible Methods using DVC
This project uses [Data Version Control (DVC)](https://dvc.org/doc) for the following purposes:
1. Version control data files that shouldn't / are too big to be managed with Git
2. Ensure method repoducibility
3. [Backup data files to a remote](https://dvc.org/doc/command-reference/remote) 

The best way to aid in reproducibility using DVC is with the [`dvc run`](https://dvc.org/doc/command-reference/run) command. Here's an example performing a simple read mapping common to bioinformatics:

```
dvc run -n mapping_stage_name -o output_file -d reference.fa -d source.fq "bwa mem reference.fa source.fq > output_file"
```

This does the following things:
1. Runs the command `bwa mem reference.fa source.fq > output_file`
2. Caches the `output_file` and replaces it with a symlink to the cache
3. Adds an `output_file` stage to the `dvc.yaml` file,  which encodes the **command**, inputs and ouputs. Also tracks the version (md5 hash) of the **dependecy files** (reference.fa, source.fq) and **output_file** in the `dvc.lock` file.

By adding `dvc.yaml`, `dvc.lock` to your git commit, you not only track *how* `output_file` was created, but also the *versions* of the files that were used to create it (dependencies), and the *expected version* of the resulting `output_file`. And finally, you can recreate `output_file` by simply running `dvc repro output_file`.

Using the dependecies feature creates a DAG of file dependencies, so that when `dvc repro` is run and the needed dependencies are not available, it will iteratively reproduce upstream dependencies to recreate them.

There are other ways of adding data files to DVC such as `dvc add` and `dvc commit`. I recommend reading through the docs once you run into a use case that is different from the above. 

Additionally, you can [setup a remote specifically for DVC](https://dvc.org/doc/command-reference/remote) (such a AWS S3) and backup your data there using [`dvc push`](https://dvc.org/doc/command-reference/push) and [`dvc pull`](https://dvc.org/doc/command-reference/pull).


### Run experiments in Jupyter Lab
Jupyter Lab offers many features that make it an ideal base from which to run experiments, from data generation to results analysis. The idea being that someone could open a notebook and press 'Run all', and not only have the entire experiment reproduced, but also understand what is happening. Therefore it is important to keep in mind that the notebook purpose is to act as a *driver* and *communicator* for the experiment - external scripts (in `src/`) should be used to keep code streamlined and minimal, and markdown text should be liberally used to explain the process. For more information of Jupyter use see [this excellent blog post](https://florianwilhelm.info/2018/11/working_efficiently_with_jupyter_lab/).

The default conda environment includes a package called [nb_conda_kernels](https://github.com/Anaconda-Platform/nb_conda_kernels). This ensures that a Jupyter session run from this environment will automatically detect any other conda environments and add them as jupyter kernels, as long as they have the `ipykernel` package installed

The default environment includes the [`nbdime`](https://nbdime.readthedocs.io) package, which allows git to [play nicely with jupyter notebooks](https://nbdime.readthedocs.io/en/latest/#git-integration-quickstart).

### Link Jupyter notebooks with DVC using [Papermill](https://papermill.readthedocs.io/en/latest/)
You can link your notebooks into DVC stages using the papermill tool (provided in the default conda environment). For info on using papermill with jupyter checkout [this blog post](https://medium.com/y-data-stories/automating-jupyter-notebooks-with-papermill-4b8543ece92f).

First, you need to make sure papermill can find your conda environment kernel by [following these instructions](https://github.com/Anaconda-Platform/nb_conda_kernels#use-with-nbconvert-voila-papermill). Take note of the kernel name by running `jupyter kernelspec list` (should be in the form of `conda-env-<env-name>`).

Essentially you will be running your jupyter notebook using papermill *through `dvc run`*. Here's an example of a dvc stage:

```
dvc run -n my_stage \
-d dependency.data
-o output.txt
"papermill --kernel conda-env-<env-name> <input-notebook-path> <output-notebook-path> -p <parameter-name> <parameter-value>"
```

### Create new experiment directories with *another* cookiecutter

You can create new experiment directories by copying the provided example or using another cookiecutter as follows:

```
cd experiments
cookiecutter https://github.com/michael-ford/new-experiment-template
```

#### Develop your software project within the DS project using Git Subrepo

[Git-subrepo](https://github.com/ingydotnet/git-subrepo) allows you to keep include software project as a seperate repo, but *include the version/state* of the project in your larger DS project commits. Generally it works the same as git, but there are some key things to keep in mind:

- It is not a standalone repository - the subrepo needs to have a proper repository elsewhere as a remote
- You can only have a **single branch** in the project at once. To switch to another branch, you need to re-clone the subrepo using the `--force` argument: `git subrepo -f clone src/<REPO-NAME> -b <BRANCH-NAME> -r <REMOTE-PATH>`. 
  Depending on your git workflow this might constrain how much development you do in the subrepo (but thats why you have a proper remote repository right? :)
- You can push new commits in your subrepo to its parent remote using `git subrepo push`. 
- Any commit in the parent DS project repo that contains files from the subrepo *will go into the commit history of the subrepo*. This does make sense (since how would you sync the branches between the DS repo and subrepo), but it means you may want to commit your subrepo changes independently and **before** you commit and DS repo changes.
