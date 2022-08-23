# 실시간 정보의 시각화 


## main.ipynb
현재 네이버시그널(https://www.signal.bz/)에서 제공하는 실시간 검색어
pororo를 활용하여 이미지로표현하기에 유의미한 키워드를 찾고 기사의 내용을 

## scrap.py
- 웹에서 데이터를 스크래핑하는 함수들을 담은 py main에서 실시간 정보를 가지고오는데에 사용
- 상세 내용은 파일내에 주석으로 

## arange.py
- 크롤링 - 세그멘테이션을 거친 이미지들을 콜라주의 형태로 배치시에 사용한 함수들을 담은 py파일
- 상세 내용은 파일내에 주석으로 작성

## seg.py
- 이미지를 기학습한 모델로 세그멘테이션하고 후처리를 거친이미지를 리턴하는 함수 및 이미지간 구분을위한 테두리를 생성하는 함수를 담은 py파일
- 상세 내용은 파일내에 주석으로 

## segmentation folder - human segmentation model에 사용한 ~
- deeplabV3+ 모델을 학습하는데에 사용했던 ipynb파일들
- visualization.ipynb : 학습결과를 시각화한 파일
- sample_image : sampleimage들과 그 결과

- [Crowd Instance-level Human Parsing Dataset](https://arxiv.org/abs/1811.12596) 을 사용하여 약 50000개의 sementic level의 사람 이미지를 학습함
- [데이터 링크](https://drive.google.com/uc?id=1B9A9UCJYMwTL4oBEo4RZfbMZMaZhKJaz)
