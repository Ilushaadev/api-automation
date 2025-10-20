pipeline {
    agent any

    environment {
        // Docker configuration
        DOCKER_IMAGE = "jenkins-demo-app"
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DOCKER_REGISTRY = "" // Set to your registry URL or leave empty for Docker Hub

        // Python configuration
        PYTHON_VERSION = "3.11"
    }

    stages {
        stage('Setup') {
            steps {
                echo 'Setting up environment...'
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                echo 'Running code quality checks...'
                sh '''
                    . .venv/bin/activate
                    flake8 app.py config.py --max-line-length=120 --extend-ignore=E203,W503 || true
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    . .venv/bin/activate
                    export API_KEY=test-api-key
                    export JWT_SECRET_KEY=test-jwt-secret
                    python -m pytest tests/ -v --cov=. --cov-report=xml --cov-report=html
                '''
            }
            post {
                always {
                    // Archive test results and coverage reports
                    junit(testResults: '**/test-results.xml', allowEmptyResults: true)
                    publishHTML(target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    def imageName = "${DOCKER_REGISTRY}${DOCKER_IMAGE}:${DOCKER_TAG}"
                    def latestImage = "${DOCKER_REGISTRY}${DOCKER_IMAGE}:latest"

                    sh """
                        docker build -t ${imageName} -t ${latestImage} .
                    """
                }
            }
        }

        stage('Security Scan') {
            steps {
                echo 'Running security scan...'
                script {
                    def imageName = "${DOCKER_REGISTRY}${DOCKER_IMAGE}:${DOCKER_TAG}"

                    // Run Trivy scan (if available)
                    sh """
                        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy:latest image --exit-code 0 --severity HIGH,CRITICAL \
                        ${imageName} || true
                    """
                }
            }
        }

        stage('Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                echo 'Pushing Docker image to registry...'
                script {
                    // Only push on main branch
                    def imageName = "${DOCKER_REGISTRY}${DOCKER_IMAGE}:${DOCKER_TAG}"
                    def latestImage = "${DOCKER_REGISTRY}${DOCKER_IMAGE}:latest"

                    sh """
                        docker push ${imageName}
                        docker push ${latestImage}
                    """
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying application...'
                script {
                    // Example deployment - adjust based on your platform
                    sh '''
                        # Stop and remove old container if exists
                        docker stop jenkins-demo-app || true
                        docker rm jenkins-demo-app || true

                        # Run new container
                        docker run -d \
                            --name jenkins-demo-app \
                            -p 5001:5001 \
                            --env-file .env \
                            --restart unless-stopped \
                            ${DOCKER_IMAGE}:${DOCKER_TAG}
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh '''
                # Clean up virtual environment
                rm -rf .venv

                # Clean up old Docker images (keep last 5 builds)
                docker images ${DOCKER_IMAGE} --format "{{.Tag}}" | \
                grep -E '^[0-9]+$' | sort -nr | tail -n +6 | \
                xargs -I {} docker rmi ${DOCKER_IMAGE}:{} || true
            '''
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
