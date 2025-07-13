pipeline {
  agent any

  environment {
    VENV = 'venv'
    PIP_CACHE_DIR = 'pip_cache'
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

    stage('Setup Python Env') {
      steps {
        bat '''
        python -m venv %VENV%
        %VENV%\\Scripts\\pip install --upgrade pip
        %VENV%\\Scripts\\pip install -r requirements.txt
        '''
      }
    }

    stage('Code Quality: Pylint & Black') {
      steps {
        script {
          echo 'Checking code formatting with Black...'
          bat '''
          %VENV%\\Scripts\\black --check . --exclude venv > black.diff 2>&1
          if %errorlevel% neq 0 (
              echo.
              echo Black formatting issues have been detected
              echo To auto-fix this locally, run: black .
              echo Diff saved to black.diff
              exit /b 1
          ) else (
              echo Black check passed.
          )
          '''

          echo 'Checking with Pylint...'
          bat '''
          setlocal EnableDelayedExpansion
          set FILES=
          for /R %%F in (*.py) do (
              set FILES=!FILES! %%F
          )
          %VENV%\\Scripts\\pylint --output-format=json !FILES! > pylint.json
          if %errorlevel% neq 0 (
              echo.
              echo Code quality issues detected!
              echo Please review suggestions and aim for a score ^>= 8.0.
              echo Output saved to pylint.json
              exit /b 1
          ) else (
              echo Pylint check passed.
          )
          endlocal
          '''
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
      archiveArtifacts artifacts: 'black.diff', onlyIfSuccessful: false
      recordIssues(tools: [
        pylint(pattern: 'pylint.json')
      ])
    }
  }
}
