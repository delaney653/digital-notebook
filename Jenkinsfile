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
                    exit /b 1
                ) else (
                    echo Black check passed.
                )
                '''

                echo 'Checking with Pylint...'
                // Fail the build if pylint score is below 8.0
                bat '''
                docker run --rm -v %CD%:/app -w /app python:3.9 sh -c "pip install -r requirements.txt && find . -name '*.py' -not -path './venv/*' -not -path './migrations/*' -not -path './__pycache__/*' | xargs pylint --output-format=colorized --fail-under=8.0" 
                if %ERRORLEVEL% neq 0 (
                    echo.
                    echo FAILURE -- Code quality issues detected with Pylint!\
                    echo To fix this locally run: pylint <file_name> in the appropriate directoy.
                    echo Please review suggestions and aim for a score ^>= 8.0.
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
                    bat 'if not exist reports mkdir reports' //make reports directory if it doesn't exist

                    bat '''
                    docker-compose --profile testing up --build --abort-on-container-exit
                    
                    REM Copy test reports from container to host
                    for /f %%i in ('docker-compose --profile testing ps -q') do (
                        docker cp %%i:/app/junit.xml ./reports/junit.xml 2>nul || echo "No JUnit XML found"
                        docker cp %%i:/app/coverage.xml ./reports/coverage.xml 2>nul || echo "No coverage XML found"
                    )
                    '''
                } finally { //check if this can stop it from hanging
                    bat 'docker-compose --profile testing down --volumes --remove-orphans'
                    bat 'docker-compose down --volumes --remove-orphans'
                }  
            }
        }
    }
  }
  post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            publishTestResults testResultsPattern: 'reports/junit.xml', allowEmptyResults: true
            
            publishCoverage adapters: [
                coberturaAdapter('reports/coverage.xml')
            ], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
            
            recordIssues(tools: [
                pylint(pattern: 'pylint.json')
            ])
        }
    }

}