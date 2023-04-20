pipeline {
  agent any
  stages {
    stage('Code Checkout') {
      steps {
        git(url: 'https://github.com/CI3715-LAB/software-project.git', branch: 'jenkins', credentialsId: 'software-project-pat')
      }
    }

  }
}