import csv
import re

# CSV 파일 불러오기
file_path = ''
output_path = ''

# 다섯 번째 열의 데이터를 처리하는 함수 정의
def process_string(s):
    # 문자열이 문자열이 아니면 (예: None) 패스
    if not isinstance(s, str):
        return s

    # <<로 시작하고 >가 연속으로 두 번 나오지 않고 한번만 나오는 경우 처리
    # > 하나를 추가하여 <<...>> 형태로 만듦
    if s.startswith('<<') and s.count('>') == 1:
        return s + '>'

    # 다른 경우 - 연속되는 두 개의 `>`를 고려한 패턴 처리
    def replace_match(match):
        substring = match.group(1)
        # 공백 및 특수 문자 제거
        substring = ''.join(ch for ch in substring if ch not in {'>', '<', ' '})
        return f"<<{substring}>>"

    # 정규 표현식을 사용하여 모든 <<...> ...> 형태를 찾아 처리
    processed_string = re.sub(r'<<([^>]*)>([^>]*)>', replace_match, s)

    return processed_string

# CSV 파일 읽고 처리하기
with open(file_path, mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)  # 헤더 추출
    rows = []

    for row in reader:
        # 다섯 번째 열 (인덱스 4)을 처리
        if len(row) > 4:  # 다섯 번째 열이 있는 경우에만 처리
            original_value = row[4]
            processed_value = process_string(original_value)
            row[4] = processed_value
        rows.append(row)

# 처리된 내용을 새로운 CSV 파일로 저장하기
with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(header)  # 헤더 작성
    writer.writerows(rows)  # 행들 작성

# 처리된 내용 출력 (처리된 행만 필터링하여 보여줌)
print("처리된 행의 비교 결과 (원본 vs 처리 후):")
with open(file_path, mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    next(reader)  # 헤더 건너뛰기
    original_rows = list(reader)

for original, modified in zip(original_rows, rows):
    if len(original) > 4 and original[4] != modified[4]:
        print(f"Original: {original[4]} | Processed: {modified[4]}")
