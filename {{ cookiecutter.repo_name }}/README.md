{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}

Clone instructions
------------------

### Automatic
Run `./setup-new-clone.sh`

### Manual
1. git clone the repo
2. Run `conda env create -f {{ cookiecutter.conda_environment_file }}`
3. `conda activate {{ cookiecutter.conda_environment_file }}`
4. Install `src` as python package: `python setup.py develop`

Project Organization
```
------------

├── data
│   ├── external                        <- Data from third party sources.
│   ├── interim                         <- Intermediate data that has been transformed.
│   ├── raw                             <- The original, immutable data dump.
│   └── results                         <- Final results
|
├── environment.yml                     <- Conda environment definition for reproducing  
|
├── experiments                         <- Experiments devided by subdirectory (see `new-experiment-template/README.md` for instructions on replicating)
│   └── 03-04-14.sample-experiment      <- Sample demonstrating the structure
│       ├── data -> ../../data/         <- Softlink to data/ for code cleanliness
│       ├── notebooks                   <- Jupyter notebooks for experiment
│       └── results                     <- Final results
│           └── figures                 <- Figures 
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
--------

<p><small>Project based on the <a target="_blank" href="http://github.com/michael-ford/data-science-development-project-template">Data Science Development Project Template</a>, a fork of <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a></small></p>
