pipeline {

    agent any

    environment {
        IMAGE_NAME = 'academic-service'
        IMAGE_TAG  = "${BUILD_NUMBER}"
        REGISTRY   = 'rohit28900'  
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
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

        stage('Build Docker Image') {
            steps {
                dir('acadmic_service') {
                    sh '''
                        docker build -t ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} \
                                   ${REGISTRY}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${REGISTRY}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Cleanup') {
            steps {
                sh '''
                    docker rmi ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} || true
                    docker rmi ${REGISTRY}/${IMAGE_NAME}:latest || true
                '''
            }
        }

    }

    post {
        always {
            echo 'Pipeline Finished'
        }
        success {
            echo "Build #${BUILD_NUMBER} pushed: ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo ' Pipeline Failed — check logs above'
        }
    }
}