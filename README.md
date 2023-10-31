# Anaconda Packaging Utilities

## Table of Contents
<!-- TOC -->

- [Anaconda Packaging Utilities](#anaconda-packaging-utilities)
    - [Table of Contents](#table-of-contents)
    - [Overview](#overview)
- [Getting Started](#getting-started)
    - [Installation](#installation)
- [How to Contribute](#how-to-contribute)
    - [Project Tenets](#project-tenets)
    - [Developer setup](#developer-setup)
    - [pre-commit](#pre-commit)
        - [Running pre-commit checks](#running-pre-commit-checks)
    - [Adding a dependency](#adding-a-dependency)
    - [Development Dependencies](#development-dependencies)
    - [Release process](#release-process)
    - [Explanation of Configuration Files](#explanation-of-configuration-files)

<!-- /TOC -->

## Overview
This project is a culmination of libraries and utilities developed and maintained by the Packaging
Automation and Tooling (PAT) Team at Anaconda. These modules are consumed by our various projects.

# Getting Started

## Installation
To get started, install `cd` into this repo and create the environment:
```sh
$ make environment
$ conda activate anaconda-packaging-utils
```
Then create a custom configuration file by copying the template:
```sh
$ cp anaconda-packaging-utils-config-template.yaml ~/.anaconda-packaging-utils-config.yaml
```
Be sure to edit your `~/.anaconda-packaging-utils-config.yaml` file with the parameters listed, filling out all the
`TODO` remarks. The comments will help you along your way.

**NEVER** commit your personal changes to the template file!

# How to Contribute
Please read the following section if you would like to contribute to this project.

## Project Tenets
TODO, adapt from `recipe_bootstrap Milestone 1` planning doc.

## Developer setup
```sh
$ make dev
$ conda activate anaconda-packaging-utils
```
Notes on `make dev`:
- This will blow away the existing conda environment, to ensure a clean development experience.
- This will run `pre-commit install` so `git commit` will automatically execute our linter rules, tests, etc

## pre-commit
`pre-commit` is configured for this project to run a number of checks using standard Python development tools:
- `black` - Python code formatter
- `pylint` - Python linter
- `mypy` - Python static code analysis tool
- `pytest` - Python testing framework

This project uses a slightly modified form of
[Google's Style guide for Python](https://google.github.io/styleguide/pyguide.html) as a basis for style.

Note that the project environment also installs these tools so developers may attempt to run them independently of
`pre-commit`.

Before committing to this project, add any new files to staging and then make sure to run:
```sh
$ make pre-commit
```
This ensures your commit passes our coding standards. These checks will be enforced by our CI/CD pipeline.

### Running pre-commit checks
The provided `Makefile` also provides a handful of convenience recipes for running all or part of the `pre-commit`
automations:
1. `make test`: Runs all the unit tests
1. `make test-cov`: Reports the current test coverage percentage and indicates
   which lines are currently untested.
1. `make lint`: Runs our `pylint` configuration, based on Google's Python
   standards.
1. `make format`: Automatically formats code
1. `make analyze`: Runs the static analyzer, `mypy`.
1. `make pre-commit`: Runs all the `pre-commit` checks


## Adding a dependency
When a dependency is added to this project, make sure to update the following files:
- `environment.yaml`
You may need newer versions of tools that include type-annotations in order
for `mypy` to correctly analyze any new dependencies. To get around this:
- Make a request for a new package so that the package can be added in the future.
- Prepend `conda-forge::` to install a version from the open source community.
You can also use `conda install -c conda-forge` or `pip install` to test packages. Be sure to rebuild your
environment after testing to ensure you match the environment that is installed for everyone else.

Be sure to re-run `conda deactivate && make dev` to add the new dependencies. `pre-commit` may take more time to execute
on the first run after adding new dependencies.

## Development Dependencies
In the event that you need to work on/edit another `conda` package while developing in this repository, you will need to
install the "development" version of the package.

To do this, temporarily comment out the package of interest in the `environment.yaml` file. Then run the following
commands to rebuild your development environment:

```sh
conda deactivate # If you are working in the target environment already
make dev
conda activate anaconda-packaging-utils
conda develop path_to_git_repo
```

Any changes on your development (local) copy of the other package should now be automatically reflected when executed
from `anaconda-packaging-utils`.

Make sure that you un-comment the package name from `environment.yaml` so that the change is not accidentally committed.

## Release process
Here is a rough outline of how to conduct a release of this project:
1. Update `CHANGELOG.md`
1. Update the version number in `pyproject.toml`
1. Ensure `environment.yaml` is up to date with the latest dependencies
1. Create a new release on GitHub with a version tag.
1. The Anaconda packaging team will need to update
[the feedstock](https://github.com/AnacondaRecipes/anaconda-packaging-utils-feedstock)
and [aggregate](https://github.com/AnacondaRecipes/aggregate) and publish to `distro-tooling`


## Explanation of Configuration Files
Here is a brief summary of the configuration files included by this repoistory:
- `.coveragerc`: `pytest-cov` configuration for managing `pytest` coverage requirements.
- `.mypy.ini`: `mypy` Configuration file, used to set static analyzer settings.
- `.pre-commit-config.yaml`: Configures pre-commit to automatically run our commit acceptance criteria tools.
- `.pylintrc`: Configures style guide acceptance criteria. Adapated from
  [Google's Python code standards](https://google.github.io/styleguide/pyguide.html).
- `environment.yaml`: Environment file for the `conda` project environment.
