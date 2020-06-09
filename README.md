# Data Science Development Project Template

_A logical, reasonably standardized, but flexible project structure for doing and sharing data science work **while developing a software tool**.


This is a project template for data science projects that uses [Cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/) for easy deployment. It is a direct modification of [Cookiecutter Data Science](https://github.com/drivendata/cookiecutter-data-science) to serve a use case common to research sciences (especially computational biology / bioinformatics) where a data science project is developed *alongside a software development project*.

It utilizes many new tools and best practices to data science:

- Reproducability and data version control through [DVC](https://dvc.org/doc)
- Integration of a software development project using [git-subrepo](https://github.com/ingydotnet/git-subrepo)
- Experiment development and communication using [Jupyter-lab](https://jupyterlab.readthedocs.io/en/stable/)
- Environment reproducability and package management using [Conda](https://docs.conda.io/en/latest/)

### Requirements to use the cookiecutter template:
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

### Starting a new project:
------------

#### 1. Setup the repository


Run:
`cookiecutter https://github.com/michael-ford/data-science-development-project-template.git`

#### 2. Setup Git
First, [setup a bare repository](https://help.github.com/en/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line) elsewhere (e.g. Github) to serve as your remote. Then run the following:
```
git init
git remote add origin <REMOTE-REPO-URL>
git remote -v
```
#### 2. Create Conda Environment


Conda is used to create a independent environment, isolated from your system intallations (especially python). Included is a basic python 3.7 conda environment containing standard DS tools (including everything mentioned here), and is stored in `environment.yml`. The default environment name is the same as your repo name (this can be changed by editing `environment.yml`)

1. Create environment with `conda create --file environment.yml`. 
2. Activate the environment with `conda activate <NEW-ENV-NAME>`

#### 3. Setup DVC

    dvc init

#### 4. Setup in software project as a subrepo
If your DS project is supporting the development of some software development project, you can include that repo by cloning it as follows:

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

1. `cd src/`
2. `putup <PROJECT-NAME>`
3. `cd ..`
4. `git subrepo init src/<PROJECT-NAME> -r <REMOTE-PATH>`

Note if you would to use a branch other than `master`, checkout that branch before the `git subrepo init` and add `-b <BRANCH-NAME>` to the `git subrepo init` command (see [note about git subrepo branches](#develop-your-software-project-within-the-ds-project-using-git-subrepo) below).

#### 5. Install code in src/ as python packages

`python setup.py develop` will setup the `src/` directory as a python package installed in the conda environment. 

Note it is recommended to install your subrepo as a python package [independent from other code in src/](#process-and-generate-data-through-standalone-scripts-stored-in-src). By default your subrepo is excluded from the package install of `src/` (as defined in `setup.py`), so you have to install is deperately by running `python setup.py develop` in the subrepo.




### The resulting directory structure
------------

The directory structure of your new project looks like this: 

```
├── data
│   ├── external                        <- Data from third party sources.
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
│       └── reports                     <- Final reports for communication (e.g. html 
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

### Workflow
-----------
#### Run experiments from Jupyter Lab
Jupyter Lab offers many features that make it an ideal base from which to run experiments, from data generation to results analysis. The idea being that someone could open a notebook and press 'Run all', and not only have the entire experiment reproduced, but also understand what is happening. Therefore it is important to keep in mind that  the notebook should be a *driver* for the experiment - external packages should be used to keep code streamlined and minimal, and markdown text should be liberally used to explain the process. For more information of Jupyter use see [this excellent blog post](https://florianwilhelm.info/2018/11/working_efficiently_with_jupyter_lab/).

#### Process and generate data through standalone scripts stored in src/
Any step in an experiment that *fetches raw data*, *generates data* or *creates results* that is **longer than a one-liner** should be developed as a standalone script. This keeps your notebooks clean, but also helps ensure **data reproducability** later (see below).

You can import any python code stored in src/ as a package in your jupyter notebook. For example
`from src.data.clean import clean_raw_dataset` 

#### Version Control, Reproduce and Backup Data using DVC
This project uses [Data Version Control (DVC)](https://dvc.org/doc) to keep track of data files that shouldn't / are too big to be managed with Git. 

The best way to aid in reproducability using DVC is with the [`dvc run`](https://dvc.org/doc/command-reference/run) command. Here's an example performing a simple read mapping common to bioinformatics:

`dvc run -f output_file.dvc -o output_file -d reference.fa -d source.fq "bwa mem reference.fa source.fq > output_file"`

This does the following things:
1. Runs the command `bwa mem reference.fa source.fq > output_file`
2. Caches the `output_file` and replaces it with a symlink to the cache
3. Generates the `output_file.dvc` which encodes the **command** as well as the version of the **dependecy files** (reference.fa, source.fq) and the version of the **output_file**

By adding `output_file.dvc` to your git commit, you not only track *how* `output_file` was created, but also the *versions* of the files that were used to create it (dependencies), and the *expected version* of the resulting `output_file`. And finally, you can recreate `output_file` by simply running `dvc repro output_file.dvc`.

Using the dependecies feature creates a DAG of file dependencies, so that when `dvc repo` is run and the needed dependencies are not available, it will iteratively reproduce upstream dependencies to recreate them.

Thankfully, you can run these commands from within a Jupyter notebook - the example Jupyter notebook `experiments > 03-04-14.sample-experiment > notebooks > template.ipynb` includes a dvc_run function that integrates this processes seamlessly into your notebook workflow.

There are other ways of adding data files to DVC like `dvc add`, `dvc commit` and `dvc pipeline`. I recommend reading through the docs once you run into a use case that is different from the above. 

Additionally, you can [setup a remote specifically for DVC](https://dvc.org/doc/command-reference/remote) (such a AWS S3) and backup your data there using [`dvc push`](https://dvc.org/doc/command-reference/push) and [`dvc pull`](https://dvc.org/doc/command-reference/pull).

#### Develop your software project within the DS project using Git Subrepo

[Git-subrepo](https://github.com/ingydotnet/git-subrepo) allows you to keep include software project as a seperate repo, but *include the version/state* of the project in your larger DS project commits. Generally it works the same as git, but there are some key things to keep in mind:

- It is not a standalone repository - the subrepo needs to have a proper repository elsewhere as a remote
- You can only have a **single branch** in the project at once. To switch to another branch, you need to re-clone the subrepo using the `--force` argument: `git subrepo -f clone src/<REPO-NAME> -b <BRANCH-NAME> -r <REMOTE-PATH>`. 
  Depending on your git workflow this might constrain how much development you do in the subrepo (but thats why you have a proper remote repository right? :)
- You can push new commits in your subrepo to its parent remote using `git subrepo push`. 
- Any commit in the parent DS project repo that contains files from the subrepo *will go into the commit history of the subrepo*. This does make sense (since how would you sync the branches between the DS repo and subrepo), but it means you may want to commit your subrepo changes independently and **before** you commit and DS repo changes.