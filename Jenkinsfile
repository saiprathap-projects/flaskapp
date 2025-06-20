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
            when {
                expression {
                   // This shell command checks for both repositories
                   def flaskExists = sh(script: "aws ecr describe-repositories --repository-names flaskapp --region $AWS_REGION", returnStatus: true) == 0
                   def nginxExists = sh(script: "aws ecr describe-repositories --repository-names flask-nginx --region $AWS_REGION", returnStatus: true) == 0

                   return !(flaskExists && nginxExists) // Run only if at least one repo is missing
                }
            }
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
                    docker compose version
                    docker compose build --no-cache
                    '''
                }
            }
        }
        stage('Tag & Push image to ECR') {
            steps {
                script {
                    def ecrUrl = "${env.AWS_ACCOUNT_ID}.dkr.ecr.${env.AWS_REGION}.amazonaws.com"
                    def commitId = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    def versionTag = "v${env.BUILD_NUMBER}-${commitId}"
                    def images = ['flaskapp':'flaskapp', 'flask-nginx':'flask-nginx']

                    images.each { localName, repoName ->
                        def localImage = "${localName}:latest"
                        def latestTag = "${ecrUrl}/${repoName}:latest"
                        def versionedTag = "${ecrUrl}/${repoName}:${versionTag}"

                        sh """
                        docker tag ${localImage} ${latestTag}
                        docker tag ${localImage} ${versionedTag}
                        docker push ${latestTag}
                        docker push ${versionedTag}
                        """
                    }

                    // Save version tag for later use (like updating deployment)
                    env.IMAGE_VERSION = versionTag
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    def ecrUrl = "${env.AWS_ACCOUNT_ID}.dkr.ecr.${env.AWS_REGION}.amazonaws.com"

                     withCredentials([file(credentialsId: 'kubeconfig-prod', variable: 'KUBECONFIG')]) {
                         sh """
                         # Apply the base deployment YAML (once or if needed for initial deploy)
                         kubectl apply -f k8s/flask-deployment.yaml --validate=false
                         kubectl apply -f k8s/nginx-service.yaml --validate=false

                         # Update container images dynamically using the Jenkins-generated version tag
                         kubectl set image deployment/flask-nginx-deployment \
                             flaskapp=${ecrUrl}/flaskapp:${IMAGE_VERSION} \
                             nginx=${ecrUrl}/flask-nginx:${IMAGE_VERSION}

                         # Wait for rollout to complete
                         kubectl rollout status deployment/flask-nginx-deployment
                         """
                     }   
                }     
            }
        }
    }
}
    
