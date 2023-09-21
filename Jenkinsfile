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

            stage('Docker stop') {
                steps {
                    sh 'echo "BUild FastAPI Start"'
                    dir('backend') {
                        sh 'echo "Docker Container Stop"'
                        // 도커 컴포즈 권한설정
                        sh 'chmmod -R 777 /usr/local/bin'
                        sh 'chmod +x /usr/local/bin/docker-compose'
                        //기존 백그라운드에 돌아가는 컨테이너 중지
                        sh 'docker-compose -f docker-compose-prod.yml down'

                    }
                }
                post {
                    failure {
                        sh 'echo Docker Fail'
                    }
                }
            }
            
        }
}

pipeline {
    
agent any
    stages {
				// # 준비단계 -> Merge가 된 git 파일을 webHook에서 감지하여 갖고온다.
        stage('Prepare') {
            steps {
                sh 'echo "Clonning Repository"'
                git branch: 'master',
                    url: 'https://lab.ssafy.com/s09-mobility-smarthome-sub2/S09P22B201.git',
                    credentialsId: '8db2b91b-769d-456b-9d19-d19611824ba3'
            }
            post {
                success {
                     sh 'echo "Successfully Cloned Repository"'
                 }
                 failure {
                     sh 'echo "Fail Cloned Repository"'
                 }
            }
        }


        // stage('[BE]Bulid Gradle') {
        //     steps {
        //         sh 'echo "Bulid Gradle Start"'
        //         dir('BE') {

        //         }
        //     }
        //     post {
        //          failure {
        //              sh 'echo "Bulid Gradle Fail"'
        //         }
        //     }
        // }
				// #기존에있는 Docker 컨테이너들을 내려야함.
        stage('Docker stop'){
            steps {
                dir('backend'){
                    sh 'echo "Docker Container Stop"'
    //              도커 컴포즈 다운
                    // sh 'curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose'
    //              해당 도커 컴포즈 다운한 경로로 권한 설정
                    // sh 'chmod -R 777 /usr/local/bin'
                    // sh 'chmod +x /usr/local/bin/docker-compose'
    //              기존 백그라운드에 돌아가던 컨테이너 중지
										// ## 기존 백그라운드에 돌아가던 컨테이너들을 DooD 방식으로 다운시킴.
                    sh 'docker-compose -f /jenkins/workspace/docker-compose-prod.yml down'
                    // sh 'docker-compose -f docker-compose-prod.yml down'

                }


            }
            post {
                 failure {
                     sh 'echo "Docker Fail"'
                }
            }
        }
				// #정지된 도커 컨테이너를 삭제함
        stage('RM Docker'){
            steps {

                sh 'echo "Remove Docker"'

                //정지된 도커 컨테이너 찾아서 컨테이너 ID로 삭제함
								// #ttp로 시작하는건 다 삭제함.
                sh '''
                    result=$( docker container ls -a --filter "name=ttp*" -q )
                    if [ -n "$result" ]
                    then
                        docker rm $(docker container ls -a --filter "name=ttp*" -q)
                    else
                        echo "No such containers"
                    fi
                '''
                sh '''
                                    result=$( docker container ls -a --filter "name=ttp*" -q )
                                    if [ -n "$result" ]
                                    then
                                        docker rm $(docker container ls -a --filter "name=ttp*" -q)
                                    else
                                        echo "No such containers"
                                    fi
                                '''

                // homesketcher로 시작하는 이미지 찾아서 삭제함
                sh '''
                    result=$( docker images -f "reference=ttp*" -q )
                    if [ -n "$result" ]
                    then
                        docker rmi -f $(docker images -f "reference=ttp*" -q)
                    else
                        echo "No such container images"
                    fi
                '''
                sh '''
                                    result=$( docker images -f "reference=ttp*" -q )
                                    if [ -n "$result" ]
                                    then
                                        docker rmi -f $(docker images -f "reference=ttp*" -q)
                                    else
                                        echo "No such container images"
                                    fi
                                '''
                // 안쓰는이미지 -> <none> 태그 이미지 찾아서 삭제함
                sh '''
                    result=$(docker images -f "dangling=true" -q)
                    if [ -n "$result" ]
                    then
                        docker rmi -f $(docker images -f "dangling=true" -q)
                    else
                        echo "No such container images"
                    fi
                '''

            }
            post {
                 failure {
                     sh 'echo "Remove Fail"'
                }
            }
        }
				# 프로젝트 내에 있는 start-prod.sh 실행
        stage('Set Permissions') {
                    steps {
                        // 스크립트 파일에 실행 권한 추가
                        sh 'chmod +x /jenkins/workspace/start-prod.sh'
                    }
                }
        stage('Execute start-prod.sh Script') {
            steps {
                // start-prod.sh 스크립트 실행
                sh '/var/jenkins_home/workspace/start-prod.sh'
            }
        }



//         stage('[FE] prepare') {
//             steps {
//                 dir('frontend'){
//                     sh 'echo " Frontend Bulid Start"'
//                     script {
//                         sh 'docker-compose stop'
//                         sh 'docker rm vue'
//                         sh 'docker rmi frontend_vue'
//                     }
//                 }


//             }

//             post {
//                 failure {
//                     sh 'echo "Frontend Build Fail"'
//                 }
//             }
//         }
//         stage('Fronteend Build & Run') {
//             steps {
//                 dir('frontend'){
//                     sh 'echo " Frontend Build and Start"'
//                     script {

// //                          업데이트된 코드로 빌드 및 실행
//                         sh 'docker-compose up -d'
//                     }
//                 }


//             }

//             post {
//                 failure {
//                     sh 'echo "Bulid Docker Fail"'
//                 }
//             }
//         }
    }
}