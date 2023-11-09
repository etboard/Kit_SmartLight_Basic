# *****************************************************************************************
# FileName     : SmartLight_Basic
# Description  : 스마트 가로등 코딩 키트 (기본)
# Author       : 손정인
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2022.02.08
# Reference    :
# Modified     : 2022.11.23 : YSY : 소스 클린징
# Modified     : 2022.12.16 : YSY : 조도값 수정, ledpin->led, 주석 수정
# Modified     : 2022.12.19 : YSY : 조도센서 입력 확인값 수정, 센서 임계값 추가. 주석수정
# Modified     : 2022.12.21 : YSY : 변수 명명법 통일
# Modified     : 2023.03.14 : PEJ : 주석 길이 수정
# Modified     : 2023.10.26 : PEJ : 녹색 LED 핀 변경
# *****************************************************************************************

# import
import time
from machine import Pin, time_pulse_us, ADC
from ETboard.lib.pin_define import *
from ETboard.lib.OLED_U8G2 import *

#------------------------------------------------------------------------------------------
# ETBoard 핀번호 설정
#------------------------------------------------------------------------------------------
# global variable
cds_pin  = ADC(Pin(A3))                            # 조도 센서
echo_pin = Pin(D8)                                 # 초음파 센서 수신부
trig_pin = Pin(D9)                                 # 초음파 센서 송신부                

blue_led  = Pin(D3)                                # 가로등 파란색 LED
green_led = Pin(D4)                                # 가로등 녹색 LED

cds_threshold = 800                                # 조도 센서 임계치
usw_threshold = 10                                 # 초음파 센서 임계치


#==========================================================================================
# setup
#==========================================================================================
def setup():
    trig_pin.init(Pin.OUT)                         # 초음파 센서 송신부 출력 모드 설정                     
    echo_pin.init(Pin.IN)                          # 초음파 센서 수신부 입력 모드 설정
    
    green_led.init(Pin.OUT)                        # 녹색 LED 출력 모드 설정
    blue_led.init(Pin.OUT)                         # 파란색 LED 출력 모드 설정
    
    cds_pin.atten(ADC.ATTN_11DB)                   # 조도 센서를 입력 모드 설정
    
    
#==========================================================================================
# main loop
#==========================================================================================
def loop():
    #--------------------------------------------------------------------------------------
    # 초음파 센서로 장애물과의 거리 구하기
    #--------------------------------------------------------------------------------------
    # 초음파 송신 후 수신부는 HIGH 상태로 대기
    trig_pin.value(LOW)
    echo_pin.value(LOW)
    time.sleep_ms(2)
    trig_pin.value(HIGH)
    time.sleep_ms(10)
    trig_pin.value(LOW)
    
    # echo_pin이 HIGH 를 유지한 시간 저장
    duration = time_pulse_us(echo_pin, HIGH)      
    
    # HIGH 였을 때 시간(초음파 송수신 시간)을 기준으로 거리를 계산
    distance = ((34 * duration) / 1000) / 2
    print("초음파 센서  : ", distance, "cm")
    
    #--------------------------------------------------------------------------------------
    # 조도 센서로 빛의 세기 구하기
    #--------------------------------------------------------------------------------------
    cds_value = cds_pin.read()                     # 조도 센서 입력 확인
    print(" 조도 센서  : ", cds_value)
    print("---------------------")
    
    #--------------------------------------------------------------------------------------
    # 조도 센서를 이용하여 어두우면 가로등의 녹색LED 켜기, 밝으면 끄기
    #--------------------------------------------------------------------------------------
    # 밝기에 따라 green_led 제어
    if( cds_value < cds_threshold ) :              # 조도 센서값이 cds_threshold 미만이면
        green_led.value(HIGH)                      # green_led 켜짐
    else :
        green_led.value(LOW)                       # green_led 꺼짐
    
    
    #--------------------------------------------------------------------------------------
    # 초음파 센서를 이용하여 장애물을 감지하여 파란 LED 켜기, 없으면 끄기
    #--------------------------------------------------------------------------------------
    # 장애물 감지 여부에 따라 blue_led 제어
    if( distance < usw_threshold ) :               # 초음파 센서값이 usw_threshold 미만이면
        blue_led.value(HIGH)                       # blue_led 켜짐
    else :
        blue_led.value(LOW)                        # blue_led 꺼짐
        
    time.sleep(0.5)                                


if __name__ == "__main__":
    setup()
    while True:
        loop()
        
#==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
#==========================================================================================