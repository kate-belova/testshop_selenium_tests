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

                    echo "Chrome version:"
                    google-chrome --version

                    python3 -m venv venv
                    . venv/bin/activate

                    echo "Installing project dependencies..."
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    echo "Running Selenium tests with Chrome..."
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