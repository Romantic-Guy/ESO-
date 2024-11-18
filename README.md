# EsoTransKrLang

안녕하세요 kr.lang 한글 번역 입니다.
본 코드는 번역을 위한 참고용도입니다.


준비물
1. en.lang , kr.lang(기존 kr.lang), EsoExtractdata

순서
1. EsoExtractData를 활용하여 kr.lang에는 없지만 en.lang에 있는 데이터(csv) 추출 (추출 데이터를 Diff.lang.csv 라고 가명 짓겠음.)
2. Diff.lang.csv파일을 '번역 전 데이터 전처리'폴더 내 파이썬 코드를 통해 가공 (폴더 내 파이썬 코드에서 경로를 지정하고 순서대로 실행)
3. Diff.lang.csv파일을 '데이터 번역'폴더 내 파이썬 코드를 통해 통해 영어->한글->한문으로 가공 (폴더 내 파이썬 코드에서 경로를 지정하고 순서대로 실행)
4. Diff.lang.csv파일을 '번역 후 데이터 전처리'폴더 내 파이썬 코드를 통해 가공 (폴더 내 파이썬 코드에서 경로를 지정하고 순서대로 실행)
5. Diff.lang.csv파일과 kr.lang파일을 '데이터 정리'폴더 내 파이썬 코드를 통해 합치고 가공(폴더 내 파이썬 코드에서 경로를 지정하고 순서대로 실행)
6. EsoExtractData를 통해 다시 csv를 다시 Lang으로 저장
7. 기존 GameData내에 kr.lang을 번역한 kr.lang으로 교체



파이썬으로 무언가 작업해본게 처음이라 매우 미숙합니다.(데이터 전처리도 미숙함)
u45나 u46때 좀더 다듬고 GUI도 써보면서 좀더 쉽게 할 수 있도록 해보겠습니다.
