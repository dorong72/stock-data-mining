import pyautogui
import time
import pandas as pd
import sys

# 주식 종목코드를 문자열리스트로 받아서 분기 데이타를 추출하는 함수
def save_stock_quad_data(stock_codes):
    # 퀀트킹 프로그램이 실행 중이어야 합니다.
    # 프로그램 창을 활성화합니다.
    pyautogui.getWindowsWithTitle('퀀트킹 한국')[0].activate()
    time.sleep(5)
    stock_len = len(stock_codes)
    stock_cnt = 0
    for code in stock_codes:
        # 종목코드 입력 필드로 이동하여 클릭
        # for test
        #if stock_cnt == 5:
        #    break

        stock_cnt += 1
                print("종목수 : " , stock_len ,"/" ,stock_cnt)
        print("종목 코드 이동 : ",code)
        pyautogui.click(x=168, y=95)  # 좌표_x와 좌표_y를 실제 위치로 변경하세요
        pyautogui.hotkey('ctrl', 'a')  # 기존 입력 내용 모두 선택
        pyautogui.typewrite(code)  # 종목코드 입력

        # 현황보기 버튼 클릭
        print("현황보기 이동")
        pyautogui.click(x=388, y=94)  # 실제 위치로 변경하세요
        time.sleep(2)
        # 파일로 내려받기 버튼 클릭
        print("파일로 내려받기 이동")
        pyautogui.click(x=1083, y=97)  # 실제 위치로 변경하세요

        # 파일 다운로드 대기 (필요에 따라 조정)
        time.sleep(3)

        # 저장하기 버튼 클릭
        print("저장하기 이동")
        pyautogui.click(x=1018, y=779)  # 실제 위치로 변경하세요
        time.sleep(1)
        # 폴더이동 아니요 버튼 클릭
        print("폴더이동 아니오")
        pyautogui.click(x=1398, y=885)  # 실제 위치로 변경하세요
        time.sleep(1)

def get_stock_codes(stock_file_path):
    # CSV 파일을 읽어들입니다.
    df = pd.read_csv(stock_file_path)

    # 첫 번째 열의 이름을 가져옵니다.
    first_column_name = df.columns[0]
    print(df[first_column_name])
    # 첫 번째 열의 1행부터 각 셀의 값에서 첫 번째 문자 'A'를 제거합니다.
    # 결과를 저장할 리스트를 생성합니다.
    result = []
    for value in df[first_column_name][0:]:  # 1행부터 시작하도록 변경
        if value.startswith('A'):
            result.append(value[1:])
        else:
            result.append(value)

    # 결과를 출력합니다.
    return result

import os
import shutil

def move_csv_file(target_dir):
    # 현재 디렉토리
    current_dir = os.getcwd()

    # 현재 디렉토리의 모든 파일을 순회
    for filename in os.listdir(current_dir):
        # 파일 확장자가 .csv인 경우에만 이동
        if filename.endswith('.csv'):
            # 현재 디렉토리에 있는 파일의 전체 경로
            source_path = os.path.join(current_dir, filename)
            # 이동할 디렉토리에 있는 파일의 전체 경로
            target_path = os.path.join(target_dir, filename)

            # 파일 이동
            shutil.move(source_path, target_path)

print("주의 pycharm을 관리자 권한으로 실행 시켜야 마우스 control이 정상 동작합니다")
stock_file_path = './stock-data/korea/kospi_100.csv'
print("추출시작 : ",stock_file_path)
stock_codes= get_stock_codes(stock_file_path)
print(stock_codes)
save_stock_quad_data(stock_codes)
target_dir = 'C:\antonio\homework-AI\openai-and-upbit\kiwoom-크롤링\stock-data\kospi'
move_csv_file(target_dir)
#테스트 때는 강제 종료
sys.exit()

stock_file_path = './stock-data/korea/kodaq_100.csv'
print("추출시작 : ",stock_file_path)
stock_codes= get_stock_codes(stock_file_path)
print(stock_codes)
save_stock_quad_data(stock_codes)
target_dir = './stock-data/korea/kodaq/'
move_csv_file(target_dir)
print("작업 완료")