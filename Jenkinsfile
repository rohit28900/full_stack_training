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
                    pip3 install -r requirements.txt
                    pytest -v
                    '''
                }
            }
        }

        stage('Test Academic Service') {
            steps {
                dir('acadmic_service') {
                    sh '''
                    pip3 install -r requirements.txt
                    pytest -v
                    '''
                }
            }
        }
    }
}