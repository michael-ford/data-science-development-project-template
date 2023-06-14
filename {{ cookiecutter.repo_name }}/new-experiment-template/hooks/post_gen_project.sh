#! /usr/bin/env bash
ln -s ../../data ./
expr_name = '{{ cookiecutter.experiment_dir_name }}'
mkdir data/$expr_name
