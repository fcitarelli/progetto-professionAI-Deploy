pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "federicocitarelli/sentiment-analysis-api"
    }

    stages {
        stage('Checkout') {
            steps {
                // AGGIUNTO: credentialsId deve essere l'ID che hai dato alla credenziale su Jenkins
                git url: 'https://github.com/fcitarelli/progetto-professionAI-Deploy.git', 
                    branch: 'main', 
                    credentialsId: 'github-token-federico' 
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
                // Qui usiamo correttamente le credenziali di Docker Hub (che hai già salvato)
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    powershell '''
                    $env:DOCKER_PASS | docker login -u $env:DOCKER_USER --password-stdin
                    docker push ${env:DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                powershell """
                if (docker ps -a -q -f name=sentiment-api) {
                    docker stop sentiment-api
                    docker rm sentiment-api
                }
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