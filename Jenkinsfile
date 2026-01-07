pipeline {
    agent any

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
