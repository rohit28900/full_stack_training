pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test IAM Service') {
            steps {
                dir('iam_service') {
                    sh '''
                    python3 -m venv venv
                    . venv/bin/activate

                    pip install -r requirements.txt
                    pytest -v
                    '''
                }
            }
        }

        stage('Test Academic Service') {
            steps {
                dir('academic_service') {
                    sh '''
                    python3 -m venv venv
                    . venv/bin/activate

                    pip install -r requirements.txt
                    pytest -v
                    '''
                }
            }
        }

        stage('Build IAM Image') {
            steps {
                dir('iam_service') {
                    sh '''
                    docker build \
                    -t iam-service:${BUILD_NUMBER} .
                    '''
                }
            }
        }

        stage('Build Academic Image') {
            steps {
                dir('academic_service') {
                    sh '''
                    docker build \
                    -t academic-service:${BUILD_NUMBER} .
                    '''
                }
            }
        }
    }
}