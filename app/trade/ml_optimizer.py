import datetime
import itertools
from db_manager import DBManager

def optimize_abc(db: DBManager):
    """
    과거 매매 데이터(trades)를 참고해서 (a,b,c) 최적 파라미터 탐색 (단순 예시)
    """
    candidate_a = [0.05, 0.1, 0.2]
    candidate_b = [1.0, 2.0, 5.0]
    candidate_c = [3, 5, 7, 10]

    best_params = (0.1, 2.0, 7)
    best_score = -9999

    cutoff = datetime.datetime.now() - datetime.timedelta(days=30)
    # 실제로는 과거 30일 매매 내역 불러와서 "평균 수익률" 등 계산 → 시뮬레이션
    db.cursor.execute("""
        SELECT AVG(profit_rate) AS avg_profit
        FROM trades
        WHERE trade_date >= %s
    """, (cutoff,))
    row = db.cursor.fetchone()
    baseline = row["avg_profit"] if row and row["avg_profit"] else 0

    # 매우 단순한 점수함수(데모)
    for a_val, b_val, c_val in itertools.product(candidate_a, candidate_b, candidate_c):
        score = baseline
        score += b_val * 0.3
        score -= a_val * 0.2
        score -= abs(c_val - 7) * 0.1

        if score > best_score:
            best_score = score
            best_params = (a_val, b_val, c_val)

    return best_params
