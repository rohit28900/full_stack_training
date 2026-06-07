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
                    rm -rf venv

                    python3 -m venv venv
                    . venv/bin/activate

                    pip install --upgrade pip
                    pip install -r requirements.txt

                    pytest -v
                    '''
                }
            }
        }

        stage('Test Academic Service') {
            steps {
                dir('acadmic_service') {
                    sh '''
                    rm -rf venv

                    python3 -m venv venv
                    . venv/bin/activate

                    pip install --upgrade pip
                    pip install -r requirements.txt

                    pytest -v
                    '''
                }
            }
        }

    }

    post {

        always {
            echo 'Pipeline Finished'
        }

        success {
            echo 'All tests passed successfully!'
        }

        failure {
            echo 'Pipeline Failed!'
        }
    }
}