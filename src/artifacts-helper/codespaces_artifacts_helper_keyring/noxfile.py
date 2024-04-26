import os

import nox

os.environ.update({"PDM_IGNORE_SAVED_PYTHON": "1"})

PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12"]
LOCATIONS = "src", "tests", "noxfile.py"


@nox.session
@nox.parametrize(
    "python,keyring",
    [
        (python, keyring)
        for python in PYTHON_VERSIONS
        for keyring in ("20", "25.1")
        # exclude keyring 20 because it is incompatible with python 3.12
        if (python, keyring) != ("3.12", "20")
    ],
)
def tests(session, keyring):
    session.run_always("pdm", "install", "-G", "test", external=True)
    session.install(f"keyring=={keyring}")
    session.run("pdm", "test", *session.posargs, external=True)


@nox.session
def lint(session):
    session.run_always("pdm", "install", "-G", "lint", external=True)
    session.run("pdm", "check", external=True)


@nox.session(py=PYTHON_VERSIONS)
def mypy(session):
    session.run_always("pdm", "install", external=True)
    args = session.posargs or LOCATIONS
    session.run("pdm", "run", "mypy", *args, external=True)
