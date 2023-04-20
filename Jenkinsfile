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
      }
    }

    stage('Test') {
      steps {
        sh 'python3 test_app.py'
        input(id: "Deploy Gate", message: "Deploy ${params.project_name}?", ok: 'Deploy')
      }
    }

    stage('Run') {
      steps {
        echo "running the application"
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
            junit allowEmptyResults: true, testResults:'**/test_reports/*.xml'
        }
        success {                   
            echo "Flask Application Up and running!!"
        }
        failure {
            echo 'Build stage failed'
            error('Stopping early…')
        }
      }
}

  }
}