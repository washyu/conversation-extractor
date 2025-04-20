pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            args '-v $HOME/.cache/pip:/root/.cache/pip'
        }
    }

    stages {
        stage('Setup') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install build twine wheel pytest pytest-html'
                sh 'pip install -e .[dev]'
                sh 'python -c "import nltk; nltk.download(\'punkt\'); nltk.download(\'stopwords\')"'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest --junitxml=test-results.xml --html=test-report.html'
            }
            post {
                always {
                    junit 'test-results.xml'
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'test-report.html',
                        reportName: 'Test Report'
                    ])
                }
            }
        }

        stage('Build') {
            steps {
                sh 'python -m build'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'dist/*', fingerprint: true
                }
            }
        }

        stage('Publish to Local Repository') {
            when {
                branch 'main'
            }
            steps {
                // This step would publish to your private PyPI repository
                // Replace the URL with your actual repository URL
                sh '''
                if [ -d "$JENKINS_HOME/pypi-repo" ]; then
                    twine upload --repository-url file://$JENKINS_HOME/pypi-repo dist/*
                else
                    echo "Local PyPI repository not found. Skipping publish step."
                fi
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
