pipeline {
    agent any

    environment {
        SLACK_CHANNEL = 'jenkins' // Replace with your Slack channel
        SLACK_CREDENTIALS_ID = '8dgg3XNduLJGAkDODdeuZMQN' // The ID of the Jenkins credentials storing the token
        GIT_REPO_URL = 'https://github.com/jawahar1098/thunderbolt.git'
    }

    stages {
        stage('Clone repository') {
            steps {
                git GIT_REPO_URL
                script {
                    def gitCommit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    slackSend(channel: SLACK_CHANNEL, message: "Git repository cloned. Commit: ${gitCommit}")
                }
            }
        }

        stage('Backend Deployment on Slave') {
            agent {
                label 'slavenode1' // Replace with your slave node label
            }
            steps {
                dir('backend') {
                    script {
                        def dockerInstalled = sh(script: 'which docker', returnStatus: true)
                        if (dockerInstalled != 0) {
                            sh 'sudo apt-get update && sudo apt-get install -y docker.io'
                        }
                        
                        def networkExists = sh(script: 'sudo docker network ls --filter name=maze --format "{{.Name}}"', returnStdout: true).trim()
                        if (!networkExists) {
                            sh 'sudo docker network create maze'
                        }

                        def mongoImageExists = sh(script: 'sudo docker images -q mongo', returnStdout: true).trim()
                        if (!mongoImageExists) {
                            sh 'sudo docker pull mongo'
                        }

                        def mongoContainerExists = sh(script: 'sudo docker ps -a --filter name=mymongo --format "{{.Names}}"', returnStdout: true).trim()
                        if (!mongoContainerExists) {
                            sh 'sudo docker run -d --name mymongo --network maze -p 27017:27017 mongo'
                        }
                    }

                    sh '''
                        sudo docker build -t mazebackend .
                        sudo docker run -d -p 5006:5006 --name mazeback --network maze mazebackend 
                    '''

                    script {
                        try {
                            sh 'sudo docker ps'
                            slackSend(channel: SLACK_CHANNEL, message: "Backend deployment successful")
                        } catch (Exception e) {
                            slackSend(channel: SLACK_CHANNEL, message: "Backend deployment failed: ${e}")
                            throw e
                        }
                    }
                }
            }
        }

        stage('Frontend Deployment on Slave') {
            agent {
                label 'slavenode1' // Replace with your slave node label
            }
            steps {
                dir('front_app') {
                    script {
                        sh 'sudo apt-get update'
                        sh 'sudo docker build -t mazefrontend .'
                    }

                    sh 'sudo docker run -d -p 3001:3001 --name mazefront --network maze mazefrontend'

                    script {
                        try {
                            sh 'sudo docker ps'
                            slackSend(channel: SLACK_CHANNEL, message: "Frontend deployment successful")
                        } catch (Exception e) {
                            slackSend(channel: SLACK_CHANNEL, message: "Frontend deployment failed: ${e}")
                            throw e
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                def serverStatus = sh(script: 'curl -Is http://localhost:8000 | head -n 1', returnStdout: true).trim()
                slackSend(channel: SLACK_CHANNEL, message: "Deployment finished. Server status: ${serverStatus}")
            }
        }
        success {
            slackSend(channel: SLACK_CHANNEL, message: "Deployment successful")
        }
        failure {
            slackSend(channel: SLACK_CHANNEL, message: "Deployment failed")
        }
    }
}
