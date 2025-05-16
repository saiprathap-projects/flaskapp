pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'flaskapp'
        IMAGE_TAG = 'latest'
        ECR_URI = "340752824368.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/saiprathap-projects/flaskapp.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker-compose build"
                }
            }
        }
        stage('Login to ECR') {
            steps {
                script {
                    sh """
                    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI
                    """
                }
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    sh """
                    docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_URI}:${IMAGE_TAG}
                    docker push ${ECR_URI}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh "docker-compose up -d"
                }
            }
        }
    }

}
