# Contributing

Contributions are always welcome and appreciated!

## Prerequisites

> [!note]
>
> You may skip these steps if you have already performed them before.

1. Install a [Git][git-install] client.

1. [Generate an SSH key pair][ssh-key-generate] and [add the public key to your github.com account][ssh-key].

1. Install [uv][uv-install] as a Python package, dependency, and version manager.

## Setup

1. Create a fork of this project in your personal namespace.

1. Clone the fork to your local machine. Then, change your current working directory to the root of the cloned project.

1. Install runtime and development dependencies:

    ```shell
    uv sync --locked --all-groups
    ```

1. Install Git pre-commit hooks to enable code quality checks when making a Git commit:

    ```shell
    uv run pre-commit install
    ```

## Development

1. Create a new branch:

    ```shell
    git checkout -b your-branch-name
    ```

1. Make changes and don't forget to implement tests.

    If you need to add or remove runtime dependencies, edit `pyproject.toml` by adding or removing a package in the section `[project]` under `dependencies`. Strictly pin runtime dependencies also in `pyproject.toml` for transparency and maintainability; broad version ranges are unnecessary and increase maintenance cost, as this application is not reused downstream. Similarly, development dependencies are located in the section `[dependency-groups]`. Finally, run `uv sync` in order to reflect the changes in the `uv.lock` file and to update the virtual environment.

1. Run or Test the CLI with

    ```shell
    uv run labeam --help
    ```

1. Run the test suite:

    ```shell
    uv run pytest
    ```

1. To view changes that affect the documentation, serve it locally:

    ```shell
    uv run mkdocs serve
    ```

    Then view it in the browser at [http://localhost:8000](http://localhost:8000).

    > [!tip]
    >
    > Disable URL validation by setting the environment variable `MKDOCS_HTMLPROOFER_ENABLED` to `false` to speed up local site builds.

1. Commit and push changes:

    ```console
    $ git add .
    $ uv run git commit
    Ruff – Format code.......................................................Passed
    Ruff – Lint..............................................................Passed
    mypy – Check typing......................................................Passed
    uv – Check `uv.lock`.....................................................Passed
    Trim trailing whitespace.................................................Passed
    Fix end of files.........................................................Passed
    Check for merge conflicts................................................Passed
    $ git push -u
    ```

    > [!note]
    >
    > (Some) GUI-based Git tools don't seem to support pre-commit hook execution or don't execute them within the context of the virtual environment.

1. Submit a merge request to this project.

## Changelog

To generate a [Keep a Changelog][keepachangelog]-formatted `CHANGELOG.md` from the Git history:

1. Fetch the latest Git history to ensure the version is bumped correctly:

    ```shell
    git fetch
    ```

1. Generate the changelog using [git-cliff]:

    ```shell
    uv run --only-group dev git-cliff --offline --bump --unreleased --prepend CHANGELOG.md
    ```

1. Consider curating the generated changelog to improve clarity and relevance.

    - Refine wording for consistency and readability.
    - Add brief context where a change would otherwise be unclear.
    - Deduplicate repeated user-facing dependency updates and show only the latest version bump.
    - Combine iterative commits into one logical changelog entry when they belong to the same overall change.

> [!important]
>
> Commits must follow the [Conventional Commits][conventional-commits] specification, otherwise generation fails with `commit ... is not conventional`. Either amend the offending commit or add a skip parser for its type to `cliff.toml`.

### Version bumping

[git-cliff] infers the next [SemVer][semver] version for the unreleased section from the conventional commits since the last tag:

| Commit type                              | Bump  |
|------------------------------------------|-------|
| `feat` type                              | minor |
| `!` or `BREAKING CHANGE:`                | major |
| Any other valid conventional commit type | patch |

## Releases

Releases are fully automated by Github Actions. To publish a new release:

1. Generate the changelog for the upcoming release as described in the [Changelog](#changelog) section. Review the prepended section, then commit the result to the default branch via a merge request.

1. Create and push a `vX.Y.Z` tag from the default branch:

    - Using the command line:

        ```shell
        git tag -a vX.Y.Z -m "Release vX.Y.Z"
        git push origin vX.Y.Z
        ```

## Versioning

This project conforms with [Semantic Versioning 2.0.0][semver]. The version is found in the file `pyproject.toml`.

[conventional-commits]: https://www.conventionalcommits.org
[ssh-key-generate]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
[ssh-key]: https://github.com/settings/keys
[git-cliff]: https://git-cliff.org
[git-install]: https://git-scm.com
[keepachangelog]: https://keepachangelog.com/en/1.0.0/
[semver]: https://semver.org
[uv-install]: https://docs.astral.sh/uv/getting-started/installation/#installation-methods
