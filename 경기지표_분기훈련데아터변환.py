import pandas as pd
import calendar

# 파일 경로 설정
#file_path = '/content/drive/My Drive/stock_data/economic_indi.csv'
file_path = './economic_indi.csv'
# CSV 파일 읽어오기
df = pd.read_csv(file_path, encoding='cp949')

# 1행에 '월간' 또는 '신규'가 포함된 열을 식별합니다.
target_columns = []
col_cnt =0
for col in df.columns:
    #first_value = df[col].iloc[0]
    first_value = col
    condition = isinstance(first_value, str) and (('월간' in first_value) or ('신규' in first_value))
    #print(f"Column: {col}, First value: {first_value}, Condition: {condition}")
    if condition:
        target_columns.append(col)
        #target_columns.append(col_cnt)
    col_cnt = col_cnt+1
#print(f"Target columns: {target_columns}")
# target_columns에서 열 이름을 열 번호로 변환합니다.
#target_column_indices = [df.columns.get_loc(col) for col in target_columns]
#print(f"target_column_indices: {target_column_indices}")

# 식별된 열에 대해 1, 2, 3월 데이터를 합쳐 3월에, 4, 5, 6월 데이터를 합쳐 6월에, 7, 8, 9월 데이터를 합쳐 9월에, 10, 11, 12월 데이터를 합쳐 12월에 넣습니다.
for col in target_columns:
    for i in range(1, 13, 3):
        month_filter = df['Unnamed: 0'].str.contains(f'({"|".join([calendar.month_abbr[j] for j in range(i, i + 3)])})-', regex=True, case=False)
        #print('month_filter',month_filter)
        # DataFrame 복사
        df_copy = df.copy()
        # .str[:7] -> .str[:6] 으로 수정해야 합니다. Unnamed: 0 열이 MMM-YY 형식이므로 6자리까지만 그룹화해야 합니다.
        grouped_sum = df_copy.loc[month_filter, col].groupby(df_copy['Unnamed: 0'].str[4:]).sum()
        print('grouped_sum : ',grouped_sum)
        for date, value in grouped_sum.items():
            # date는 연도만 포함하고 있으므로, 월 정보를 포함하도록 수정해야 합니다.
            # 예를 들어, '15' 대신 'Jan-15', 'Feb-15', 'Mar-15'와 같이 월 정보를 포함해야 합니다.
            # 3, 6, 9, 12월에 해당하는 월 이름 약어를 사용하여 필터링합니다.
            target_month = calendar.month_abbr[i + 2]  # 3, 6, 9, 12월에 해당하는 월 이름 약어
            df_copy.loc[df_copy['Unnamed: 0'] == f'{target_month}-{date}', col] = value #.str.startswith(date)  ->  == f'{target_month}-{date}'

        # 원본 DataFrame에 변경 사항 반영
        df.loc[df_copy.index, col] = df_copy[col]


df_filtered = df[df['Unnamed: 0'].str.contains(r'(Mar|Jun|Sep|Dec)-', regex=True, case=False)]
print(df_filtered.head())
# 결과를 "economic_indi_processed.csv"라는 이름의 새 CSV 파일로 저장합니다.
df_filtered.to_csv("./economic_indi_quarterly_data.csv", index=False, encoding='cp949')