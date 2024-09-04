pipeline {
    agent {
        label 'worker1'
    }

    environment {
        BACKEND_IMAGE = "thunderbolt_backend"
        FRONTEND_IMAGE = "thunderbolt_frontend"
        GIT_REPO = "https://github.com/Govindharamanathan333/thunderbolt.git"
        
        DOCKER_REGISTRY = "10.10.30.22:8085/thunderbolt_frontend/"
        DOCKER_CREDENTIALS_ID = "nexus"
        SLACK_CHANNEL = 'jenkins' // Replace with your Slack channel
        SLACK_CREDENTIALS_ID = 'slack_token_aug19' // Replace this with the correct ID
        SONAR_HOST_URL = "http://10.10.30.18:9000"
        SONAR_LOGIN = "sqp_ffd5d52d2c974df64d6e94da40470fa9728ff02e"
        PROJECT_KEY = "thunderbolt"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: GIT_REPO, branch: 'main'
                script {
                    def gitCommit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    slackSend(channel: SLACK_CHANNEL, tokenCredentialId: SLACK_CREDENTIALS_ID, message: "Git repository cloned. Commit: ${gitCommit}")
                }
            }
        }

        stage('Build Frontend Docker Image') {
            steps {
                script {
                    def buildNumber = env.BUILD_NUMBER
                    dir('front_app') {
                        sh "sudo docker build -t ${FRONTEND_IMAGE}:v${buildNumber} ."
                    }
                    slackSend(channel: SLACK_CHANNEL, tokenCredentialId: SLACK_CREDENTIALS_ID, message: "Frontend image build successful: ${FRONTEND_IMAGE}:v${buildNumber}")
                }
            }
        }

        stage('SonarQube Code Analysis') {
            steps {
                script {
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
                    slackSend(channel: SLACK_CHANNEL, tokenCredentialId: SLACK_CREDENTIALS_ID, message: "SonarQube analysis completed successfully.")
                }
            }
        }

        stage('Push Docker Image to Nexus') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'nexus', usernameVariable: 'NEXUS_USERNAME', passwordVariable: 'NEXUS_PASSWORD')]) {
                    script {
                        sh """
                          sudo docker login -u $NEXUS_USERNAME -p $NEXUS_PASSWORD ${DOCKER_REGISTRY}
                          sudo docker push ${DOCKER_REGISTRY}/${FRONTEND_IMAGE}:v${env.BUILD_NUMBER}
                        """
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
