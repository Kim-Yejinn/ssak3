pipeline {
    agent any
    stages {
        // WebHook에서 감지된 변경 코드를 clone 해서 가져오기
        stage('Prepare') {
            steps {
                sh 'echo "Clone Repository"'
                git branch: 'back/feat63-jenkinstest',
                    url: 'https://lab.ssafy.com/s09-mobility-smarthome-sub2/S09P22B201.git',
                    credentialsId: '8db2b91b-769d-456b-9d19-d19611824ba3'
            }
            post {
                success {
                    sh 'echo "Successfully Cloned Repository"'
                }
                failure {
                    sh 'echo "Failed in Cloning Repository"'
                }
            }
        } 

        stage('Docker container delete') {
            steps {
                script {
                    def containerNames = ['back', 'front', 'nginx']

                    for (String containerName in containerNames) {
                        sh "docker stop ${containerName}"
                        sh "docker rm ${containerName}"
                    }
                }
            }
        }

        stage('Docker image delete') {
            steps {
                script {
                    def imageNames = ['test-backend', 'test-frontend', 'nginx']

                    for (String imageName in imageNames) {
                        sh "docker rmi ${imageName}"
                    }
                }
            }
        }

        stage('Deploy with Docker-Compose') {
            steps {
                script {
                    dir('test') {
                        sh 'docker-compose up -d'
                    }
                }
            }
        }
    }
}
