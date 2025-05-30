pipeline {
  agent any

  stages {
    stage('Prepare Python') {
      steps {
        // Install Python3 and pip inside the Jenkins container
        sh '''
          apt-get update -y
          apt-get install -y python3 python3-pip
        '''
      }
    }

    stage('Detect Resource Waste') {
      steps {
        // Install Python deps and run the detector
        sh '''
          pip3 install --upgrade pip requests
          python3 scripts/cleanup-detector.py http://prometheus:9090 20 8
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'scripts/cleanup-detector.py', fingerprint: true
    }
  }
}
