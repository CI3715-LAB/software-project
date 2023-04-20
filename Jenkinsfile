pipeline {
  agent any
  stages {
    stage('Code Checkout') {
      steps {
        git(url: 'https://github.com/CI3715-LAB/software-project.git', branch: 'master', credentialsId: 'software-project-pat')
      }
    }

    stage('Build') {
      steps {
        sh 'docker compose -f ./docker-compose.yml build'
        sh 'pip install -r requirements.txt'
      }
    }

    stage('Test') {
      steps {
        sh 'python3 -m unittest discover -s ./shortTests'
        input(id: 'DeployGate', message: 'Deploy?', ok: 'Deploy')
      }
    }

    stage('Deploy') {
      steps {
        echo 'deploying the application'
        sh 'docker compose up -d'
      }
    }

    stage('Exit') {
      steps {
        sh 'docker compose down'
      }
    }
  }
  
  post {
    always {
      echo 'The pipeline completed'
      junit(allowEmptyResults: true, testResults: '**/test_reports/*.xml')
    }

    success {
      echo 'Flask Application Up and running!!'
    }

    failure {
      echo 'Build stage failed'
      error 'Stopping early…'
    }

  }
}