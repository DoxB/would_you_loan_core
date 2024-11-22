from fastapi import FastAPI
from items import QuestionRequest, KeywordRequest
from functions import retriever, augmented, generation

app = FastAPI()

####################################
###     RAG 이후 답변 보내기     ###
####################################

### RAG
@app.post("/rag")
async def rag_service(requset: QuestionRequest):
    user_id = requset.user_id
    user_question = requset.user_question

    result = retriever(user_question, 1)
    text = augmented(user_question, result)
    answer = generation(text)

    response = {
        "user_id": user_id,
        "answer": answer,
        "title": result[0].metadata['title'],
        "article_date": result[0].metadata['article_date'],
        "company": result[0].metadata['company'],
        "url": result[0].metadata['url']
    }

    return response

### VectorSearch
@app.post("/vector_search")
async def vs_service(requset: KeywordRequest):
    report_location = requset.report_location

    results = retriever(report_location, 10)
    response = []

    for result in results:
        response.append({
            "title": result.metadata['title'],
            "articleDate": result.metadata['article_date'],
            "company": result.metadata['company'],
            "url": result.metadata['url'],
            "keywords": result.metadata['keywords'],
            "sentiment": result.metadata['sentiment']
        })

    return response