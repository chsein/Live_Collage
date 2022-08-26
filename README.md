# 실시간 정보의 시각화 

모든 학습 및 파일은 Google Colab Pro + 환경에서 구동되도록 구현하였음


![시연](https://user-images.githubusercontent.com/102151612/186908419-2406ee04-3d4b-4944-9324-09ff0323daea.png)


- 카드뉴스의 형식으로 기사의 타이틀과 요약문제공
- 왼쪽 콜라주에 마우스를 오버하면 우측 기사가 

## main.ipynb



![도식화](https://user-images.githubusercontent.com/102151612/186887076-ec0e6c2e-e211-4c57-9603-30408e2275f9.png)


1. 현재 [네이버시그널](https://www.signal.bz/) 에서 제공하는 실시간 검색어를 스크래핑

2. SENTENCE EMBEDDING -> cossine similarity로 대표기사 선정

3. 대표 기사를 이용하여 이슈키워드 도출

4. 대표 기사의 내용을 요약

5. 3에서 찾은 키워드의 이미지를 나무위키 (인물의 프로필사진 또는 단체의 로고를 고해상도로 제공)에서 스크랩

6. 레이아웃 알고리즘으로 콜라주진행

7. 위 결과물들을 web으로 전송

* 상세내용은 파일내에 주석으로 작성

## scrap.py

- 웹에서 데이터를 스크래핑하는 함수들을 담은 py main에서 실시간 정보를 가지고오는데에 사용

- 상세 내용은 파일내에 주석으로 작성

## arange.py

- 크롤링 - 세그멘테이션을 거친 이미지들을 콜라주의 형태로 배치시에 사용한 함수들을 담은 py파일

- 상세 내용은 파일내에 주석으로 작성

## seg.py

- 이미지를 기학습한 모델로 세그멘테이션하고 후처리를 거친이미지를 리턴하는 함수 및 
  이미지간 구분을 위한 테두리를 생성하는 함수를 담은 py파일

- 상세 내용은 파일내에 주석으로 작성

## segmentation folder - human segmentation model에 사용한 ~

![image](https://user-images.githubusercontent.com/102151612/186291825-5ae6f6d2-db7a-4b5b-b0f5-e3d3ce73e58c.png)

- deeplabV3+ 모델을 학습하는데에 사용했던 ipynb파일들

- visualization.ipynb : 학습결과를 시각화한 파일

- sample_image : sampleimage들과 그 결과

- training code에 대한 주석은 1. DLv3_base.ipynb에 모두 작성

- weight는 깃용량이 제한으로 구글 드라이브로 공유 [weight](https://drive.google.com/file/d/1ZfHykt-hw3qDvk8GV2qfeGooNc6fu2qx/view?usp=sharing)

- [Crowd Instance-level Human Parsing Dataset](https://arxiv.org/abs/1811.12596) 을 사용하여 약 50000개의 sementic level의 사람 이미지를 학습함
- [데이터 링크](https://drive.google.com/uc?id=1B9A9UCJYMwTL4oBEo4RZfbMZMaZhKJaz)
