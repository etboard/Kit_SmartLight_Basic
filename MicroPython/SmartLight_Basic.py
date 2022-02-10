# ******************************************************************************************
# FileName     : SmartPot_Basic_python
# Description  : 스마트화분 코딩 키트 (기본)
# Author       : 손정인
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2022.02.08
# Reference    :
# Modified     :
# ******************************************************************************************

# import
import time
from machine import Pin, time_pulse_us, ADC
from ETboard.lib.pin_define import *
from ETboard.lib.OLED_U8G2 import *

# global variable
led1 = Pin(D2)                                     # 가로등 1번 LED
led2 = Pin(D3)                                     # 가로등 2번 LED
TRIG = Pin(D9)                                     # 초음파 송신부                
ECHO = Pin(D8)                                     # 초음파 수신부
cds = ADC(Pin(A3))                                 # 조도 센서 

# setup
def setup():
    TRIG.init(Pin.OUT)                             # 초음파 송신부 출력 모드 설정하기                     
    ECHO.init(Pin.IN)                              # 초음파 수신부 입력 모드 설정하기
    led1.init(Pin.OUT)                             # 가로등 1번 LED 출력 모드 설정하기
    led2.init(Pin.OUT)                             # 가로등 2번 LED 출력 모드 설정하기
    cds.atten(ADC.ATTN_11DB)                       # 조도 센서 입력 모드 설정하기

# main loop
def loop():
    TRIG.value(LOW)
    ECHO.value(LOW)
    time.sleep_ms(2)
    TRIG.value(HIGH)
    time.sleep_ms(10)
    TRIG.value(LOW)
    
    duration = time_pulse_us(ECHO, HIGH)           # echoPin 이 HIGH 를 유지한 시간 저장
    distance = ((34 * duration) / 1000) / 2        # HIGH 였을 때 시간(초음파 송수신 시간)을 기준으로 거리를 계산
    cdsValue = (cds.read()) / 10                   # 조도 센서 입력 확인
    
    #주변 밝기에 따라 따라 LED1 제어
    if( distance < 10 ) :                          # 조도 센서값이 10 이하면
        led1.value(HIGH)                           # LED 켜짐
    else :
        led1.value(LOW)                            # LED 꺼짐
        
    print("초음파 센서  : ", distance)
    
    # 장애물 감지 여부에 따라 LED2 제어
    if( cdsValue < 300 ) :                         # 조도 센서값이 300 이하면
        led2.value(HIGH)                           # LED 켜짐
    else :
        led2.value(LOW)                            # LED 꺼짐
    
    print("조도 센서  : ", cdsValue)
    print("---------------------")
    
    time.sleep(0.1)                                


if __name__ == "__main__":
    setup()
    while True:
        loop()
        
# ==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
# ==========================================================================================
        