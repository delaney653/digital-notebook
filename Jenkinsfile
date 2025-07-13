pipeline {
  agent any
  
  environment{
    VENV = 'venv'
  }
  stages{
    stage('Clean Docker Environment') {
        steps {
            script {
                bat 'docker-compose down --volumes --remove-orphans || true'
                bat 'docker system prune -f || true'
            }
        }
    }
    stage('Checkout git'){
      steps{
        git branch: 'main', url: 'https://github.com/delaney653/digital-notebook'
      }
    }
    stage('Run Tests') {
        steps {
            script { 
                try {
                    bat 'docker-compose --profile testing up --build --abort-on-container-exit'
                } finally { //check if this can stop it from hanging
                    bat 'docker-compose --profile testing down --volumes --remove-orphans'
                    bat 'docker-compose down --volumes --remove-orphans'
                }  
            }
        }
    }
  }
}