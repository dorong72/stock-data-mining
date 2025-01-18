import pandas as pd
import os
import glob

def get_csv_file_paths(directory):
    """
    특정 디렉토리 안에 있는 모든 csv 파일을 순차적으로 읽어서 file_path 변수에 넣어주는 함수입니다.

    Args:
        directory: csv 파일들이 있는 디렉토리 경로입니다.

    Returns:
        csv 파일들의 전체 경로를 담은 리스트입니다.
    """
    file_paths = []
    for filename in glob.glob(os.path.join(directory, '*.csv')):
        file_paths.append(filename)
    return file_paths


def transfer_data_and_label(file_path):
    dir_name = os.path.basename(file_path).split("_")[0]
    new_data_filename = dir_name + "_data.csv"
    new_label_filename = dir_name + "_label.csv"
    # 하위 디렉토리 생성
    new_dir_path = os.path.join(directory, dir_name)
    os.makedirs(new_dir_path, exist_ok=True)

    #df = pd.read_csv(file_path, encoding='utf-8-sig',encoding_errors='ignore',on_bad_lines='skip', header=None,usecols=range(55))
    df = pd.read_csv(file_path, encoding='utf-8-sig', header=None,usecols=range(55))
    # 1열부터 14열까지 삭제
    df = df.drop(df.columns[0:13], axis=1).reset_index(drop=True)

    # 1행부터 4행까지 삭제
    df = df.drop(df.index[0:4]).reset_index(drop=True)

    # 모든 열에 값이 없는 행 삭제
    df = df.dropna(how='all')

    # 10행부터 22행까지 삭제
    df = df.drop(df.index[9:22])  # 인덱스는 0부터 시작하므로 8부터 21까지 지정

    # 2번째부터 10번째 열까지의 값을 비교하여 중복된 행을 찾습니다.
    # keep='first'는 처음 나타난 중복 행을 유지하고 나머지를 삭제하도록 지정합니다.
    duplicate_rows = df.duplicated(subset=df.columns[4:13], keep='first')
    # 중복된 행을 삭제합니다.
    df = df[~duplicate_rows]

    # 5번째부터 10번째 열까지의 값을 비교하여 중복된 행을 찾습니다.
    # keep='first'는 처음 나타난 중복 행을 유지하고 나머지를 삭제하도록 지정합니다.
    duplicate_rows = df.duplicated(subset=df.columns[6:15])
    # 중복된 행을 삭제합니다.
    df = df[~duplicate_rows]

    # '주가 & 영업' 값을 가진 행 찾기
    target_row_index = df[df.apply(lambda row: row.astype(str).str.contains('주가 & 영업').any(), axis=1)].index
    # 행 삭제
    df = df.drop(target_row_index)

    # '매출액&판관' 값을 가진 행 찾기
    target_row_index = df[df.apply(lambda row: row.astype(str).str.contains('매출액&판관').any(), axis=1)].index
    # 행 삭제
    df = df.drop(target_row_index)

    # 1행 삭제
    #df = df.drop(df.index[0])

    # 1열 삭제
    df = df.drop(df.columns[0], axis=1)
    # 수정된 데이터프레임을 CSV 파일로 저장
    data_file_path = new_dir_path +'\\' + new_data_filename
    label_file_path = new_dir_path +'\\' + new_label_filename
    df.to_csv(data_file_path, index=False, encoding='utf-8-sig')

    df = pd.read_csv(data_file_path, encoding='utf-8-sig')
    # 행과 열 반전
    df = df.transpose()

    # 수정된 데이터프레임을 CSV 파일로 저장
    df.to_csv(data_file_path, index=False, encoding='utf-8-sig')

    print(f"파일이 {file_path}에 저장되었습니다.")

    # 원본 CSV 파일 경로
    #original_file = './SK하이닉스_재무차트_20250118_123349_ai_data.csv'

    # 새로운 CSV 파일 경로
    #new_file = './SK하이닉스_재무차트_20250118_123349_ai_label.csv'

    # pandas를 사용하여 CSV 파일 읽기
    df = pd.read_csv(data_file_path, encoding='utf-8-sig')

    # 1열과 8열 데이터 추출
    column1 = df.iloc[:, 0].values  # 1열 데이터 (인덱스는 0부터 시작)
    column8 = df.iloc[:, 7].values  # 8열 데이터 (인덱스는 0부터 시작)

    # 새로운 데이터프레임 생성
    new_df = pd.DataFrame({'Column1': column1, 'Column8': column8})

    # 새로운 CSV 파일로 저장
    new_df.to_csv(label_file_path, index=False, encoding='utf-8-sig', header=False)

    # 원본 데이터프레임에서 8열 삭제 (선택 사항)
    df = df.drop(df.columns[7], axis=1)

    # 수정된 원본 데이터프레임 저장 (선택 사항)
    df.to_csv(data_file_path, index=False, encoding='utf-8-sig')

# 예시: 'C:/antonio/homework-AI/openai-and-upbit/kiwoom-크롤링/stock-data/korea' 디렉토리의 모든 csv 파일 경로를 가져옵니다.
directory = r'C:/antonio/homework-AI/openai-and-upbit/kiwoom-크롤링/stock-data/korea/kospi'
csv_file_paths = get_csv_file_paths(directory)

# 결과를 출력합니다.
for file_path in csv_file_paths:
    transfer_data_and_label(file_path)