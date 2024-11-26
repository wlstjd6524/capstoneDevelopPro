# [ 2024.09 - 12 캡스톤디자인 프로젝트 ]
## 👨‍🏫 프로젝트 소개
Wi-Fi CSI Data 를 활용한 실시간 행동 모니터링 및 알림 시스템


## ⏲️ 개발 기간 
- 2024.09.16 ~ 2024.11.26
  - 프로젝트에 대한 이해 및 학습
  - 프로젝트에 필요한 하드웨어 및 소프트웨어 구성
  - 오픈소스 채택
  - 환경구성
  - 데이터 수집
  - 머신러닝 모델 구현 및 학습
  - UI/UX 구현
  - UI/UX 와 맞는 앱데이터 개발
  - 프로젝트 제출
  - 발표 및 평가


## 🧑‍🤝‍🧑 팀 소개
- **이진성** : 팀장
- **남궁준** : 팀원
- **홍성환** : 팀원


## 💻 개발환경 및 도구와 하드웨어 플랫폼 정보
- Raspberry Pi 4 Model B 2GB RAM
  - Raspberry Pi OS Kernel Version : 5.10.92
  - Nexmon Tool & Nexmon OpenSource
    - Nexmon OpenSource : <https://github.com/nexmonster/nexcsi>
- Wi-Fi AP
- TensorFlow_GPU ver 2.10.0 , Android TensorFlowLite
- WireShark
- Miniconda Virtual Environment
- Python 3.9.0
- NVIDIA CUDA Toolkit 11.2
- NVIDIA cuDNN 8.1
- AndroidStudio by Kotlin


## 📌 프로젝트개요
기존의 행동 인식(HAR: Human Activity Recognition) 시스템은 주로 카메라나 웨어러블 센서를 사용해 사람의 행동을 분석해 왔습니다. <br>
하지만 이들 기술은 높은 설치 비용, 사생활 침해와 같은 문제점을 가지고 있습니다. <br>
본 프로젝트는 Wi-Fi 신호에서 추출한 CSI(Channel State Information)를 이용하여 저비용, 비접촉, 비침해적인 행동 인식 시스템을 구현하는 것을 목표로 합니다. <br>
<br>
Wi-Fi CSI 기반 기술은 추가적인 센서 없이 Wi-Fi 신호만으로 실내 공간의 행동을 분석할 수 있습니다. <br>
이를 활용하여 LoS(Line of Sight) 및 NLoS(Non-Line of Sight) 환경에서의 신뢰성 높은 행동 인식을 수행하고, 노인의 행동 데이터를 모니터링하여 돌봄 서비스를 제공할 수 있는 애플리케이션을 개발하고자 합니다. <br>
<br>
이 시스템은 특히 노인의 안전 관리에 초점을 맞추어, 움직임이 없거나 넘어짐과 같은 이상 상황을 탐지했을 때 실시간 알림을 통해 사용자(보호자)에게 경고를 전송하는 기능을 제공합니다. <br>


## 📏 프로젝트 목적
**🥇 수행배경** 
  - 인구 고령화가 가속화됨에 따라 노인들의 안전을 보장하고 돌봄 효율성을 높이기 위한 기술적 솔루션의 필요성이 증가하고 있습니다. <br>
  특히, 노인들이 가정 내에서 넘어지거나 장시간 움직임이 없는 상황은 심각한 건강 및 안전 문제를 초래할 수 있습니다. <br>
  이러한 위험을 조기에 감지하고 즉각적으로 대응할 수 있는 시스템이 필수적입니다. <br> <br>
  
**🥈 필요성**
  - 기존의 노인 케어 서비스는 웨어러블 장비나 단순 알람 시스템에 의존하는 경우가 많습니다. <br>
  하지만 웨어러블 장비는 착용 불편과 잦은 배터리 충전 문제 등으로 활용도가 제한적입니다. <br>
  또한, 단순 알람 시스템은 행동 상태를 정확히 감지하지 못해 오작동 가능성이 높습니다. <br> <br>
  
**🥉 목적** 
  - 본 과제는 Wi-Fi CSI(Channel State Information)를 활용한 행동 인식 기술을 기반으로 한 실시간 노인 돌봄 케어 애플리케이션을 개발하는 것을 목적으로 합니다. <br>
  이를 통해 노인의 상태를 정확히 파악하고, 넘어짐 및 장시간 움직임이 없는 상황을 실시간으로 감지하여 사용자에게 알림을 제공하는 시스템을 구현하고자 합니다. <br> <br>


