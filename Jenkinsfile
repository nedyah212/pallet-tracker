pipeline {
    agent any
    environment {
        NEXUS_REGISTRY = 'localhost:8082'
        NEXUS_REGISTRY_IP = '10.0.0.224:8082'
        NEXUS_CREDENTIAL_ID = 'nexus-credentials'
        IMAGE_NAME = "${scm.getUserRemoteConfigs()[0].getUrl().tokenize('/').last().split('\\.')[0]}"
        STAGING_SERVER = '10.0.0.225'
        PROD_SERVER = '10.0.0.226'
        CONTAINER_PORT = '5000'
        STAGING_SERVER_PORT = '80'
        PROD_SERVER_PORT = '8080'
    }

        stages {
            stage('Build Docker Image') {
                steps {
                    script {
                        echo "Building image: ${NEXUS_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}"
                        dockerImage = docker.build("${NEXUS_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}")
                        echo "✓ Image built successfully"
                    }
                }
            }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install -r requirements-dev.txt
                    python -m pytest tests/ --verbose --junit-xml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Push to Nexus') {
            steps {
                script {
                    echo "Logging into registry: ${NEXUS_REGISTRY}"
                    docker.withRegistry("http://${NEXUS_REGISTRY}", NEXUS_CREDENTIAL_ID) {
                        echo "Pushing ${BUILD_NUMBER} tag..."
                        dockerImage.push("${BUILD_NUMBER}")
                        echo "✓ Pushed build number tag"

                        echo "Pushing latest tag..."
                        dockerImage.push('latest')
                        echo "✓ Pushed latest tag"
                    }
                    echo "✓✓✓ All pushes completed successfully!"
                }
            }
        }

        stage('Verify in Nexus') {
            steps {
                script {
                    echo "Image should now be visible in Nexus at:"
                    echo "http://localhost:8081 → Browse → docker-private → ${IMAGE_NAME}"
                }
            }
        }

        stage('Deploy to Staging Server') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'staging-ssh-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    ),
                    usernamePassword(
                        credentialsId: 'nexus-credentials',
                        usernameVariable: 'NEXUS_CREDS_USR',
                        passwordVariable: 'NEXUS_CREDS_PSW'
                    )
                ]) {
                    script {
                        echo "Deploying to staging server..."
                        sh """
                            ssh -o StrictHostKeyChecking=no -i \$SSH_KEY \$SSH_USER@${STAGING_SERVER} \
                                "echo '\$NEXUS_CREDS_PSW' | docker login ${NEXUS_REGISTRY_IP} -u '\$NEXUS_CREDS_USR' --password-stdin && \
                                docker pull ${NEXUS_REGISTRY_IP}/${IMAGE_NAME}:${BUILD_NUMBER} && \
                                docker stop ${IMAGE_NAME} || true && \
                                docker rm ${IMAGE_NAME} || true && \
                                docker run -d --name ${IMAGE_NAME} -p ${STAGING_SERVER_PORT}:${CONTAINER_PORT} ${NEXUS_REGISTRY_IP}/${IMAGE_NAME}:${BUILD_NUMBER}"
                        """
                        echo "Container deployed on staging"
                    }
                }
            }
        }

        stage('Verify Staging Deployment') {
            steps {
                sh '''
                    # Wait for container to start
                    sleep 10

                    # Check if it's responding
                    curl -f http://10.0.0.225 || exit 1

                    echo "Staging deployment verified!"
                '''
            }
        }

        stage('Deploy to Production Server') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'prod-ssh-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    ),
                    usernamePassword(
                        credentialsId: 'nexus-credentials',
                        usernameVariable: 'NEXUS_CREDS_USR',
                        passwordVariable: 'NEXUS_CREDS_PSW'
                    )
                ]) {
                    script {
                        echo "Deploying to production server..."
                        sh """
                            ssh -o StrictHostKeyChecking=no -i \$SSH_KEY \$SSH_USER@${PROD_SERVER} \
                                "echo '\$NEXUS_CREDS_PSW' | docker login ${NEXUS_REGISTRY_IP} -u '\$NEXUS_CREDS_USR' --password-stdin && \
                                docker pull ${NEXUS_REGISTRY_IP}/${IMAGE_NAME}:${BUILD_NUMBER} && \
                                docker stop ${IMAGE_NAME} || true && \
                                docker rm ${IMAGE_NAME} || true && \
                                docker run -d --name ${IMAGE_NAME} -p ${PROD_SERVER_PORT}:${CONTAINER_PORT} ${NEXUS_REGISTRY_IP}/${IMAGE_NAME}:${BUILD_NUMBER}"
                        """
                        echo "Container deployed on production"
                    }
                }
            }
        }
        stage('Verify Production Deployment') {
            steps {
                sh '''
                    sleep 10
                    curl -f http://10.0.0.226:8080 || exit 1
                    echo "Production deployment verified!"
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Please check the logs."
        }
    }
}
