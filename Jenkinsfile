pipeline {
  agent any

  environment {
    VENV = 'venv'
  }

  stages {
    stage('Clean Docker Environment') {
      steps {
        script {
          bat 'docker-compose down --volumes --remove-orphans || true'
          bat 'docker system prune -f || true'
        }
      }
    }

    stage('Checkout git') {
      steps {
        git branch: 'main', url: 'https://github.com/delaney653/digital-notebook'
      }
    }

    stage('Code Quality: Pylint & Black') {
      steps {
        script {
          echo 'Checking code formatting with Black...'
          try {
            bat '''
              call venv\\Scripts\\activate
              black --check . --exclude "venv|.*migrations.*" > black.diff 2>&1
            '''
            echo "Black formatting check passed!"
          } catch (err) {
            echo "Black formatting check failed! Please run 'black .' locally to fix formatting issues."
            echo "Diff saved to black.diff"
            error("Black formatting issues detected.")
          }

          echo 'Checking with Pylint...'
          try {
            bat '''
              call venv\\Scripts\\activate
              del python_files.txt 2>nul
              for /f "delims=" %%i in ('dir /s /b *.py ^| findstr /v /i "venv migrations __pycache__"') do echo %%i >> python_files.txt
              pylint --output-format=json --fail-under=8.0 @python_files.txt > pylint.json 2>&1
            '''
            echo "Pylint check passed!"
          } catch (err) {
            echo "Pylint check failed! Please improve code quality to meet minimum score of 8.0."
            echo "Output saved to pylint.json"
            error("Pylint quality gate not met.")
          }
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          try {
            bat 'docker-compose --profile testing up --build --abort-on-container-exit'
          } finally {
            bat 'docker-compose --profile testing down --volumes --remove-orphans'
            bat 'docker-compose down --volumes --remove-orphans'
          }
        }
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'black.diff', allowEmptyArchive: true
      archiveArtifacts artifacts: 'pylint.json', allowEmptyArchive: true
      archiveArtifacts artifacts: 'python_files.txt', allowEmptyArchive: true
      recordIssues(tools: [
        pylint(pattern: 'pylint.json')
      ])
    }
  }
}
