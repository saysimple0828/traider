# 해외 주식 자동매매 & 대시보드 예시 (FastAPI + MySQL)

이 프로젝트는 **해외 주식 자동매매 로직**과 **간단한 웹 대시보드**를 구현한 예시입니다.

---

## 프로젝트 구조

auto_trading_system/ ├── main.py # FastAPI 웹서버 (대시보드), 자동매매 로직(예시) ├── config.py # DB 접속 정보, API 키, 초기 파라미터(a,b,c 등) ├── data_fetcher.py # 종목 데이터(가격, 수익률 등) 수집 (가상 예시) ├── strategy.py # 매수/매도 전략 (규칙 1~6) ├── ml_optimizer.py # 머신러닝/백테스트로 a,b,c 최적화 ├── db_manager.py # MySQL 연동 (테이블 생성, 매매기록, 보유현황) ├── requirements.txt # 필요한 라이브러리 목록 └── README.md # 안내 문서

markdown
복사
편집

---

## 주요 기능

1. **자동매매 (매일 매수 & 조건부 매도)**
    - 소수점 매매(가정)로 금액 기준 매수
    - a%·b% 조건 충족 시 수익 실현 매도 + c일 주기 재확인
2. **MySQL DB 기록**
    - `trades` (매수/매도 내역), `holdings` (보유현황), `parameters` (a,b,c 히스토리)
3. **머신러닝(최적화)**
    - 과거 매매 데이터를 이용해 a,b,c 자동 업데이트
4. **FastAPI 대시보드**
    - `/dashboard` 에서 종목별 수익률 차트
    - `/api/symbol_profit` 으로 JSON 데이터 제공

---

## 설치 및 실행

1. **사전 준비**
    - Python 3.9 이상
    - MySQL 서버
2. **라이브러리 설치**
    ```bash
    pip install -r requirements.txt
    환경 설정
    config.py 수정 (DB_CONFIG, TOSS_API_KEY, 등)
    초기 a,b,c 값 (예: A_INIT=0.1, B_INIT=2.0, C_INIT=7)
    DB 테이블 생성
    main.py 실행 시 @on_event("startup") 에서 테이블 자동 생성
    서버 실행
    bash
    복사
    편집
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    브라우저에서 http://localhost:8000 접속
    사용 방법
    자동매매 로직은 예시로 main.py에 포함되어 있으나,
    실제 운영에서는 cron_daily.py 같은 별도 스크립트를 만들어
    매일/정기적으로 매수·매도를 실행 (DB에 기록)
    대시보드
    http://<서버주소>:8000/dashboard : 종목별 평균 수익률 그래프
    http://<서버주소>:8000/api/symbol_profit : JSON 응답
    확장 아이디어
    실제 해외 주식 API 연동
    토스증권(해외주식 소수점 매매 가능 시) 또는 Alpaca, IBKR 등
    실시간 데이터 수집
    Yahoo Finance, Polygon.io, Alpha Vantage, WebSocket 등
    백테스트/머신러닝 고도화
    a,b,c 외에도 다양한 파라미터(종목 선택, 리스크 관리) 최적화
    대시보드 추가 기능
    보유 종목 현황, 누적 손익 그래프, 파라미터 변화 추적
    주의사항
    이 예시는 데모용이며, 실제 투자 전 충분한 검증이 필요합니다.
    API 사용 가능 여부 및 해외주식 소수점 매매 규정 확인 필수.
    투자 리스크와 금융 규제, 세금(해외주식 양도세, 환전 수수료 등)을 반드시 고려하세요.
    개발 과정에서 보안(API 키, 비밀번호 등)에도 유의해야 합니다.
    라이선스
    이 프로젝트 예시는 MIT License 등을 적용 가능하며,
    사용에 따른 책임은 전적으로 사용자에게 있습니다.
    복사
    편집
    ```
