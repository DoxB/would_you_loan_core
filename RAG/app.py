from fastapi import FastAPI
from items import QuestionRequest
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

    result = retriever(user_question)
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