## ✒️ 프로젝트 목표
**LoS(가시선) 환경 : 중간 장애물 없이 인간 행동을 신호가 곧바로 받는 환경** <br>
**NLoS(비가시선) 환경 : 중간에 장애물이 있는 상태에서 인간 행동을 신호가 받는 환경** <br>
<br>
또한 프로젝트 목표는 다음과 같습니다. <br>
1. LoS/NLoS 환경 구분 및 행동 인식 정확도 향상
   - Wi-Fi 신호를 활용하여 LoS(가시선) 및 NLoS(비가시선) 환경을 구분.
   - 각 환경에 적합한 HAR 모델을 학습시켜 행동 인식 정확도를 극대화.
2. 비접촉 기반의 행동 인식 시스템 구현
    - Wi-Fi CSI 데이터를 활용해 기존 센서나 카메라 없이 행동 데이터를 분석하는 시스템 구축.
    - 데이터 노이즈 제거 및 필터링을 통해 정확도를 높이고 실시간 처리가 가능하도록 최적화.
3. 실시간 행동 데이터 분석 및 알림 시스템 개발
    - 노인이 넘어지거나 장시간 움직임이 없는 상황을 실시간으로 탐지.
    - 이상 상황 발생 시 보호자에게 Android 애플리케이션을 통해 알림 전송.
4. 사용자 친화적 애플리케이션 개발
    - 간단하고 직관적인 UI/UX를 통해 보호자가 쉽게 사용할 수 있는 앱 제공.
    - 머신러닝 모델과의 원활한 통합으로 실시간 데이터 처리를 지원.
5. 확장성과 호환성 고려
    - Wi-Fi 신호 기반 시스템으로 다양한 공간에서 활용 가능.
    - 실시간 스트리밍 및 데이터 분석을 위한 Python 기반 서버와 Android 앱 간 연동.


