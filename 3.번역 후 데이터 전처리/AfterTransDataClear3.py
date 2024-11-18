import pandas as pd
import re

# CSV 파일 불러오기
file_path = ''  # 여기에 CSV 파일 경로를 입력
data = pd.read_csv(file_path)


def process_text(text):
    if pd.isnull(text):
        return text

    # '!'로 시작하면 제거
    text = re.sub(r'^!', '', text)

    # 문장부호 뒤에 공백 추가
    return re.sub(r'([.?!])(?=\S)', r'\1 ', text)


# 5번째 열 데이터를 가져와서 처리
fifth_column_name = data.columns[4]  # 5번째 열 이름 가져오기
data[fifth_column_name] = data[fifth_column_name].apply(process_text)

# 결과를 CSV로 저장
output_path = ''  # 여기에 출력 파일 경로를 입력
data.to_csv(output_path, index=False)
