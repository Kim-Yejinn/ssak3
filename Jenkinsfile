pipeline {

    agent any
        stages {
            stage('Prepare') {
                steps {
                    sh 'echo "Clone Repository"'
                    git branch: 'develop',
                        url: 'https://lab.ssafy.com/s09-mobility-smarthome-sub2/S09P22B201.git',
                        credentialsId: 'dhekgml1234@gmail.com'
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