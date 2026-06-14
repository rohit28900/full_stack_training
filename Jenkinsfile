pipeline {

    agent any

    environment {
        IMAGE_NAME         = 'academic-service'
        IMAGE_TAG          = "${BUILD_NUMBER}"
        REGISTRY           = 'rohit28900'
        RAILWAY_SERVICE_ID = '52f79f2f-6cc8-4ddf-bc42-cfeea6208057'
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

        stage('Build and Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    dir('acadmic_service') {
                        sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                            docker buildx create --use --name multiarch || true

                            docker buildx build \
                                --platform linux/amd64 \
                                -t ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} \
                                -t ${REGISTRY}/${IMAGE_NAME}:latest \
                                --push \
                                .
                        '''
                    }
                }
            }
        }

        stage('Deploy to Railway') {
            steps {
                withCredentials([string(
                    credentialsId: 'railway-token',
                    variable: 'RAILWAY_TOKEN'
                )]) {
                    sh '''
                        export PATH=$PATH:$HOME/.railway/bin

                        if ! command -v railway > /dev/null 2>&1; then
                            curl -fsSL https://railway.app/install.sh | bash
                        fi

                        export PATH=$PATH:$HOME/.railway/bin

                        railway up \
                            --service ${RAILWAY_SERVICE_ID} \
                            --detach
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
            echo "✅ Deployed to Railway — Build #${BUILD_NUMBER}"
        }
        failure {
            echo '❌ Pipeline Failed — check logs above'
        }
    }
}