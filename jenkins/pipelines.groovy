pipeline {
  agent any

  stages {
    stage('Prepare Python') {
      steps {
        // Install Python3 and the requests library via apt
        sh '''
          apt-get update -y
          apt-get install -y python3 python3-requests
        '''
      }
    }

    stage('Detect Resource Waste') {
      steps {
        // Run the detector (requests is already available)
        sh 'python3 scripts/cleanup-detector.py http://prometheus:9090 20 8'
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'scripts/cleanup-detector.py', fingerprint: true
    }
  }
}
