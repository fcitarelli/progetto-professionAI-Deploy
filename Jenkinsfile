pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "federicocitarelli/sentiment-analysis-api"
    }

    stages {

        stage('Checkout') {
            steps {
                git url: 'https://github.com/FedericoCitarelli/progetto-professionAI-Deploy.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                powershell 'pip install -r requirements.txt'
            }
        }

        stage('Tests') {
            steps {
                powershell 'python -m pytest tests -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                powershell "docker build -t ${env.DOCKER_IMAGE}:latest ."
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    powershell '''
                    echo "$env:DOCKER_PASS" | docker login -u "$env:DOCKER_USER" --password-stdin
                    docker push ${env:DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                powershell """
                docker stop sentiment-api 2>$null
                docker rm sentiment-api 2>$null
                docker run -d -p 8000:8000 --name sentiment-api ${env:DOCKER_IMAGE}:latest
                """
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline FAILED! Check the logs for details.'
        }
        always {
            powershell 'docker logout'
            cleanWs()
        }
    }
}
