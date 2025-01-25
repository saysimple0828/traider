import os

# 예시: 환경 변수 또는 직접 기입
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "myuser",
    "password": "mypassword",
    "database": "trading_db"
}

# 토스증권 해외주식(가정) API 키 (실제 존재 여부 확인 필요)
TOSS_API_KEY = os.getenv("TOSS_API_KEY", "YOUR_TOSS_API_KEY")
TOSS_API_SECRET = os.getenv("TOSS_API_SECRET", "YOUR_TOSS_API_SECRET")

# 초기 파라미터
A_INIT = 0.1   # 0.1% (일간 수익률 임계)
B_INIT = 2.0   # 2%   (누적 수익률 임계)
C_INIT = 7     # 7일  (매도 재확인 주기)

# 하루 투자금 (예시)
DAILY_BUDGET_USD = 1000

# 환율 (가정). 실제로는 실시간/자동 수집 가능
USD_KRW = 1200

# 머신러닝/최적화 주기 (예: 1주일마다 a,b,c 재조정)
ML_OPTIMIZE_INTERVAL_DAYS = 7
