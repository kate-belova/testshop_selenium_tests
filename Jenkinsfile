pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    echo "Python version:"
                    python3 --version

                    python3 -m venv venv
                    . venv/bin/activate

                    echo "Installing project dependencies..."
                    pip install -r requirements.txt

                    apt-get update
                    apt-get install -y wget unzip
                    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
                    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
                    apt-get update
                    apt-get install -y google-chrome-stable

                    echo "Chrome version:"
                    google-chrome --version
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m pytest --alluredir=allure-results -v
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-results/**/*', fingerprint: true

            echo "Build completed with status: ${currentBuild.result}"
        }

        success {
            echo '✅ All Selenium tests passed successfully!'
        }

        failure {
            echo '❌ Selenium tests failed!'
        }
    }
}