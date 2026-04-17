pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "federicocitarelli/sentiment-analysis-api"
    }

    stages {
        stage('Checkout') {
            steps {
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
                powershell """
                # Rimuove l'immagine locale se esiste già
                docker rmi ${env.DOCKER_IMAGE}:latest -f 2>\$null
                
                # Build dell'immagine
                docker build -t ${env.DOCKER_IMAGE}:latest .
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    powershell '''
                    Write-Host "Login to Docker Hub..."

                    $env:DOCKER_PASS | docker login -u $env:DOCKER_USER --password-stdin

                    if ($LASTEXITCODE -ne 0) {
                        Write-Error "Docker login failed"
                        exit 1
                    }

                    Write-Host "Pushing image..."
                    docker push federicocitarelli/sentiment-analysis-api:latest
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
                # Corretto env:DOCKER_IMAGE in env.DOCKER_IMAGE per coerenza
                docker run -d -p 8000:8000 --name sentiment-api ${env.DOCKER_IMAGE}:latest
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