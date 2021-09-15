# 감정분석 기반 영화 추천
네이버 영화 리뷰 데이터를 통해 감정분석을 진행하고, 샘플 리뷰들의 긍정 리뷰 수에 따라 영화를 추천한다.

## 1. 감정분석
LSTM모델과 DNN 모델을 사용해 감정분석을 진행했다. 그 결과 두 모델 모두 테스트 데이터에서 85%의 정확도를 기록했다.
따라서 큰 차이가 없기 때문에 prediction에서 조금 더 빠른 DNN 모델을 사용했다.

사용한 데이터는 네이버 영화 리뷰를 크롤링하여 만든 [데이터](https://github.com/e9t/nsmc)를 사용했다. 

## 2. 웹앱 구성
영화 리뷰 100개를 가져와 감성분석을 하고, 긍정 리뷰가 60개 이상이면 추천, 40개 미만이면 비추, 그 사이라면 호불호 갈림으로 표시했다.

- 상영작
    - 현재 상영중인 영화 20개를 먼저 스크래이핑 하고 해당 리뷰를 분석하여 추천 여부를 보여준다.
    - 매일 같은 시간에 현재 상영중인 영화와 새로 달린 리뷰를 스크래이핑하여 업데이트한다.
- 검색
    - 검색하고 싶은 영화를 검색하면 해당 영화의 추천여부를 보여준다.
    - 현재는 검색을 했을때 DB에 없는 영화라면 리뷰 스크래이핑부터 감성분석까지 모두 진행한 후 결과가 나오기 때문에 3분 이상의 시간이 걸린다.
    - 그리고 네이버 영화 검색결과 중 맨 위의 영화를 가져오기 때문에 원하는 영화가 나오지 않을 수 있고, 미개봉 등의 이유로 리뷰가 없는 영화가 선택되어 멈추는 현상이 있음

- 로그인
    - 로그인 기능을 추가하여 로그인 한 사람의 검색기록 등을 추가
    - 아직 이부분은 구현하지 못함


## 3. 지난 프로젝트와 비교
- 지난번 기사 요약에서는 db 암호 등을 그대로 github에 노출했다. 이번에는 .env파일 중요 내용을 저장하고 github에는 올리지 않았다.
- trading_bot을 만들면서 (이때는 API token이 유출되면 절대 안되니까) 사용한 dotenv를 사용해서 github에 민감 정보를 올리지 않을 수 있었다.
- 역시 AWS를 통해 배포를 해보려 했지만, Free tier에서 GPU를 사용할 수 없어서 이번 프로젝트의 감성분석 부분을 실행할 수 없기 때문에 AWS에는 올리지 못했다.