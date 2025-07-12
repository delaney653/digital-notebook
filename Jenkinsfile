pipeline {
  agent {
    dockerContainer {
        image 'docker:24.0.2-cli'
    }
  }
  
  environment{
    VENV = 'venv'
  }
  stages{
    stage('Checkout git'){
      steps{
        git branch: 'main', url: 'https://github.com/delaney653/digital-notebook'
      }
    }
    stage('Run Tests') {
        steps {
            script {
                sh 'docker-compose --profile testing up --build --abort-on-container-exit'
            }
        }
    }
  }
}