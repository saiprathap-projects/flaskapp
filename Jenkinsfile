pipeline {
    agent any

    environment {
        IMAGE_NAME = 'myflaskapp'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('SCM checkout') {
            steps {
                git 'https://github.com/your-username/your-flask-repo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker-compose build -t $IMAGE_NAME:$IMAGE_TAG ."
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh "docker-compose up --name flask_container $IMAGE_NAME:$IMAGE_TAG"
                }
            }
        }
    }

}
