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
    stage('Code Quality: Pylint & Black') {
        steps {
            script {
                echo 'Checking code formatting with Black...'
                // Fail the build if code is not black-formatted
                bat '''
                docker run --rm -v %CD%:/app -w /app python:3.9 sh -c "pip install -r requirements.txt && black --check . --exclude venv"
                if %ERRORLEVEL% neq 0 (
                    echo.
                    echo FAILURE -- Black formatting issues have been detected
                    echo To auto-fix this locally, run: black .
                    echo Diff saved to black.diff
                    exit /b 1
                ) else (
                    echo Black check passed.
                )
                '''

                echo 'Checking with Pylint...'
                // Fail the build if pylint score is below 8.0
                bat '''
                docker run --rm -v %CD%:/app -w /app python:3.9 sh -c "pip install -r requirements.txt && find . -name '*.py' -not -path './venv/*' -not -path './migrations/*' -not -path './__pycache__/*' | xargs pylint --output-format=json --fail-under=8.0" 
                if %ERRORLEVEL% neq 0 (
                    echo.
                    echo FAILURE -- Code quality issues detected!
                    echo Please review suggestions and aim for a score ^>= 8.0.
                    echo Output saved to pylint.json
                    exit /b 1
                ) else (
                    echo Pylint check passed.
                )
                '''

            }
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
//   post {
//         always {
//             archiveArtifacts artifacts: 'black.diff', allowEmptyArchive: true
//             archiveArtifacts artifacts: 'pylint.json', allowEmptyArchive: true
//             recordIssues(tools: [
//                 pylint(pattern: 'pylint.json')
//             ])
//         }
//     }

}