pipeline {
    agent {
        label 'worker1'
    }

    environment {
        BACKEND_IMAGE = "thunderbolt_backend"
        FRONTEND_IMAGE = "thunderbolt_frontend"
        GIT_REPO = "https://github.com/Govindharamanathan333/thunderbolt.git"
        
        DOCKER_REGISTRY = "http://10.10.30.22:8084"
        DOCKER_CREDENTIALS_ID = "nexus"
        SLACK_CHANNEL = 'jenkins' // Replace with your Slack channel
        SLACK_CREDENTIALS_ID = '8dgg3XNduLJGAkDODdeuZMQN' // Slack token credentials
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
                    slackSend(channel: SLACK_CHANNEL, message: "Git repository cloned. Commit: ${gitCommit}")
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

        stage('Build Frontend Docker Image') {
            steps {
                script {
                    def buildNumber = env.BUILD_NUMBER
                    dir('front_app') {
                        sh "sudo docker build -t ${FRONTEND_IMAGE}:v${buildNumber} ."
                    }
                    slackSend(channel: SLACK_CHANNEL, message: "Frontend image build successful: ${FRONTEND_IMAGE}:v${buildNumber}")
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
                          -Dsonar.sources=backend,front_app \
                          -Dsonar.projectBaseDir=/usr/src \
                          -Dsonar.login=${SONAR_LOGIN} \
                          -X
                    """
                    slackSend(channel: SLACK_CHANNEL, message: "SonarQube analysis completed successfully.")
                }
            }
        }

        stage('Push Backend Image to Nexus') {
            steps {
                script {
                    docker.withRegistry(DOCKER_REGISTRY, DOCKER_CREDENTIALS_ID) {
                        docker.image("${BACKEND_IMAGE}:v${env.BUILD_NUMBER}").push("latest")
                        docker.image("${BACKEND_IMAGE}:v${env.BUILD_NUMBER}").push("${env.BUILD_NUMBER}")
                    }
                    slackSend(channel: SLACK_CHANNEL, message: "Backend image pushed to Nexus.")
                }
            }
        }

        stage('Push Frontend Image to Nexus') {
            steps {
                script {
                    docker.withRegistry(DOCKER_REGISTRY, DOCKER_CREDENTIALS_ID) {
                        docker.image("${FRONTEND_IMAGE}:v${env.BUILD_NUMBER}").push("latest")
                        docker.image("${FRONTEND_IMAGE}:v${env.BUILD_NUMBER}").push("${env.BUILD_NUMBER}")
                    }
                    slackSend(channel: SLACK_CHANNEL, message: "Frontend image pushed to Nexus.")
                }
            }
        }
    }

    post {
        always {
            cleanWs()
            script {
                def serverStatus = sh(script: 'curl -Is http://localhost:8000 | head -n 1', returnStdout: true).trim()
                slackSend(channel: SLACK_CHANNEL, message: "Pipeline finished. Server status: ${serverStatus}")
            }
        }
        success {
            slackSend(channel: SLACK_CHANNEL, message: "Deployment successful.")
        }
        failure {
            slackSend(channel: SLACK_CHANNEL, message: "Deployment failed.")
        }
    }
}
