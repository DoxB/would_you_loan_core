from fastapi import FastAPI
from function import *

app = FastAPI()

####################################
###   실시간 지표 수치 크롤링    ###
####################################

@app.get("/total")
async def total_index():
    return {
        "cd_rate": await cd_crawling(),
        "cofix_rate": await cofix_crawling(),
        "financial_rate": await financial_crawling(),
        "trade_rate": await trade_crawling()
    }

@app.get("/cd")
async def cd_index():
    return {"rate": await cd_crawling()}

@app.get("/cofix")
async def cofix_index():
    return {"rate": await cofix_crawling()}

@app.get("/financial")
async def financial_index():
    return {"rate": await financial_crawling()}

@app.get("/trade")
async def trade_index():
    return {"rate": await trade_crawling()}











