import pandas as pd
import os

# 1. 경제지표 분기별 데이터 읽기
economic_data = pd.read_csv("./economic_indi_quarterly_data.csv", encoding='cp949')

# 2. 'stock-data/korea/kospi' 아래의 하위 디렉토리 목록 가져오기
kospi_dir = "./stock-data/korea/kospi"
sub_dirs = [d for d in os.listdir(kospi_dir) if os.path.isdir(os.path.join(kospi_dir, d))]

# 3. 각 하위 디렉토리별로 파일 처리
for sub_dir in sub_dirs:
    stock_file_path = os.path.join(kospi_dir, sub_dir, f"{sub_dir}_data.csv")
    quarterly_file_path = os.path.join(kospi_dir, sub_dir, f"{sub_dir}_quarterly_data.csv")

    try:
        # 주식 데이터 파일 읽기
        stock_data = pd.read_csv(stock_file_path, encoding='utf-8-sig')

        # 경제지표 데이터 중에서 필요한 열 선택 (2열부터 마지막 열까지)
        economic_data_subset = economic_data.iloc[:, 1:]  # 2열부터 마지막 열까지 선택

        # 두 데이터프레임 병합 (주식 데이터 마지막 열에 경제지표 데이터 추가)
        #merged_data = pd.concat([stock_data, economic_data_subset], axis=1)
        # 마지막 행 저장
        economic_data_last_row = economic_data_subset.iloc[-1].to_frame().T
        # 두 데이터프레임 병합 (stock_data의 2번째 행부터 economic_data_subset의 1번째 행부터)
        economic_data_subset = economic_data_subset.shift(1)
        # 마지막 행 추가
        economic_data_subset = pd.concat([economic_data_subset, economic_data_last_row], ignore_index=True)
        merged_data = pd.concat([stock_data, economic_data_subset], axis=1)

        #결측치 제거
        #merged_data = merged_data.dropna()
        # 새로운 파일로 저장
        merged_data.to_csv(quarterly_file_path, index=False, encoding='utf-8')

        print(f"{quarterly_file_path} 저장 완료")

    except FileNotFoundError:
        print(f"{stock_file_path} 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"{stock_file_path} 처리 중 오류 발생: {e}")

print("모든 파일 처리 완료")