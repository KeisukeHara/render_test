from fastapi import FastAPI
from typing import Optional,List
from pydantic import BaseModel

class IntFutOpTrade(BaseModel):
    trade_id:str = None
    product_type:str = None
    future_type:str = None
    ccy:str = None
    strike:float = None
    call_put:str = None
    buy_sell:str = None
    amount:float = None

class TradeResponse(BaseModel):
    eval_date: str
    trade_list: List[IntFutOpTrade]=[]

class pv(BaseModel):
    trade_id:str = None
    pv:float = None

class CalcPvResponse(BaseModel):
    eval_date: str
    pv_list: List[pv]=[]
    trade_list: List[IntFutOpTrade]=[]


class CalcCondition(BaseModel):
    eval_date:str = None

class TradeCondition(BaseModel):
    eval_date:str = None

class MarketCondition(BaseModel):
    eval_date:str = None


app = FastAPI()

@app.get("/")
async def top():
    return {"message": "calc pv of interest future option trade."}

@app.post("/trade/get_trade/")
async def get_trade(cond: TradeCondition) -> TradeResponse:
    result = TradeResponse(eval_date=cond.eval_date)

    trade1 = IntFutOpTrade(trade_id="Ref001", product_type="IntFutOp", future_type="ON", ccy="JPY",
                          strike=99.7, call_put="C", buy_sell="B", amount=1000000)
    trade2 = IntFutOpTrade(trade_id="Ref002", product_type="IntFutOp", future_type="1M", ccy="JPY",
                          strike=99.5, call_put="P", buy_sell="B", amount=2000000)
    trade3 = IntFutOpTrade(trade_id="Ref003", product_type="IntFutOp", future_type="3M", ccy="USD",
                          strike=99.6, call_put="C", buy_sell="S", amount=3000000)

    result.trade_list.append(trade1)
    result.trade_list.append(trade2)
    result.trade_list.append(trade3)

    return result

@app.post("/market/get_market/")
async def get_market(cond: MarketCondition):
    result = {
        "ir": [
            {
                "ccy": "JPY",
                "rate": "TBD"
            },
            {
                "ccy": "USD",
                "rate": "TBD"
            }
        ],
        "int_fut_price": [
            {
                "ccy": "JPY",
                "future_type": "ON",
                "price": 99
            },
            {
                "ccy": "USD",
                "future_type": "3M",
                "price": 98
            }

        ]

    }

    return result


@app.post("/calc/calc_pv_all/")
async def calc_pv(cond: CalcCondition) -> CalcPvResponse:
    #基準日の明細、マーケット、マスタを取得
    #全明細のPVを計算
    result = CalcPvResponse(eval_date=cond.eval_date)
    
    result.pv_list.append(pv(trade_id="Ref001", pv=111.11))
    result.pv_list.append(pv(trade_id="Ref002", pv=222.22))
    result.pv_list.append(pv(trade_id="Ref003", pv=333.33))

    trade1 = IntFutOpTrade(trade_id="Ref001", product_type="IntFutOp", future_type="ON", ccy="JPY",
                          strike=99.7, call_put="C", buy_sell="B", amount=1000000)
    trade2 = IntFutOpTrade(trade_id="Ref002", product_type="IntFutOp", future_type="1M", ccy="JPY",
                          strike=99.5, call_put="P", buy_sell="B", amount=2000000)
    trade3 = IntFutOpTrade(trade_id="Ref003", product_type="IntFutOp", future_type="3M", ccy="USD",
                          strike=99.6, call_put="C", buy_sell="S", amount=3000000)

    result.trade_list.append(trade1)
    result.trade_list.append(trade2)
    result.trade_list.append(trade3)
    return result
