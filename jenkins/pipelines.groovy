pipeline {
  agent any

  stages {
    stage('Detect Resource Waste') {
      steps {
        sh '''
          # Pull the Python image
          docker pull python:3.9-slim

          # Run cleanup-detector.py inside a throwaway container
          docker run --rm \
            -v "$WORKSPACE":/app \
            -w /app \
            python:3.9-slim \
            /bin/sh -c "pip3 install requests && python3 scripts/cleanup-detector.py http://prometheus:9090 20 8"
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
