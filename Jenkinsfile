pipeline {
    agent any

    environment {
        IMAGE_NAME = 'myflaskapp'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('SCM checkout') {
            steps {
                git credentialsId: 'a500b7e5-e244-466b-8d05-074c05b22cae', url: 'https://github.com/saiprathap-projects/flaskapp.git'
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
