# Setting Up a Local PyPI Repository

This guide explains how to set up a local PyPI repository to host your packages.

## Using pypiserver

### 1. Install pypiserver

```bash
pip install pypiserver passlib
```

### 2. Create a directory for your packages

```bash
mkdir -p ~/pypi-repo
```

### 3. Create a password file (optional, for secure uploads)

```bash
htpasswd -sc ~/.pypipasswd your_username
```

### 4. Start the server

```bash
pypi-server -p 8080 -a .pypipasswd ~/pypi-repo
```

### 5. Configure pip to use your local repository

Create or edit `~/.pip/pip.conf` (Linux/Mac) or `%APPDATA%\pip\pip.ini` (Windows):

```ini
[global]
index-url = http://localhost:8080/simple
trusted-host = localhost
```

### 6. Configure twine for uploads

Create or edit `~/.pypirc`:

```ini
[distutils]
index-servers =
    local

[local]
repository = http://localhost:8080
username = your_username
password = your_password
```

## Using Jenkins to Host a PyPI Repository

### 1. Create a directory in Jenkins home

In your Jenkins server, create a directory for the PyPI repository:

```bash
mkdir -p $JENKINS_HOME/pypi-repo
```

### 2. Install pypiserver in Jenkins

```bash
pip install pypiserver
```

### 3. Create a Jenkins job to run the PyPI server

Create a new Jenkins freestyle job with the following shell command:

```bash
pypi-server -p 8081 $JENKINS_HOME/pypi-repo
```

### 4. Configure your project to publish to this repository

In your Jenkinsfile:

```groovy
stage('Publish to Local Repository') {
    steps {
        sh 'twine upload --repository-url http://localhost:8081 dist/*'
    }
}
```

## Using the Package in Other Projects

### 1. Install from your local PyPI repository

```bash
pip install --index-url http://localhost:8080/simple conversation-extractor
```

### 2. Or add to requirements.txt

```
--index-url http://localhost:8080/simple
conversation-extractor==0.1.0
```

### 3. Or install directly from the artifact

If you've downloaded the wheel file from Jenkins:

```bash
pip install conversation_extractor-0.1.0-py3-none-any.whl
```
