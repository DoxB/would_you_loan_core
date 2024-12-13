import asyncio
from fastapi import FastAPI
from items import QuestionRequest, KeywordRequest
from functions import retriever, augmented, generation, filter_answer, tavily_search, augmented_tavily, retriever_local
from langchain.schema import Document

app = FastAPI()

SIMILARITY_THRESHOLD_LOW = 0.4
SIMILARITY_THRESHOLD_HIGH = 0.6

@app.post("/rag")
async def rag_service(request: QuestionRequest):
    user_id = request.user_id
    user_question = request.user_question.strip()

    # 특정 질의 처리
    if user_question == "오늘 날씨는 어때?" or "날씨" in user_question:
        await asyncio.sleep(1)
        final_answer = "부동산 관련 뉴스 기사 질문을 해주시길 바랍니다."
        final_answer = filter_answer(final_answer)
        return {"user_id": user_id, "answer": final_answer}

    if user_question == "욕해봐" or "욕" in user_question:
        await asyncio.sleep(1)
        final_answer = "부동산 관련 뉴스 기사 질문을 해주시길 바랍니다."
        final_answer = filter_answer(final_answer)
        return {"user_id": user_id, "answer": final_answer}

    if user_question == "어디서 사는게 좋아?" or "사는게 좋아" in user_question:
        # 1초 지연 후 Tavily 검색 및 LLM 응답
        await asyncio.sleep(1)
        tavily_results = tavily_search(user_question)
        text = augmented_tavily(user_question, tavily_results)
        answer = generation(text)
        answer = filter_answer(answer)
        return {"user_id": user_id, "answer": answer}

    # 그 외 질의에 대해 벡터 검색
    results = retriever(user_question, 1)
    if not results:
        await asyncio.sleep(1)
        final_answer = "부동산 관련 뉴스 기사 질문을 해주시길 바랍니다."
        final_answer = filter_answer(final_answer)
        return {"user_id": user_id, "answer": final_answer}

    doc, score = results[0]

    await asyncio.sleep(1)
    if score <= SIMILARITY_THRESHOLD_LOW:
        # 0.4 이하
        final_answer = "부동산 관련 뉴스 기사 질문을 해주시길 바랍니다."
        final_answer = filter_answer(final_answer)
        return {"user_id": user_id, "answer": final_answer}
    elif score <= SIMILARITY_THRESHOLD_HIGH:
        # 0.4 ~ 0.6: Tavily 검색
        tavily_results = tavily_search(user_question)
        text = augmented_tavily(user_question, tavily_results)
        answer = generation(text)
        answer = filter_answer(answer)
        return {"user_id": user_id, "answer": answer}
    else:
        # 0.6 초과: RAG 파이프라인
        text = augmented(user_question, doc)
        answer = generation(text)
        answer = filter_answer(answer)
        return {
            "user_id": user_id,
            "answer": answer,
            "title": doc.metadata.get('title', ''),
            "article_date": doc.metadata.get('article_date', ''),
            "company": doc.metadata.get('company', ''),
            "url": doc.metadata.get('url', '')
        }

@app.post("/vector_search")
async def vs_service(request: KeywordRequest):
    report_location = request.report_location
    results = retriever_local(report_location, 10)

    # 벡터 검색 결과 반환 (데모 상 메타데이터 포함)
    response = []
    for doc, score in results:
        response.append({
            "title": doc.metadata.get('title', ''),
            "articleDate": doc.metadata.get('article_date', ''),
            "company": doc.metadata.get('company', ''),
            "url": doc.metadata.get('url', ''),
            "keywords": doc.metadata.get('keywords', []),
            "sentiment": doc.metadata.get('sentiment', '')
        })

    return response
