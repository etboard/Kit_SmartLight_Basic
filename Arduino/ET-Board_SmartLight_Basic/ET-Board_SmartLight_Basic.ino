/**********************************************************************************
 * Author : (주)한국공학기술연구원
 * Program ID : smart_light
 * Description : 스마트 가로등 코딩
 **********************************************************************************/

//초음파 센서를 사용할 ET-보드 핀번호 설정
const int echoPin = D7;  // 초음파 수신부
const int trigPin = D8;  // 초음파 송신부 
const int cdsPin = A7;   // 조도 센서

const int ledPin1 = D3;  // 가로등 1번 LED
const int ledPin2 = D4;  // 가로등 2번 LED

const int cds_threshold = 300;  // 조도센서 임계치
const int usw_threshold = 30;   // 초음파센서 임계치

void setup() {
  Serial.begin(57600);
  // 초음파 센서 모드설정 : trigPin를 출력모드로 설정, echoPin를 입력모드로 설정
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  // 조도 센서를 입력모드로 설정
  pinMode(cdsPin, INPUT);   
  // LED 출력모드 설정
  pinMode(ledPin1, OUTPUT); 
  pinMode(ledPin2, OUTPUT); 
}

void loop() {
  // 초음파 송신 후 수신부는 HIGH 상태로 대기
  digitalWrite(trigPin, LOW);
  digitalWrite(echoPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // echoPin 이 HIGH를 유지한 시간 저장
  unsigned long duration = pulseIn(echoPin, HIGH); 
  // HIGH 였을 때 시간(초음파 송수신 시간)을 기준으로 거리를 계산
  float distance = ((float)(340 * duration) / 10000) / 2;  

  // 조도 센서 입력 확인
  int cdssensorValue = analogRead(cdsPin);

  // 주변 밝기에 따라 따라 LED1 제어
  if (cdssensorValue < cds_threshold) { // 조도 센서값이 cds_threshold 이상이면
    digitalWrite(ledPin1, HIGH); // LED 켜짐
    } else {
    digitalWrite(ledPin1, LOW);  // LED 꺼짐
    }
  Serial.print("  조도 센서 : ");
  Serial.println(cdssensorValue);
    
  // 장애물 감지 여부에 따라 LED2 제어
  if (distance < usw_threshold) { // 거리가 usw_threshold 이상이면
    digitalWrite(ledPin2, HIGH); // LED 켜짐
    } else {
    digitalWrite(ledPin2, LOW);  // LED 꺼짐
    }
  Serial.print("초음파 센서 : ");
  Serial.print(distance);
  Serial.println("cm");
  Serial.println("--------------------");
  
  delay(300);
}


//┌────────────────────────────────┐
//│                                                      │
//│     (주)한국공학기술연구원 http://et.ketri.re.kr        │
//│                                                      │ 
//└────────────────────────────────┘
