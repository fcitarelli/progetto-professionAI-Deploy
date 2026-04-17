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
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Tests') {
            steps {
                sh 'python -m pytest tests -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:latest ."
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh """
                docker stop sentiment-api || true
                docker rm sentiment-api || true
                docker run -d -p 8000:8000 --name sentiment-api ${DOCKER_IMAGE}:latest
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
            sh 'docker logout || true'
            cleanWs()
        }
    }
}
