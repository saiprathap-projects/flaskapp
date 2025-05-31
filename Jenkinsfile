pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = '340752824368'
        ECR_REPO = 'flaskapp'
        KUBECONFIG = "${WORKSPACE}/config"
        
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }
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
        stage ('Terraform - Create ECR') {
            steps {
                script {
                    sh '''
                        cd terraform/ECR
                        export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                        export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                        export AWS_REGION=$AWS_REGION

                        terraform init
                        terraform plan
                        terraform apply -auto-approve

                       '''
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                    cd $WORKSPACE
                    docker-compose build
                    '''
                }
            }
        }
        stage('Tag & Push image to ECR') {
            steps {
                script {
                    def ecrUrl = "${env.AWS_ACCOUNT_ID}.dkr.ecr.${env.AWS_REGION}.amazonaws.com"
                    def services = ['flaskapp_flaskapp','flaskapp_nginx']                    
                    
                    for (service in services) {
                        def localImage = "${service}:latest"
                        def remoteImage = "${ecrUrl}/${env.ECR_REPO}:latest"

                        sh """
                        docker tag ${localImage} ${remoteImage}
                        docker push ${remoteImage}
                        """
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'kubeconfig-prod', variable: 'KUBECONFIG')]) {
                        sh '''
                        (
                            trap 'echo "Pipeline interrupted"; exit 1' SIGINT SIGTERM
                            kubectl apply -f k8s/flask-deployment.yaml --validate=false
                            kubectl apply -f k8s/nginx-service.yaml --validate=false
                            kubectl rollout status deployment flask-nginx-deployment
                        )
                        '''                 
                    }
              }
          }  
      }
   }     
}
