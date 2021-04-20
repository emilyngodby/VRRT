pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
                docker {
                    image 'python:2-alpine' 
                }
            }
            steps {
                sh 'python3 manage.py migrate'
                sh 'python3 manage.py makemigrations'
                sh 'python3 train.py'
                sh 'python3 manage.py runserver' 
            }
        }
        stage('Test') { 
            steps {
                sh 'python3 manage.py test' 
            }
        }
    }
}