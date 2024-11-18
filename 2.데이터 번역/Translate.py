import pandas as pd
from googletrans import Translator
import re
import time

translator = Translator()

def translate_text_batch(texts):
    """텍스트 리스트를 하나의 문자열로 병합하여 번역을 시도합니다."""
    if not texts:
        return []  # 빈 리스트가 들어온 경우 처리

    combined_text = "\n".join(texts)  # 텍스트를 개행 문자로 병합
    try:
        translated = translator.translate(combined_text, src='en', dest='ko')
        if translated and translated.text:
            return translated.text.split("\n")  # 개행 문자를 기준으로 분리
    except Exception as e:
        print(f"번역 오류: {e}")
        return None  

    return None

def convert_ko_to_cn(text):
    """한국어 텍스트를 특정 한자 코드 범위로 변환합니다."""
    converted_text = ""
    for char in text:
        utf8_val = ord(char)
        if 0xAC00 <= utf8_val <= 0xEA00:
            converted_char = chr(utf8_val - 0x3E00)
        else:
            converted_char = char
        converted_text += converted_char

    return converted_text

def split_text_into_four_parts(text):
    """긴 텍스트를 4등분으로 쪼갭니다."""
    quarter = len(text) // 4
    return text[:quarter], text[quarter:2 * quarter], text[2 * quarter:3 * quarter], text[3 * quarter:]

def process_csv(input_file, output_file, initial_batch_size=100):
    """CSV 파일의 5열만 번역하고 한자로 변환 후 저장합니다."""
    df = pd.read_csv(input_file, on_bad_lines='skip', encoding='utf-8', engine='python')
    total_rows = len(df)
    batch_size = initial_batch_size
    index = 0

    while index < total_rows:
        text_batch = []
        index_batch = []

        # 배치 크기만큼 텍스트 모으기
        while len(text_batch) < batch_size and index < total_rows:
            row = df.iloc[index]
            text = row.iloc[4]  # 다섯 번째 열의 텍스트 가져오기
            
            # 문자열이 아닌 값은 빈 문자열로 처리
            if not isinstance(text, str):
                text = ""  # 문자열이 아닌 경우 빈 문자열로 변환
            
            text_batch.append(text)
            index_batch.append(index)
            index += 1

        # 번역 시도
        translated_texts = translate_text_batch(text_batch)

        if translated_texts is None:
            # 번역 실패 시 배치 크기 줄이기
            if batch_size > 10:
                batch_size -= 10
            elif batch_size > 1:
                batch_size -= 1
            else:
                # 배치 크기가 1일 때도 번역 실패하면 텍스트를 4등분으로 나누기
                for i, text in enumerate(text_batch):
                    print(f"텍스트 너무 길어서 4등분 시도: {text}")
                    part1, part2, part3, part4 = split_text_into_four_parts(text)

                    # 쪼갠 텍스트 번역 시도
                    translated_part1 = translate_text_batch([part1])
                    translated_part2 = translate_text_batch([part2])
                    translated_part3 = translate_text_batch([part3])
                    translated_part4 = translate_text_batch([part4])

                    # 번역 성공 시 각 부분 합치기
                    if all([translated_part1, translated_part2, translated_part3, translated_part4]):
                        translated_text = (
                            translated_part1[0] +
                            translated_part2[0] +
                            translated_part3[0] +
                            translated_part4[0]
                        )
                    else:
                        # 여전히 실패하는 경우 원문 그대로 사용
                        translated_text = text

                    # 번역된 텍스트 한자로 변환 후 DataFrame 업데이트
                    converted_text = convert_ko_to_cn(translated_text)
                    df.iat[index_batch[i], 4] = converted_text

                    # 디버그 출력
                    print(f"원문: {text}")
                    print(f"번역된 텍스트: {translated_text}")
                    print(f"한자로 변환된 텍스트: {converted_text}")
                    print('-' * 50)

                # 배치 크기 초기화 후 다음으로 넘어가기
                batch_size = initial_batch_size
                continue

            print(f"번역 실패로 배치 크기를 줄입니다. 새로운 배치 크기: {batch_size}")

            # 인덱스를 다시 실패한 배치의 시작으로 되돌림
            index -= len(text_batch)
            continue  # 실패한 부분부터 다시 시도

        # 번역 성공한 텍스트들 처리
        for i, translated_text in enumerate(translated_texts):
            # 번역된 텍스트 한자로 변환 후 DataFrame 업데이트
            converted_text = convert_ko_to_cn(translated_text)
            df.iat[index_batch[i], 4] = converted_text

            # 디버그 출력
            print(f"원문: {text_batch[i]}")
            print(f"번역된 텍스트: {translated_text}")
            print(f"한자로 변환된 텍스트: {converted_text}")
            print('-' * 50)

        print(f"진행 상황: {index}/{total_rows} 행 처리 완료.")
        
        # 성공 후 배치 크기 초기화
        batch_size = initial_batch_size
        

    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"처리가 완료되었습니다. 결과는 {output_file}에 저장되었습니다.")

# 파일 경로
input_csv = ''
output_csv = ''

# 번역 및 변환 작업 실행
process_csv(input_csv, output_csv)
