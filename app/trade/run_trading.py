from app.db.crud import CRUD


def run_trading(crud: CRUD):
    db = DBManager()
    # 현재 파라미터 읽기
    params = db.get_current_parameters()
    if not params:
        a_val, b_val, c_val = A_INIT, B_INIT, C_INIT
    else:
        a_val, b_val, c_val = params["a_value"], params["b_value"], params["c_value"]

    # (1) 매수
    candidate_stocks = get_candidate_stocks()
    daily_buy(db, candidate_stocks, a_val, b_val, c_val)

    # (2) 매도
    daily_sell(db, a_val, b_val, c_val)

    # (3) a,b,c 최적화 (예: 7일마다)
    last_update = get_last_param_update(db)
    if (datetime.datetime.now() - last_update).days >= ML_OPTIMIZE_INTERVAL_DAYS:
        new_a, new_b, new_c = optimize_abc(db)
        db.insert_parameters(new_a, new_b, new_c)

    db.close()
    return {"message": "자동매매 & 파라미터 최적화 실행 완료"}


def get_last_param_update(db: DBManager):
    db.cursor.execute("SELECT updated_at FROM parameters ORDER BY id DESC LIMIT 1")
    row = db.cursor.fetchone()
    if row:
        return row["updated_at"]
    else:
        return datetime.datetime.now() - datetime.timedelta(days=30)
