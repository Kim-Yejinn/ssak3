<h1 align="middle">SSAK3</h1>
<h3 align="middle">빨래수거 로봇</h3>
<p align="middle"><img src="/img/싹쓸이 로고.png" width="30%" /></p>

<br>
<br>

# ✏️ 서비스 소개
```
SSAK3 : 알아서 빨래수거를 해주는 로봇 🤖

원하는 세탁물, 스케줄 설정을 통해 빨래를 수거해보세요!
```
<br>
<br>

# 👪 멤버
| BE, ROS | BE, ROS | BE, FE | FE, ROS | ROS | FE, ROS
| -------- | -------- | -------- | -------- | -------- | --------
| [김라현](https://github.com/wwldwwld7) | [김예진](https://github.com/Kim-Yejinn) | [오다희](https://github.com/DaHeeO) | [이정섭](https://github.com/ZScomnet) | [이승종](https://github.com/SeungJong-Lee) | [홍영기](https://github.com/YoungKiHong85) 

<br>
<br>

# 🔧 기술스택

## 🎮 시뮬레이터

<div align="middle">
<img src="https://img.shields.io/badge/ros2-22314E?style=for-the-badge&logo=ros&logoColor=white">
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/openssl-721412?style=for-the-badge&logo=openssl&logoColor=white">
<img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white">
<img src="https://img.shields.io/badge/yolo-00FFFF?style=for-the-badge&logo=yolo&logoColor=white">

**Language |** python 3.7.5

**Library |** ROS eloquent(20200124 release), Openssl 1.0.2u, Opencv 3.4.6, YOLO v5

</div>



## 👑 프론트엔드

<div align="middle">

<img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white">
<img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white">
<img src="https://img.shields.io/badge/axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white">
<img src="https://img.shields.io/badge/recoil-000000?style=for-the-badge&logo=recoil&logoColor=white">

**Language |** Javascript

**Framework |** React 18.2.0

**Library |** Axios 1.5.0, Recoil 0.7.7

<br>
<br>

</div>

## 🎺 백엔드

<div align="middle">

<img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white">
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white">
<img src="https://img.shields.io/badge/SQLAlchemy-0C0C0E?style=for-the-badge&logo=Alchemy&logoColor=white">


**Language |** Python 3.7.5

**Framework |** FastAPI 0.99.1

**Data(RDBMS) |** SQLAlchemy 2.0.20


</div>

<br>
<br>


## 🔑 인프라

<div align="middle">

<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
<img src="https://img.shields.io/badge/AWS EC2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white">
<img src="https://img.shields.io/badge/mariadb-003545?style=for-the-badge&logo=mariadb&logoColor=white">
<img src="https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white">
<img src="https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=nginx&logoColor=white">
<img src="https://img.shields.io/badge/jenkins-111111?style=for-the-badge&logo=jenkins&logoColor=white">
<img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
<img src="https://img.shields.io/badge/docker_compose-e0319d?style=for-the-badge&logo=docker&logoColor=white">


**DB |** MariaDB 8.0.34

**Server |** Git, Ubuntu 20.0.4, Nginx, Jenkins, Docker, Docker compose

</div>

## 🔗 시스템 아키텍처
<br>
<p align="middle"><img src="/img/시스템아키텍쳐.png" width="90%" /></p>

<br>
<br>

# 🎀 기능소개

## 시리얼 번호 등록
로봇의 시리얼 번호를 등록
<br>
<p align="middle"><img src="/img/시리얼번호_등록.gif" width="40%" /></p>

## 세탁물 선택 & 주행
원하는 세탁물을 선택 후 수거 명령
<br>
<p align="middle"><img src="/img/세탁물고르고주행.gif" width="40%" /></p>
<p align="middle"><img src="/img/실행로그.gif" width="40%" /></p>

## 스케줄 등록
원하는 시간대에 자동으로 수행 명령
<br>
<p align="middle"><img src="/img/스케줄_등록.gif" width="40%" /></p>

# 🖋️ 사용기술

## 맵 생성
Lidar센서를 사용하여 거리를 측정하고 맵을 생성합니다
<br>
<p align="middle"><img src="/img/슬램.gif" width="90%" /></p>

## 물체 탐지 & 위치 계산
Yolo를 사용하여 물체를 탐지하고 위치를 계산합니다
<p align="middle"><img src="/img/yolo사진.PNG" width="90%" /></p>

## 경로 생성 & 제어
<p align="middle"><img src="/img/패스트래킹.gif" width="90%" /></p>
<p align="middle"><img src="/img/셔츠만수거.gif" width="90%" /></p>

<br>
<br>


# 📐 명세
### 📬 API 명세
https://www.notion.so/API-9a5578cf822b47e68afc881373511fb3

###  🧮ERD
<p align="middle"><img src="/img/erd.png" width="90%" /></p>