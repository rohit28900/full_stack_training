pipeline {

    agent any

    environment {
        IMAGE_NAME         = 'academic-service'
        IMAGE_TAG          = "${BUILD_NUMBER}"
        REGISTRY           = 'rohit28900'
        RAILWAY_SERVICE_ID = '52f79f2f-6cc8-4ddf-bc42-cfeea6208057'
        RAILWAY_ENV_ID     = '21f62e98-a1db-4397-8e2d-7a93f8a50f46'
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
                        curl -f -X POST \
                            -H "Authorization: Bearer $RAILWAY_TOKEN" \
                            -H "Content-Type: application/json" \
                            -d "{\\"query\\": \\"mutation { serviceInstanceRedeploy(environmentId: \\\\\\"${RAILWAY_ENV_ID}\\\\\\", serviceId: \\\\\\"${RAILWAY_SERVICE_ID}\\\\\\") }\\"}" \
                            https://backboard.railway.com/graphql/v2
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
            echo "✅ Deployed to Railway via API — Build #${BUILD_NUMBER}"
        }
        failure {
            echo '❌ Pipeline Failed — check logs above'
        }
    }
}