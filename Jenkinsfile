pipeline {

    agent any

    environment {
        // ── Application ──────────────────────────────────────────
        APP_NAME           = 'academic-service'
        APP_VERSION        = "1.0.${BUILD_NUMBER}"

        // ── Docker ───────────────────────────────────────────────
        REGISTRY           = 'rohit28900'
        IMAGE_NAME         = 'academic-service'
        IMAGE_TAG          = "${BUILD_NUMBER}"
        FULL_IMAGE         = "${REGISTRY}/${IMAGE_NAME}"

        // ── Railway ──────────────────────────────────────────────
        RAILWAY_SERVICE_ID = '52f79f2f-6cc8-4ddf-bc42-cfeea6208057'
        RAILWAY_ENV_ID     = '21f62e98-a1db-4397-8e2d-7a93f8a50f46'

        // ── Notifications ─────────────────────────────────────────
        TEAM_EMAIL         = 'team@yourcompany.com'  // 🔧 Replace
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        timestamps()
    }

    stages {

        // ── Stage 1: Checkout ─────────────────────────────────────
        stage('Checkout') {
            steps {
                echo "📥 Checking out branch: ${GIT_BRANCH}"
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
                echo "📝 Commit: ${GIT_COMMIT_MSG}"
                echo "👤 Author: ${GIT_AUTHOR}"
            }
        }

        // ── Stage 2: Code Quality ─────────────────────────────────
        stage('Code Quality') {
            steps {
                dir('acadmic_service') {
                    sh '''
                        rm -rf venv
                        python3 -m venv venv
                        . venv/bin/activate

                        pip install --upgrade pip --quiet
                        pip install -r requirements.txt --quiet
                        pip install flake8 --quiet

                        echo "────────────────────────────────"
                        echo " Running Linter (flake8)"
                        echo "────────────────────────────────"
                        flake8 . --max-line-length=120 --exclude=venv || true
                    '''
                }
            }
        }

        // ── Stage 3: Test ─────────────────────────────────────────
        stage('Test') {
            steps {
                dir('acadmic_service') {
                    sh '''
                        . venv/bin/activate

                        pip install pytest-html --quiet

                        mkdir -p reports

                        echo "────────────────────────────────"
                        echo " Running Tests (pytest)"
                        echo "────────────────────────────────"

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
                    junit allowEmptyResults: true,
                          testResults: 'acadmic_service/reports/junit.xml'

                    publishHTML(target: [
                        allowMissing         : false,
                        alwaysLinkToLastBuild: true,
                        keepAll              : true,
                        reportDir            : 'acadmic_service/reports',
                        reportFiles          : 'test-report.html',
                        reportName           : 'Pytest Report'
                    ])

                    script {
                        def summary = junit testResults: 'acadmic_service/reports/junit.xml',
                                            allowEmptyResults: true
                        env.TEST_TOTAL   = summary.totalCount
                        env.TEST_PASSED  = summary.passCount
                        env.TEST_FAILED  = summary.failCount
                        env.TEST_SKIPPED = summary.skipCount
                    }
                }
                failure {
                    emailext(
                        to: "${TEAM_EMAIL}",
                        subject: "❌ [${APP_NAME}] Build #${BUILD_NUMBER} — Tests Failed",
                        mimeType: 'text/html',
                        body: """
                        <html>
                        <body style="font-family: Arial, sans-serif; padding: 20px;">

                            <h2 style="color: #e74c3c;">❌ Tests Failed — ${APP_NAME}</h2>
                            <hr/>

                            <h3>🧪 Test Results</h3>
                            <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse; width:400px;">
                                <tr style="background:#f2f2f2;">
                                    <th>Total</th>
                                    <th style="color:green;">Passed</th>
                                    <th style="color:red;">Failed</th>
                                    <th style="color:orange;">Skipped</th>
                                </tr>
                                <tr align="center">
                                    <td>${TEST_TOTAL}</td>
                                    <td style="color:green;">${TEST_PASSED}</td>
                                    <td style="color:red;">${TEST_FAILED}</td>
                                    <td style="color:orange;">${TEST_SKIPPED}</td>
                                </tr>
                            </table>

                            <h3>📋 Build Info</h3>
                            <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse; width:400px;">
                                <tr><td><b>App</b></td><td>${APP_NAME}</td></tr>
                                <tr><td><b>Build</b></td><td>#${BUILD_NUMBER}</td></tr>
                                <tr><td><b>Branch</b></td><td>${GIT_BRANCH}</td></tr>
                                <tr><td><b>Author</b></td><td>${GIT_AUTHOR}</td></tr>
                                <tr><td><b>Commit</b></td><td>${GIT_COMMIT_MSG}</td></tr>
                            </table>

                            <br/>
                            <a href="${BUILD_URL}console"
                               style="background:#e74c3c;color:white;padding:10px 20px;
                                      text-decoration:none;border-radius:5px;">
                                🔍 View Logs
                            </a>
                            &nbsp;
                            <a href="${BUILD_URL}Pytest_20Report"
                               style="background:#8e44ad;color:white;padding:10px 20px;
                                      text-decoration:none;border-radius:5px;">
                                📊 Pytest Report
                            </a>

                            <br/><br/>
                            <p style="color:grey;font-size:12px;">Jenkins CI — ${APP_NAME} Pipeline</p>
                        </body>
                        </html>
                        """,
                        attachmentsPattern: 'acadmic_service/reports/test-report.html'
                    )
                }
            }
        }

        // ── Stage 4: Build & Push ─────────────────────────────────
        stage('Build & Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    dir('acadmic_service') {
                        sh '''
                            echo "────────────────────────────────"
                            echo " Building Docker Image"
                            echo " ${FULL_IMAGE}:${IMAGE_TAG}"
                            echo "────────────────────────────────"

                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                            docker buildx create --use --name multiarch || true

                            docker buildx build \
                                --platform linux/amd64 \
                                --build-arg APP_VERSION=${APP_VERSION} \
                                --build-arg BUILD_NUMBER=${BUILD_NUMBER} \
                                -t ${FULL_IMAGE}:${IMAGE_TAG} \
                                -t ${FULL_IMAGE}:latest \
                                --push \
                                .

                            echo "✅ Image pushed: ${FULL_IMAGE}:${IMAGE_TAG}"
                            echo "✅ Image pushed: ${FULL_IMAGE}:latest"
                        '''
                    }
                }
            }
        }

        // ── Stage 5: Deploy to Railway ────────────────────────────
        stage('Deploy to Railway') {
            steps {
                withCredentials([string(
                    credentialsId: 'railway-token',
                    variable: 'RAILWAY_TOKEN'
                )]) {
                    sh '''
                        echo "────────────────────────────────"
                        echo " Deploying to Railway"
                        echo " Service: ${RAILWAY_SERVICE_ID}"
                        echo "────────────────────────────────"

                        RESPONSE=$(curl -s -X POST \
                            -H "Authorization: Bearer $RAILWAY_TOKEN" \
                            -H "Content-Type: application/json" \
                            -d "{\\"query\\": \\"mutation { serviceInstanceRedeploy(environmentId: \\\\\\"${RAILWAY_ENV_ID}\\\\\\", serviceId: \\\\\\"${RAILWAY_SERVICE_ID}\\\\\\") }\\"}" \
                            https://backboard.railway.com/graphql/v2)

                        echo "Railway Response: $RESPONSE"

                        if echo "$RESPONSE" | grep -q "errors"; then
                            echo "❌ Railway deployment failed"
                            exit 1
                        fi

                        echo "✅ Deployment triggered successfully"
                    '''
                }
            }
        }

        // ── Stage 6: Cleanup ──────────────────────────────────────
        stage('Cleanup') {
            steps {
                sh '''
                    echo "────────────────────────────────"
                    echo " Cleaning up"
                    echo "────────────────────────────────"
                    docker rmi ${FULL_IMAGE}:${IMAGE_TAG} || true
                    docker rmi ${FULL_IMAGE}:latest || true
                    docker buildx rm multiarch || true
                    echo "✅ Cleanup done"
                '''
            }
        }
    }

    // ── Post Actions ──────────────────────────────────────────────
    post {

        success {
            emailext(
                to: "${TEAM_EMAIL}",
                subject: "✅ [${APP_NAME}] Build #${BUILD_NUMBER} — Deployed Successfully",
                mimeType: 'text/html',
                body: """
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">

                    <h2 style="color: #27ae60;">✅ Deployment Successful — ${APP_NAME}</h2>
                    <hr/>

                    <h3>🧪 Test Results</h3>
                    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse; width:400px;">
                        <tr style="background:#f2f2f2;">
                            <th>Total</th>
                            <th style="color:green;">Passed</th>
                            <th style="color:red;">Failed</th>
                            <th style="color:orange;">Skipped</th>
                        </tr>
                        <tr align="center">
                            <td>${TEST_TOTAL}</td>
                            <td style="color:green;">${TEST_PASSED}</td>
                            <td style="color:red;">${TEST_FAILED}</td>
                            <td style="color:orange;">${TEST_SKIPPED}</td>
                        </tr>
                    </table>

                    <h3>🐳 Docker Image</h3>
                    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse; width:400px;">
                        <tr><td><b>Image</b></td><td>${FULL_IMAGE}:${IMAGE_TAG}</td></tr>
                        <tr><td><b>Latest</b></td><td>${FULL_IMAGE}:latest</td></tr>
                    </table>

                    <h3>📋 Build Info</h3>
                    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse; width:400px;">
                        <tr><td><b>App</b></td><td>${APP_NAME} v${APP_VERSION}</td></tr>
                        <tr><td><b>Build</b></td><td>#${BUILD_NUMBER}</td></tr>
                        <tr><td><b>Branch</b></td><td>${GIT_BRANCH}</td></tr>
                        <tr><td><b>Author</b></td><td>${GIT_AUTHOR}</td></tr>
                        <tr><td><b>Commit</b></td><td>${GIT_COMMIT_MSG}</td></tr>
                    </table>

                    <br/>
                    <a href="${BUILD_URL}Pytest_20Report"
                       style="background:#8e44ad;color:white;padding:10px 20px;
                              text-decoration:none;border-radius:5px;margin-right:10px;">
                        📊 Pytest Report
                    </a>
                    &nbsp;
                    <a href="${BUILD_URL}"
                       style="background:#2980b9;color:white;padding:10px 20px;
                              text-decoration:none;border-radius:5px;">
                        🔨 View Build
                    </a>

                    <br/><br/>
                    <p style="color:grey;font-size:12px;">Jenkins CI — ${APP_NAME} Pipeline</p>
                </body>
                </html>
                """,
                attachmentsPattern: 'acadmic_service/reports/test-report.html'
            )
        }

        failure {
            emailext(
                to: "${TEAM_EMAIL}",
                subject: "❌ [${APP_NAME}] Build #${BUILD_NUMBER} — Pipeline Failed",
                mimeType: 'text/html',
                body: """
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">

                    <h2 style="color: #e74c3c;">❌ Pipeline Failed — ${APP_NAME}</h2>
                    <hr/>

                    <h3>📋 Build Info</h3>
                    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse; width:400px;">
                        <tr><td><b>App</b></td><td>${APP_NAME}</td></tr>
                        <tr><td><b>Build</b></td><td>#${BUILD_NUMBER}</td></tr>
                        <tr><td><b>Branch</b></td><td>${GIT_BRANCH}</td></tr>
                        <tr><td><b>Author</b></td><td>${GIT_AUTHOR}</td></tr>
                        <tr><td><b>Commit</b></td><td>${GIT_COMMIT_MSG}</td></tr>
                    </table>

                    <br/>
                    <a href="${BUILD_URL}console"
                       style="background:#e74c3c;color:white;padding:10px 20px;
                              text-decoration:none;border-radius:5px;">
                        🔍 View Logs
                    </a>

                    <br/><br/>
                    <p style="color:grey;font-size:12px;">Jenkins CI — ${APP_NAME} Pipeline</p>
                </body>
                </html>
                """
            )
        }

        always {
            echo '🏁 Pipeline Finished'
            cleanWs()
        }
    }
}