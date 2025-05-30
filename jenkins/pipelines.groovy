pipeline {
  /*  
   * Runs all stages inside the official Python image,
   * which already includes python3 and pip.
   */
  agent any

  stages {
    stage('Detect Resource Waste') {
      steps {
        // Install the requests library
        sh 'pip3 install requests'

        // Run the detector against Prometheus in the Compose network
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
