pipeline {
  agent any
  stages {
    stage('Code Checkout') {
      steps {
        git(url: 'https://github.com/CI3715-LAB/software-project.git', branch: 'master', credentialsId: 'software-project-pat')
      }
    }

    stage('Get info') {
      steps {
        sh 'pwd'
        sh 'ls'
      }
    }

    stage('Build') {
      steps {
        sh 'docker compose -f ./docker-compose.yml build'
      }
    }

  }
}