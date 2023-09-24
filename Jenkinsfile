pipeline {
    agent any
    stages {
        // WebHook에서 감지된 변경 코드를 clone 해서 가져오기
        stage('Prepare') {
            steps {
                sh 'echo "Clone Repository"'
                git branch: 'back/feat63-jenkinstest',
                    url: 'https://lab.ssafy.com/s09-mobility-smarthome-sub2/S09P22B201.git',
                    credentialsId: '69daef35-2872-44f4-8e64-396a1a04dc02'
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
                    def containerNames = ['back', 'front']

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
                    def imageNames = ['backend-ssak3', 'frontend-ssak3']

                    for (String imageName in imageNames) {
                        sh "docker rmi ${imageName}"
                    }
                }
            }
        }

        stage('Run Docker Compose') {
            steps {
                script {
                    echo pwd()
                    def projectDir = '/home/ubuntu/S09P22B201' // docker-compose가 있는 디렉토리

                    // 작업 디렉토리를 프로젝트 디렉토리로 변경
                    dir(projectDir) {
                        // 여기에서 docker-compose를 실행하거나 다른 작업 수행
                        sh 'docker-compose up -d'
                    }
                }
            }
        }
    }
}
