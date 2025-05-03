pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        git(url: 'https://github.com/3D23/neuralBackend.git', branch: 'main')
        sh '''sh "pwd"
sh "ls"'''
      }
    }

    stage('Clear') {
      steps {
        cleanWs(cleanWhenFailure: true, cleanWhenAborted: true, cleanWhenNotBuilt: true, cleanWhenSuccess: true, cleanWhenUnstable: true, cleanupMatrixParent: true, deleteDirs: true, disableDeferredWipeout: true)
      }
    }

  }
}