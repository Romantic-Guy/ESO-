import pandas as pd
import re

#번역 전 전처리1


# CSV 파일 불러오기
file_path = ''
data = pd.read_csv(file_path, on_bad_lines='skip', encoding='utf-8', engine='python')

# 특정 열의 텍스트 정리 함수 정의
def clean_text(text):
    if isinstance(text, str):
        # '\n' 또는 '\ n' 같은 탈출 문자 제거
        text = re.sub(r'\\\s*n', '', text)
        # 캐럿(^) 문자 제거
        text = re.sub(r'\^', '', text)
        # |cXXXXXX 색상 코드 제거
        text = re.sub(r'\|c[0-9A-Fa-f]{6}', '', text)
        # |r 리셋 코드 제거
        text = text.replace('|r', '')
        # 마침표, 물음표, 느낌표 뒤에 공백이 없는 경우 공백 추가
        text = re.sub(r'([.?!])(\S)', r'\1 \2', text)
    return text

# 5번째 열(index 4)에 함수 적용
data.iloc[:, 4] = data.iloc[:, 4].apply(clean_text)

# 정리된 데이터 저장
output_path = ''
data.to_csv(output_path, index=False)  # 명시적인 경로로 파일 저장

# 데이터 확인을 위해 일부 출력
print(data.head())  # 데이터 출력하여 확인
