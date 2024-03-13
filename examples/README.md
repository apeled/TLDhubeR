This folder contains setup information and usage examples for our application. After following the steps below, you will be able to run our app!
- [Running our App Locally (Hosting to Come)](#running-our-app-locally-hosting-to-come)
  - [1. Clone the Git Repo](#1-clone-the-git-repo)
  - [2. Local Environment Setup](#2-local-environment-setup)
  - [3. Loading Data](#3-loading-data)
  - [4. Obtain an OpenAI API Key](#4-obtain-an-openai-api-key)
  - [5. Run the App](#5-run-the-app)
- [Video Demo](#video-demo)

[](#)

## Running our App Locally (Hosting to Come)

The following steps walk you through how to download, setup, and then run TLDHubeR on a localhost. It will require a command line interface with `conda` installed. For now, the application can only be run locally, but a version accessible on `streamlit cloud` is soon to come!

[](#)

### 1\. Clone the Git Repo

[](#)

First, to obtain a local copy of our repository, run the following `git` command:

```shell
git clone https://github.com/apeled/TLDhubeR
```

[](#)

### 2\. Local Environment Setup

[](#)

Next, create our `conda` environment `tldhuber` as specified in the file `environment.yml`:

```shell
conda env create -f environment.yml
```

Once the Conda environment is created, it can be activated and deactivated with the following commands:

```shell
conda activate tldhuber
conda deactivate
```

Activate the `tldhuber` environment and proceed!

[](#)

### 3\. Loading Data

The reason we have not yet hosted our application is that our data source is too large for both version control and streamlit cloud. We have a plan to fix this using Google Cloud Storage and a Pinecone Vector Store, but for now you will have to download and "install" the data separately. The folder is about 300MB in size, and can be obtained at the following link: 

[Download data folder here](https://drive.google.com/drive/folders/1-DpJ9uRG-6wK9yiYZPyIj181-QSbK0_l?usp=sharing)

In order to run our application, you will need to copy the data folder and paste it into the top level of the TLDHubeR project. Once you have done this (`data/` should be at the same level as `tldhuber/`), proceed!

[](#)

### 4\. Obtain an OpenAI API Key

Our application makes use of the OpenAI API to generate text responses to your queries. Even though it costs only a few fractions of a cent per API call, we do not want to publicly share keys that are attached to our credit cards. For hosting, we do plan to include a default API key with a strict rate limit, so users without their own key may try out our app. For now though, an API key of your own is required. 

For the grader of this project, we've provided you with temporary access to an API key, for testing. For usage, see [our site navigation example](/examples/site_navigation.md). Essentially, input the API key into the sidebar, and you are good to go!

[](#)

### 5\. Run the App

[](#)

Once you have obtained the data and an OpenAI API key, the following command will kick off a local instance of our application. 

```shell
streamlit run tldhuber/hello_huber.py
```

For further usage information and more examples, [check out the rest of the examples](examples/site_navigation.md).

[](#)

## Video Demo

[]()

- Seeing is believing, so check out our **[Video Demo](https://drive.google.com/file/d/1fiSpdIgGcz334ju89eA-xbq1F2fx2haV/view?usp=sharing)** to watch TLDHubeR in action!