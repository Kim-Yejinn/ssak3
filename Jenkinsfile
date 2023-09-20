pipeline {

    agent any
        stages {
            stage('Prepare') {
                steps {
                    sh 'echo "Clone Repository"'
                    git branch: 'develop',
                        url: 'https://lab.ssafy.com/s09-mobility-smarthome-sub2/S09P22B201.git',
                        credentialsId: '8db2b91b-769d-456b-9d19-d19611824ba3'
                }
                post {
                    success {
                        sh 'echo "Successfully Cloned Repository"'
                    }
                    failure {
                        sh 'echo "Failed in Clonning Repository"'
                    }
                }
            }
            
        }
}