pipeline {
  agent any
  stages {
    stage('Detect Resource Waste') {
      steps {
        echo "Running CloudLens cleanup detector..."
        sh 'pip3 install requests'
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
