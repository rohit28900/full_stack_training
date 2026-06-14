pipeline {

    agent any

    environment {
        APP_NAME           = 'academic-service'
        APP_VERSION        = "1.0.${BUILD_NUMBER}"

        REGISTRY           = 'rohit28900'
        IMAGE_NAME         = 'academic-service'
        IMAGE_TAG          = "${BUILD_NUMBER}"
        FULL_IMAGE         = "${REGISTRY}/${IMAGE_NAME}"

        RAILWAY_SERVICE_ID = '52f79f2f-6cc8-4ddf-bc42-cfeea6208057'
        RAILWAY_ENV_ID     = '21f62e98-a1db-4397-8e2d-7a93f8a50f46'

        TEAM_EMAIL         = 'tyrect5@gmail.com'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm

                script {
                    env.GIT_COMMIT_MSG = sh(
                        script: 'git log -1 --pretty=%B',
                        returnStdout: true
                    ).trim()

                    env.GIT_AUTHOR = sh(
                        script: 'git log -1 --pretty=%an',
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Code Quality') {
            steps {
                dir('acadmic_service') {
                    sh '''
                        rm -rf venv
                        python3 -m venv venv

                        . venv/bin/activate

                        pip install --upgrade pip
                        pip install -r requirements.txt
                        pip install flake8

                        flake8 . \
                          --max-line-length=120 \
                          --exclude=venv || true
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                dir('acadmic_service') {
                    sh '''
                        . venv/bin/activate

                        pip install pytest pytest-html

                        mkdir -p reports

                        pytest -v \
                            --tb=short \
                            --junitxml=reports/junit.xml \
                            --html=reports/test-report.html \
                            --self-contained-html
                    '''
                }
            }

            post {
                always {

                    junit(
                        testResults: 'acadmic_service/reports/junit.xml',
                        allowEmptyResults: true
                    )

                    archiveArtifacts(
                        artifacts: 'acadmic_service/reports/**',
                        fingerprint: true,
                        allowEmptyArchive: true
                    )
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {

                    dir('acadmic_service') {

                        sh '''
                            echo "$DOCKER_PASS" | docker login \
                                -u "$DOCKER_USER" \
                                --password-stdin

                            docker build \
                                -t ${FULL_IMAGE}:${IMAGE_TAG} \
                                -t ${FULL_IMAGE}:latest \
                                .

                            docker push ${FULL_IMAGE}:${IMAGE_TAG}
                            docker push ${FULL_IMAGE}:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy Railway') {
            steps {

                withCredentials([
                    string(
                        credentialsId: 'railway-token',
                        variable: 'RAILWAY_TOKEN'
                    )
                ]) {

                    sh '''
                        RESPONSE=$(curl -s -X POST \
                        -H "Authorization: Bearer $RAILWAY_TOKEN" \
                        -H "Content-Type: application/json" \
                        -d "{\\"query\\": \\"mutation { serviceInstanceRedeploy(environmentId: \\\\\\"${RAILWAY_ENV_ID}\\\\\\", serviceId: \\\\\\"${RAILWAY_SERVICE_ID}\\\\\\") }\\"}" \
                        https://backboard.railway.com/graphql/v2)

                        echo "$RESPONSE"

                        if echo "$RESPONSE" | grep -q "errors"; then
                            exit 1
                        fi
                    '''
                }
            }
        }

        stage('Cleanup Docker') {
            steps {

                sh '''
                    docker rmi ${FULL_IMAGE}:${IMAGE_TAG} || true
                    docker rmi ${FULL_IMAGE}:latest || true
                '''
            }
        }
    }

    post {

        success {

            emailext(
                to: "${TEAM_EMAIL}",
                subject: "✅ ${APP_NAME} Build #${BUILD_NUMBER} Successful",
                mimeType: 'text/html',
                body: """
                    <h2>Deployment Successful</h2>

                    <p><b>Application:</b> ${APP_NAME}</p>
                    <p><b>Build:</b> #${BUILD_NUMBER}</p>
                    <p><b>Author:</b> ${GIT_AUTHOR}</p>

                    <p>
                        <a href="${BUILD_URL}">
                            View Build
                        </a>
                    </p>
                """,
                attachmentsPattern: 'acadmic_service/reports/*.html,acadmic_service/reports/*.xml'
            )
        }

        failure {

            emailext(
                to: "${TEAM_EMAIL}",
                subject: "❌ ${APP_NAME} Build #${BUILD_NUMBER} Failed",
                mimeType: 'text/html',
                body: """
                    <h2>Pipeline Failed</h2>

                    <p><b>Application:</b> ${APP_NAME}</p>
                    <p><b>Build:</b> #${BUILD_NUMBER}</p>

                    <p>
                        <a href="${BUILD_URL}console">
                            View Console Logs
                        </a>
                    </p>
                """,
                attachmentsPattern: 'acadmic_service/reports/*.html,acadmic_service/reports/*.xml'
            )
        }

        always {

            archiveArtifacts(
                artifacts: 'acadmic_service/reports/**',
                fingerprint: true,
                allowEmptyArchive: true
            )

            echo '🏁 Pipeline Finished'

            cleanWs()
        }
    }
}