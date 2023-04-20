pipeline {
  agent any
  stages {
    stage('Test Compose up') {
      steps {
        cleanWs(cleanWhenAborted: true, cleanWhenFailure: true, cleanWhenNotBuilt: true, cleanWhenUnstable: true)
      }
    }

  }
}