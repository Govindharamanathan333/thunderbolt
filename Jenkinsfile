pipeline {
    agent {
        label 'worker1'
    }

    environment {
        FRONTEND_IMAGE = "thunderbolt_frontend"
        BACKEND_IMAGE = "thunderbolt_backend"
        DOCKER_REGISTRY = "10.10.30.22:8085"
        DOCKER_CREDENTIALS_ID = "nexus"
        SLACK_CHANNEL = 'jenkins'
        SLACK_CREDENTIALS_ID = 'slack_token_aug19'
        CODE_REPO_URL = "https://github.com/Govindharamanathan333/thunderbolt.git"
        CODE_REPO_BRANCH = "main"
        YAML_REPO_URL = "https://github.com/Govindharamanathan333/manifest.git"
        YAML_REPO_BRANCH = "main"
        GIT_USER_NAME = "Govindharamanathan333"
        GIT_EMAIL = "govindharamanathan@saptanglabs.com"
        SONAR_HOST_URL = "http://10.10.30.18:9000"
        SONAR_LOGIN = "sqp_ffd5d52d2c974df64d6e94da40470fa9728ff02e"
        PROJECT_KEY = "thunderbolt"
    }

    stages {
        stage('Clone Code Repository') {
            steps {
                git url: "${CODE_REPO_URL}", branch: "${CODE_REPO_BRANCH}"
                script {
                    def gitCommit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    slackSend(channel: SLACK_CHANNEL, tokenCredentialId: SLACK_CREDENTIALS_ID, message: "Code repository cloned. Commit: ${gitCommit}")
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dir('front_app') {
                        sh "sudo docker build -t ${FRONTEND_IMAGE}:v${env.BUILD_NUMBER} ."
                    }
                    slackSend(channel: SLACK_CHANNEL, tokenCredentialId: SLACK_CREDENTIALS_ID, message: "Frontend image build successful: ${FRONTEND_IMAGE}:v${env.BUILD_NUMBER}")
                }
            }
        }
        
        stage('Build Backend Docker Image') {
            steps {
                script {
                    def buildNumber = env.BUILD_NUMBER
                    dir('backend') {
                        sh "sudo docker build -t ${BACKEND_IMAGE}:v${buildNumber} ."
                    }
                    slackSend(channel: SLACK_CHANNEL, message: "Backend image build successful: ${BACKEND_IMAGE}:v${buildNumber}")
                }
            }
        }

        stage('SonarQube Code Analysis') {
            steps {
                script {
                    // Frontend SonarQube Analysis
                    sh """
                        sudo docker run --rm \
                          -e SONAR_HOST_URL="${SONAR_HOST_URL}" \
                          -e SONAR_LOGIN="${SONAR_LOGIN}" \
                          -v "\$WORKSPACE:/usr/src" \
                          sonarsource/sonar-scanner-cli \
                          sonar-scanner \
                          -Dsonar.projectKey=${PROJECT_KEY} \
                          -Dsonar.sources=front_app \
                          -Dsonar.exclusions=**/node_modules/**,**/dist/**,**/build/**,**/static/**,**/Dockerfile,**/README.md,**/svelte.config.js,**/tailwind.config.js,**/vite.config.js,**/postcss.config.js \
                          -Dsonar.projectBaseDir=/usr/src \
                          -Dsonar.login=${SONAR_LOGIN} \
                          -X
                    """
                    
                    // Backend SonarQube Analysis for Python Files
                    sh """
                        sudo docker run --rm \
                          -e SONAR_HOST_URL="${SONAR_HOST_URL}" \
                          -e SONAR_LOGIN="${SONAR_LOGIN}" \
                          -v "\$WORKSPACE:/usr/src" \
                          sonarsource/sonar-scanner-cli \
                          sonar-scanner \
                          -Dsonar.projectKey=${PROJECT_KEY} \
                          -Dsonar.sources=backend \
                          -Dsonar.inclusions=**/*.py \
                          -Dsonar.exclusions=backend/env/** \
                          -Dsonar.projectBaseDir=/usr/src \
                          -Dsonar.login=${SONAR_LOGIN} \
                          -X
                    """

                    slackSend(channel: SLACK_CHANNEL, tokenCredentialId: SLACK_CREDENTIALS_ID, message: "SonarQube analysis completed successfully for frontend and backend.")
                }
            }
        }

        stage('Tag and Push Docker Image to Nexus') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'NEXUS_USERNAME', passwordVariable: 'NEXUS_PASSWORD')]) {
                    script {
                        def fullImageName = "${DOCKER_REGISTRY}/${FRONTEND_IMAGE}:v${env.BUILD_NUMBER}"

                        // Tag the Docker image with the build number
                        sh "sudo docker tag ${FRONTEND_IMAGE}:v${env.BUILD_NUMBER} ${fullImageName}"

                        // Log in to the Docker registry
                        sh "sudo docker login -u $NEXUS_USERNAME -p $NEXUS_PASSWORD ${DOCKER_REGISTRY}"

                        // Push the tagged Docker image to Nexus
                        sh "sudo docker push ${fullImageName}"

                        slackSend(channel: SLACK_CHANNEL, tokenCredentialId: SLACK_CREDENTIALS_ID, message: "Docker image pushed successfully: ${fullImageName}")
                    }
                }
            }
        }
        stage('Tag and Push Backend Docker Image to Nexus') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'NEXUS_USERNAME', passwordVariable: 'NEXUS_PASSWORD')]) {
                    script {
                        def fullImageName = "${DOCKER_REGISTRY}/${BACKEND_IMAGE}:v${env.BUILD_NUMBER}"

                        // Tag the Docker image with the build number
                        sh "sudo docker tag ${BACKEND_IMAGE}:v${env.BUILD_NUMBER} ${fullImageName}"

                        // Log in to the Docker registry
                        sh "sudo docker login -u $NEXUS_USERNAME -p $NEXUS_PASSWORD ${DOCKER_REGISTRY}"

                        // Push the tagged Docker image to Nexus
                        sh "sudo docker push ${fullImageName}"

                        slackSend(channel: SLACK_CHANNEL, tokenCredentialId: SLACK_CREDENTIALS_ID, message: "Docker image pushed successfully: ${fullImageName}")
                    }
                }
            }
        }

        stage('Clone YAML Repository') {
            steps {
                git url: "${YAML_REPO_URL}", branch: "${YAML_REPO_BRANCH}"
            }
        }

        stage('Update Deployment File') {
            steps {
                withCredentials([string(credentialsId: 'git', variable: 'GITHUB_TOKEN')]) {
                    script {
                        def fullImageName_front = "${DOCKER_REGISTRY}/${FRONTEND_IMAGE}:v${env.BUILD_NUMBER}"
                        def fullImageName_back = "${DOCKER_REGISTRY}/${BACKEND_IMAGE}:v${env.BUILD_NUMBER}"
                        sh """
                            git config user.email "${GIT_EMAIL}"
                            git config user.name "${GIT_USER_NAME}"
                            
                            # Replace any existing image tag with the new image tag in the deployment file
                            sed -i 's|image:.*|image: ${fullImageName_front}|g' manifest/deployment.yaml
                            sed -i 's|image:.*|image: ${fullImageName_back}|g' backend/deploy.yaml
                            git add manifest/deployment.yaml
                            git add backend/deploy.yaml
                            git commit -m "Update deployment image to version v${env.BUILD_NUMBER}"
                            git push https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/manifest.git HEAD:${YAML_REPO_BRANCH}
                        """

                        slackSend(channel: SLACK_CHANNEL, tokenCredentialId: SLACK_CREDENTIALS_ID, message: "Updated Kubernetes deployment file with image: ${fullImageName}")
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
            script {
                def serverStatus = sh(script: 'curl -Is http://localhost:8000 | head -n 1', returnStdout: true).trim()
                slackSend(channel: SLACK_CHANNEL, tokenCredentialId: SLACK_CREDENTIALS_ID, message: "Pipeline finished. Server status: ${serverStatus}")
            }
        }
        success {
            slackSend(channel: SLACK_CHANNEL, tokenCredentialId: SLACK_CREDENTIALS_ID, message: "Deployment successful.")
        }
        failure {
            slackSend(channel: SLACK_CHANNEL, tokenCredentialId: SLACK_CREDENTIALS_ID, message: "Deployment failed.")
        }
    }
}
