pipeline {
  agent any
  stages {
    stage('Test Compose up') {
      steps {
        sh 'docker compose up -d'
        cleanWs(cleanWhenAborted: true, cleanWhenFailure: true, cleanWhenNotBuilt: true, cleanWhenUnstable: true)
      }
    }

  }
}