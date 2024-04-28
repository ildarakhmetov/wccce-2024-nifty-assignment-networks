# Nifty Assignment Gradescope Autograder

This folder contains the Gradescope autograder for the Nifty Assignment.

## Running the autograder locally

> If you don't have Docker installed, please follow the instructions [here](https://docs.docker.com/get-docker/) to install it.

Get to the root of this repository. Build the containter using `docker-compose`:

```bash
docker-compose build
```

Next, define the `AUTOGRADER_PATH` environment variable to point to the path of this repository on your local machine. For example, if you cloned this repository to `/home/ildar/cs5008/autograders/autograder-sp24-hw7`, you would run:

```bash
export AUTOGRADER_PATH=/home/username/autograders/nifty-autograder
```

Run the container (bypassing the Gradescope autograder harness):

```bash
docker-compose run --rm -v $AUTOGRADER_PATH/solution:/autograder/submission -v $AUTOGRADER_PATH/results:/autograder/results rockylinux /autograder/run_autograder
```

The autograder will run and the results will be saved to the `results` directory as a JSON file. Review the results to ensure that the autograder is working as expected.

If you need to debug the autograder, you can run the container in interactive mode:

```bash
docker-compose run --rm -v $AUTOGRADER_PATH/solution:/autograder/submission -v $AUTOGRADER_PATH/results:/autograder/results rockylinux /bin/bash
```

This will drop you into a shell inside the container. You can then run the autograder manually:

```bash
/autograder/run_autograder
```

Or, you can cd into the `/autograder` directory and debug the tests manually.

## Documentation

Documentation for the autograder can be found in the `docs/` directory.

To regenerate the documentation, run from the root of the repository:

```bash
pdoc source/tests/test_* -o docs
```

This will regenerate the documentation in the `docs/` directory.

The `pdoc` tool can be installed using pip:

```bash
pip install pdoc
```