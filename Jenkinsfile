pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "federicocitarelli/sentiment-analysis-api"
        DOCKER_CONFIG = "C:\\ProgramData\\jenkins\\.docker"
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
                    $ErrorActionPreference = "Stop"

                    Write-Host "USER=[$env:DOCKER_USER]"
                    $token = $env:DOCKER_PASS.Trim()
                    Write-Host "TOKEN_LENGTH=$($token.Length)"

                    docker logout 2>$null

                    docker login -u $env:DOCKER_USER -p $token
                    if ($LASTEXITCODE -ne 0) {
                        throw "Docker login fallito. Verifica username e token in Jenkins credentials."
                    }

                    docker push federicocitarelli/sentiment-analysis-api:latest
                    if ($LASTEXITCODE -ne 0) {
                        throw "Docker push fallito."
                    }
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