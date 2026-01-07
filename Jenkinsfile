pipeline {
    agent any

    environment {
        ADMIN_EMAIL = 'cryptocat@ssd.uz'
        ADMIN_PASSWORD = 'oash5pai2uiF3lu'
    }

    stages {
        stage('Build Image') {
            steps {
                bat 'docker build -t cryptocat-test -f Dockerfile .'
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                docker run --rm --ipc=host ^
                -e ADMIN_EMAIL=%ADMIN_EMAIL% ^
                -e ADMIN_PASSWORD=%ADMIN_PASSWORD% ^
                -v "%WORKSPACE%":/workspace ^
                -w /workspace ^
                cryptocat-test ^
                pytest --junitxml=results.xml --html=report.html --self-contained-html --alluredir=allure-results
                '''
            }
        }

        stage('Publish Results') {
            steps {
                junit 'results.xml'
                archiveArtifacts artifacts: 'results.xml, report.html, allure-results/**', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
