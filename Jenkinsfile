pipeline {
    agent any

    environment {
        IMAGE_NAME = 'myflaskapp'
        IMAGE_TAG = 'latest'
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

        stage('Run Docker Container') {
            steps {
                script {
                    sh "docker-compose up -d"
                }
            }
        }
    }

}
