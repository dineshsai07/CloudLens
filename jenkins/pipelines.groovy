pipeline {
  agent any

  stages {
    stage('Detect Resource Waste') {
      steps {
        script {
          // Pull the official Python image and run the steps inside it:
          docker.image('python:3.9-slim').inside('-u root:root -v /var/run/docker.sock:/var/run/docker.sock') {
            sh '''
              pip3 install requests
              python3 scripts/cleanup-detector.py http://prometheus:9090 20 8
            '''
          }
        }
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'scripts/cleanup-detector.py', fingerprint: true
    }
  }
}
