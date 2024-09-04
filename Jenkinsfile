pipeline {
    agent {
        label 'worker1'
    }

    environment {
        FRONTEND_IMAGE = "thunderbolt_frontend"
        DOCKER_REGISTRY = "10.10.30.22:8085"
        DOCKER_CREDENTIALS_ID = "nexus"
        SLACK_CHANNEL = 'jenkins'
        SLACK_CREDENTIALS_ID = 'slack_token_aug19'
        GIT_REPO_NAME = "manifest"
        GIT_USER_NAME = "Govindharamanathan333"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: "https://github.com/Govindharamanathan333/thunderbolt.git", branch: 'main'
                script {
                    def gitCommit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    slackSend(channel: SLACK_CHANNEL, tokenCredentialId: SLACK_CREDENTIALS_ID, message: "Git repository cloned. Commit: ${gitCommit}")
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
    stage('Update Deployment File') {
        steps {
            withCredentials([string(credentialsId: 'git', variable: 'GITHUB_TOKEN')]) {
                sh '''
                    git config user.email "govindharamanathan@saptanglabs.com"
                    git config user.name "${GIT_USER_NAME}"
                    
                    # Replace any existing image tag with the new IMAGE_TAG
                    sed -i 's|image:.*|image: ${fullImageName}|g'
                    git add .
                    
                    git commit -m "Update deployment image to version ${IMAGE_TAG}"
                    git push https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${} HEAD:main
                '''
            }
        }
    }
}
