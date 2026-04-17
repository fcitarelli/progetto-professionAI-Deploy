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
                powershell """
                # Rimuove l'immagine locale se esiste già per evitare il blocco "already exists"
                docker rmi ${env.DOCKER_IMAGE}:latest -f 2>\$null
                
                # Build dell'immagine
                docker build -t ${env.DOCKER_IMAGE}:latest .
                """
            }
        }

        stage('Push Docker Image') {
        steps {
            withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                powershell """
                # Rimuoviamo eventuali spazi bianchi dalla password prima del login
                \$pass = \$env:DOCKER_PASS.Trim()
                
                # Login usando il metodo pipe compatibile con Jenkins Windows
                Write-Output \$pass | docker login -u \$env:DOCKER_USER --password-stdin
                
                if (\$LASTEXITCODE -eq 0) {
                    docker push ${env.DOCKER_IMAGE}:latest
                } else {
                    Write-Error "Login fallito con codice: \$LASTEXITCODE"
                    exit 1
                }
                """
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