## 🔨 프로젝트 아키텍처
![프로그램 아키텍처](https://github.com/user-attachments/assets/a5017301-e603-4ab6-8e7a-a293f43f2a5a)


## 📍 기대효과 및 활용방안
**기대효과**
  - 기존 카메라 및 센서 기반의 행동 인식 기술에 비해 설치 비용이 낮고 사생활 침해 우려가 적음.
  - LoS/NLoS 환경에 맞춘 행동 인식 정확도 개선으로 다양한 환경에서 활용 가능.
  - 노인의 움직임 데이터를 실시간으로 모니터링하여 이상 행동(예: 넘어짐, 장시간 움직임 없음)을 감지해 빠르게 대응 가능.

**활용방안**
  - 노인 돌봄 서비스: 독거노인 또는 요양원의 실시간 상태 모니터링.
  - ↓↓ 아래 활용방안은 Wi-Fi AP 를 통해 받은 CSI 행동데이터만으로 구현할 수 있는 추가적 활용방안 입니다. ↓↓
  - 스마트 홈 자동화: Wi-Fi 네트워크를 활용한 움직임 기반 조명, 에어컨 제어.
  - 의료 모니터링: 병원에서 환자 상태를 실시간 모니터링하고 이상 상황 감지.
  - 스마트 시티 구현: 공공장소에서의 비접촉식 행동 인식 기술 적용.


## ✍ 프로젝트 작업 내용
**⚽ 환경구성**
- CSI 데이터 수신기
![CSI 데이터 수신기](https://github.com/user-attachments/assets/3f43c15a-7a49-43dd-b5f4-9acf9371d6fb)

- CSI 데이터 캡처기
![CSI 데이터 캡쳐기](https://github.com/user-attachments/assets/382a7343-5ce0-4e53-9d32-1df4fd926762)

- Wi-Fi AP 환경
![Wi-Fi AP 환경](https://github.com/user-attachments/assets/81d6aaf5-092f-44e0-892a-7780ef0d8ec0)

- 핑 pc 와 캡처기 pc 환경구성
![핑 pc 와 캡쳐기 pc 환경구성](https://github.com/user-attachments/assets/d771d25c-5a59-421e-b827-0e39a8e023f2)

- 캡처기 pc 환경
![캡쳐기 pc 환경구성](https://github.com/user-attachments/assets/c4e0df8c-9f43-4a2a-af5e-7ec4e38efa73)

- LoS 환경구현
![LoS 환경](https://github.com/user-attachments/assets/21afba96-03d7-46b5-94dc-4e335a445b4b)

- NLoS 환경구현
![NLoS 환경](https://github.com/user-attachments/assets/811a2173-c407-4d97-82c7-73a95145bcdc)

**⚾ 데이터 전처리 및 학습**
- 행동에 대한 결과값이 저장된 .pcap 파일을 전처리 과정을 겪어 csv 로 변환 <br>
![01](https://github.com/user-attachments/assets/8585708e-76ea-461e-a97f-8255de91552f)

- 여러개의 csv 파일을 통합하여 균형있게 통합한 totalCsv 파일로 결합
- 또한 NVIDIA CUDA 및 cuDNN 과 TensorFlow_GPU 버전을 맞추어 GPU 기반 학습을 할 수 있는 라이브러리 활성화
![02](https://github.com/user-attachments/assets/8bf6f219-48f7-4a06-9ea6-30912276eb6d)

- Epoch 50 으로 설정 후 GPU 기반 학습 시작
![03](https://github.com/user-attachments/assets/17a2473c-0294-45fd-ac5f-7c08e7e005bf)

- LoS/NLoS 모델 학습 결과
![04](https://github.com/user-attachments/assets/af8dc319-2611-4253-83ed-67c95ab7fef2)

- HAR (LoS/NLoS 환경별 행동 인식) 모델 학습 결과
1) LoS 환경 HAR 모델
![05](https://github.com/user-attachments/assets/2dac1f4d-abc8-4b05-8a8b-6fead9541d43)

2) NLoS 환경 HAR 모델
![06](https://github.com/user-attachments/assets/4c41ae42-9f3a-41b5-9354-d21665387479)

**!! 다음 3개의 모델 중 학습율이 가장 높은 초기 모델 (LoS/NLoS) 모델을 채택하여 사용하였습니다. !!**

**🥎 학습해서 나온 모델 성능을 파일화**
![07](https://github.com/user-attachments/assets/6d6f5175-2fd0-4329-9b8f-d10e072418ee)

**🏀 서버실행**
- Server IP 및 Server Port 설정
![07-1](https://github.com/user-attachments/assets/d86cdf86-e962-424d-9c54-d4e49c6fdbb3)

- Python 기반 Server 실행
![09](https://github.com/user-attachments/assets/4a966bf9-291e-4312-8fc4-600be1b4e8f4)


## 💾 프로젝트 결과
- 애플리케이션 테스팅을 위한 에뮬레이터 ADB Data 연결
![08](https://github.com/user-attachments/assets/28ab81d6-6495-47ec-ab36-80e5c1ee13c8)

- 애플리케이션 <br>
![10](https://github.com/user-attachments/assets/8b8deaf9-11f4-495f-b03d-9d1686cc9a5c)

- 서버 연결 버튼을 눌렀을 때 애플리케이션에서 연동된 모습 (왼쪽 상단 시간 체크 엄수) <br>
![11](https://github.com/user-attachments/assets/2c11576d-9b80-462a-91b0-a1da21b03d27)

- 서버에서는 애플리케이션에 응답을 받은 후 실시간으로 행동을 받은 파일을 앱으로 전송하는 모습
![13](https://github.com/user-attachments/assets/49ee4a98-d589-4a6b-8623-ef2da8053b56)

- 1분이 지나서 움직임이 없는 상태를 읽고 앱에서 알림 전송 p.s) 앱에서 알람이 정상적으로 작동하는지 체크하기 위해 테스트 동안 시간값을 1시간 -> 1분 값으로 설정. <br>
![12](https://github.com/user-attachments/assets/1ae53d61-00ce-4d34-a593-483e4bad98ea)


## 🔎 프로젝트 한계 및 개선사항
1. 프로젝트 성과 및 한계
    - 프로젝트 시연 영상에 서버 -> 앱으로 데이터가 전달되는 과정을 담았으나,
    다른 시나리오 (앱->서버, 사용자와의 인터랙션 등)가 포함되지 않은 점이 아쉬웠습니다. <br>
2. 데이터 수집 및 전처리의 한계
    - 행동 데이터를 수집할 때 넘어지는 데이터를 포함하지 않아, 이후 앱 개발 시 앉아있는 데이터로 대체하여 처리한 점이 한계로 작용했습니다.
    - 데이터의 다양성과 품질을 개선하기 위한 방법에 대한 고찰을 추가할 수 있습니다. <br>
3. 행동 인식 모델의 제약
    - 걸어다니는 행동 데이터의 표준편차 변동성이 높아 일부 데이터에서는 움직임을 인식하지 못하는 문제가 있었습니다.
    - 이로 인해 행동 감지 기능이 제한적으로 구현된 점이 아쉬웠습니다.
4. 향후 개선 방향
    - 행동 데이터의 다양성을 확보하고 표준화를 적용해 모델의 성능을 개선할 필요가 있습니다.
    - 실시간 상호작용과 더불어 다양한 데이터 흐름(양방향 데이터 전송)을 시연할 수 있는 추가 기능을 구현해야 합니다.

