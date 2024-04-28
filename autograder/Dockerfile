# Set the base image to the autograder-base image
ARG BASE_REPO=gradescope/autograder-base
ARG TAG=rocky-8

# Use the autograder-base image as the base image
FROM ${BASE_REPO}:${TAG}

# If the /autograder/source directory exists, clean it up
RUN if [ -d /autograder/source ]; then rm -rf /autograder/source; fi

# Copy the source directory into the container
ADD source /autograder/source

# Copy the run_autograder script and setup.sh into the container
RUN cp /autograder/source/run_autograder /autograder/run_autograder
RUN cp /autograder/source/setup.sh /autograder/setup.sh


# Ensure that scripts are Unix-friendly and executable
RUN dos2unix /autograder/run_autograder /autograder/*.sh
RUN chmod +x /autograder/run_autograder /autograder/*.sh

RUN yum install -y \
    autofs \
    bison \
    boost \
    byacc \
    clang \
    cmake \
    dos2unix \ 
    gcc \
    gcc-toolset-10-gcc-c++ \
    gcc-toolset-11-gcc-c++ \
    gdb \
    git \
    glibc-devel \
    man-pages \ 
    nmap-ncat \
    python3 \
    tcpdump \
    tcsh \
    telnet \
    tmux \
    traceroute \
    tree \
    valgrind \ 
    wget \ 
    yum-utils

# Set the working directory
WORKDIR /home/student

# Run setup.sh
RUN /autograder/setup.sh