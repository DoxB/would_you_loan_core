import httpx
from bs4 import BeautifulSoup

### CD 금리
async def cd_crawling():
    url = 'https://finance.naver.com/marketindex/'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            index = soup.select_one('#marketindex_aside > div:nth-child(1) > table:nth-child(2) > tbody > tr:nth-child(1) > td:nth-child(2)')
            return index.get_text().strip()
        else:
            return "unknown"

### 코픽스
async def cofix_crawling():
    url = 'https://finance.naver.com/marketindex/'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            index = soup.select_one('#marketindex_aside > div:nth-child(1) > table:nth-child(2) > tbody > tr:nth-child(6) > td:nth-child(2)')
            return index.get_text().strip()
        else:
            return "unknown"

### 금융채 5년
async def financial_crawling():
    url = 'https://www.nhfire.co.kr/loan/retrieveLoanBaseRateAnnounce.nhfire'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            index = soup.select_one('#frm > div:nth-child(2) > table > tbody > tr:nth-child(4) > td:nth-child(2)')
            return index.get_text().strip()
        else:
            return "unknown"

### 부동산 매매지수
async def trade_crawling():
    url = 'https://kosis.kr/visual/eRegionJipyo/themaJipyo/eRegionJipyoThemaJipyoView.do?themaId=A_01_04&menuThemaId=A_01_04_02&jipyoId=5711_7188&jipyoNm=&graphTypeGbn=THEMA&statId=&regionChkVal=00%40&chartGbn=DTypeChart&selectPrdDe=&themaGbn=subjectJipyo&detailJipyoId=&themaGbnMenu=subjectJipyo&chooseYm=&jipyo1PrdDe=064d864d8&AreaChoiceCombo=A_01_04'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            index = soup.select_one('#mapTotalValSpanAll > strong')
            return index.get_text().strip()
        else:
            return "unknown"
