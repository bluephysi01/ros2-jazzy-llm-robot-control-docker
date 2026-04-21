# ROS 2 Jazzy LLM Robot Control Project

이 저장소는 Docker를 활용한 ROS 2 Jazzy 개발 환경에서 LLM(대규모 언어 모델) 기반 로봇 제어 시뮬레이션 환경을 빠르고 쉽게 구축하기 위한 가이드와 소스 코드를 제공합니다.
Docker 이미지에 모든 의존성 라이브러리가 사전 설치되어 있어, 빌드 후 바로 사용할 수 있습니다.

---

## 1. 사전 준비 (GUI 허용)
도커 컨테이너 내부에서 실행되는 그래픽 프로그램(Gazebo, RViz2 등)의 창을 호스트(사용자 PC) 화면에 띄우기 위한 필수 설정입니다. 
컴퓨터 부팅 후 로컬 터미널에서 최초 1회 실행해 주세요.

```bash
xhost +local:docker
```

---

## 2. 프로젝트 다운로드
GitHub에서 소스코드 및 개발 환경에 필요한 도커 파일을 로컬 컴퓨터로 복제(Clone)합니다.

```bash
git clone https://github.com/bluephysi01/ros2-jazzy-llm-robot-control-docker.git
cd ros2-jazzy-llm-robot-control-docker
```

---

## 3. 도커 이미지 빌드
제공된 Dockerfile을 사용하여 ROS 2 Jazzy와 LLM 로봇 제어에 필요한 모든 패키지가 설치된 개발 환경 이미지를 생성합니다.
*(인터넷 환경에 따라 이미지 빌드에 약간의 시간이 소요될 수 있습니다.)*

```bash
sudo docker build -t ros2_jazzy_pinky .
```

---

## 4. 컨테이너 생성 및 실행
빌드된 이미지를 기반으로 컨테이너를 생성하고 내부 터미널로 진입합니다.
로컬 호스트의 src 폴더가 컨테이너 내부(/home/root/ros2_pinky_ws/src)와 동기화(볼륨 마운트)되므로, 컨테이너 외부에서 코드를 수정해도 즉시 반영됩니다.

```bash
sudo docker run -it \
  --name ros2_jazzy_pinky \
  --privileged \
  --network host \
  --env="DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  --env="TERM=xterm-256color" \
  --env="force_color_prompt=yes" \
  --env="LIBGL_ALWAYS_SOFTWARE=1" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  --volume="$PWD/src:/home/root/ros2_pinky_ws/src" \
  ros2_jazzy_pinky
```

---

## 5. 자주 사용하는 명령어 모음 (Cheatsheet)

### 컨테이너 재접속
작업을 마치고 컨테이너를 종료한 후, 나중에 다시 접속할 때 사용합니다.
```bash
sudo docker start -ai ros2_jazzy_pinky
```

### 새 터미널 창 열기
현재 실행 중인 컨테이너에 새로운 터미널 세션을 추가로 열어 다중 작업을 할 때 사용합니다.
```bash
sudo docker exec -it ros2_jazzy_pinky bash
```

### 소스코드 수정 후 빌드 (컨테이너 내부)
호스트 편집기(VS Code 등)에서 소스 코드를 수정한 뒤, 컨테이너 내부 터미널에서 작업 공간을 빌드하고 적용하는 방법입니다.
```bash
cd /home/root/ros2_pinky_ws
colcon build --symlink-install
source install/setup.bash
```
