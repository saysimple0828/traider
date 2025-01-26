from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, JSONResponse
import plotly.express as px
import plotly

from app.api.error import Exception404, Exception500
from app.db.session import get_crud
from app.utils.logger import make_logger
from app.db.crud import CRUD

router = APIRouter(prefix="/dashboard")

logger = make_logger(__name__)


@router.get("/")
def dashboard():
    html = """
    <h1>Alpaca 해외주식 자동매매 대시보드</h1>
    <ul>
      <li><a href="/dashboard">종목별 수익률 차트</a></li>
      <li><a href="/api/symbol_profit">JSON: 종목별 평균 수익률</a></li>
    </ul>
    """
    return HTMLResponse(html)


@router.get("/show")
def dashboard(crud: CRUD = Depends(get_crud)):
    
    db = DBManager()
    db.cursor.execute("""
        SELECT symbol, AVG(profit_rate) as avg_profit
        FROM trades
        WHERE side='SELL'
        GROUP BY symbol
    """)
    rows = db.cursor.fetchall()
    db.close()

    if not rows:
        return HTMLResponse("<h2>매도된 종목이 없어 차트를 표시할 수 없습니다.</h2>")

    symbols = [r["symbol"] for r in rows]
    avg_profit = [float(r["avg_profit"]) for r in rows]

    fig = px.bar(x=symbols, y=avg_profit, labels={"x": "Symbol", "y": "Avg Profit Rate(%)"},
                 title="Symbol-wise Average Profit Rate (SELL basis)")
    chart_html = plotly.io.to_html(fig, full_html=False)

    html = f"""
    <h1>종목별 평균 매도 수익률</h1>
    {chart_html}
    <p><a href="/">[메인]</a></p>
    """
    return HTMLResponse(html)

@router.get("/list", response_model=list[Preset])
def get_preset_by_pagination(
    crud: CRUD = Depends(get_crud), *, offset: int = 0, limit: int = 10
):
    res = crud.preset.get_by_pagination(offset=offset, limit=limit)

    return res


@router.post("/create", response_model=Preset)
def create_preset(preset_create: PresetCreate, *, crud: CRUD = Depends(get_crud)):
    return crud.preset.create_preset(preset_create)


@router.put("/update", response_model=Preset)
def update_preset(preset_update: PresetUpdate, *, crud: CRUD = Depends(get_crud)):
    return crud.preset.update_preset(preset_update)


@router.delete("/delete", response_model=Preset)
def delete_presets(id: int, *, crud: CRUD = Depends(get_crud)):

    return crud.preset.delete(id=id)
