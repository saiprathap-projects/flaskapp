pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = '340752824368'
        ECR_REPO = 'flaskapp'
        IMAGE_TAG = 'latest'
        
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/saiprathap-projects/flaskapp.git'
            }
        }
        stage('Login to ECR') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-creds', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) 
                {
                    sh '''
                        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                        aws configure set region $AWS_REGION
                        
                        aws ecr get-login-password --region $AWS_REGION | \
                        docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                    '''
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker-compose build"
                }
            }
        }
        stage('Tag & Push image to ECR') {
            steps {
                script {
                    def ecrUrl = "${env.AWS_ACCOUNT_ID}.dkr.ecr.${env.AWS_REGION}.amazonaws.com"
                    def services = ['flaskapp', 'nginx']
                    def imageTag = "${env.IMAGE_TAG}"
                    
                    for (service in services) {
                        def localImage = "${service}:${imageTag}"
                        def remoteImage = "${ecrUrl}/${service}:${imageTag}"

                        sh """
                        docker tag ${localImage} ${remoteImage}
                        docker push ${remoteImage}
                        """
                    }
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
