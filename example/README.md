This folder contains the files for various demonstrations including:

- [Running Locally](#running-locally)
  - [1. Clone the Git Repo](#1-clone-the-git-repo)
  - [2. Local Environment Setup](#2-local-environment-setup)
  - [3. Loading Data (TODO---Finish for Tomorrow)](#3-loading-data-todo---finish-for-tomorrow)
  - [4. Run the App](#4-run-the-app)
- [Video Demo](#video-demo)

[](#)

## Running Locally

[](#)

### 1\. Clone the Git Repo

[](https://github.com/yashmanne/an_analysis_of_nothing/tree/main/examples#1-clone-the-git-repo)

Run the following `git` command:

```shell
git clone https://github.com/apeled/TLDhubeR
```

[](#)

### 2\. Local Environment Setup

[](https://github.com/yashmanne/an_analysis_of_nothing/tree/main/examples#2-local-environment-setup)

Initialize our Conda environment `tldhuber` with the following command:

```shell
conda env create -f environment.yml
```

Once the Conda environment is created, it can be activated by:

```shell
conda activate tldhuber
```

And deactivated with the command:

```shell
conda deactivate
```

[](#)

### 3\. Loading Data (TODO---Finish for Tomorrow)

[](https://github.com/yashmanne/an_analysis_of_nothing/tree/main/examples#3-loading-data)

Follow the link here (link to come) and copy the contents into the tldhuber folder. 

[](#)

### 4\. Run the App

[](https://github.com/yashmanne/an_analysis_of_nothing/tree/main/examples#4-run-the-app)

A local application can be generated with the code:

```shell
conda activate nothing
streamlit run tldhuber/hello_huber.py
```

[](#)

## Video Demo

[]()

- See our **[Video Demo](put link here)** to watch tldhuber in action!