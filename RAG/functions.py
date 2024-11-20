from langchain_huggingface import HuggingFaceEmbeddings
from langchain_elasticsearch import ElasticsearchStore
import os
from dotenv import load_dotenv
import requests
import json
from transformers import AutoTokenizer

load_dotenv()

#################
### Retriever ###
#################
def retriever(user_question, top_num):
    ELASTIC_ID = os.environ.get('ELASTIC_ID')
    ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD')
    ELASTIC_HOST = os.environ.get('ELASTIC_HOST')
    ELASTIC_PORT = os.environ.get('ELASTIC_PORT')

    # 임베딩 모델 설정
    embeddings = HuggingFaceEmbeddings(
        model_name="./embedding/model/bge-m3",
        model_kwargs={'device':'cpu'}
    )

    # ElasticSearch 벡터 스토어 설정
    client = ElasticsearchStore(
        es_url=f"http://{ELASTIC_HOST}:{ELASTIC_PORT}",
        index_name="article-index",
        es_user=ELASTIC_ID,
        es_password=ELASTIC_PASSWORD,
        embedding=embeddings)

    query = user_question
    result = client.similarity_search(query, k=top_num)

    return result

#################
### Augmented ###
#################
def augmented(user_question, result):
    model_id = './llm/model/llama-3-Korean-Bllossom-8B-gguf-Q4_K_M'
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    PROMPT = f'''
    당신은 유용한 AI 어시스턴트입니다. 사용자의 질의에 대해 친절하고 정확하게 답변해야 합니다.
    '''

    question = f'''
    {user_question}

    답변은 추천하는 기사 내용을 요약하자면 이렇게 된다고 친절히 설명해주고 제목은 출력하지마.

    추천하는 기사의 내용은 다음과 같습니다.

    {result[0].page_content}
    '''

    messages = [
        {"role": "system", "content": f"{PROMPT}"},
        {"role": "user", "content": f"{question}"}
        ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize = False,
        add_generation_prompt=True
    )

    return text

##################
### generation ###
##################

def generation(text):
    VLLM_HOST = os.environ.get('VLLM_HOST')
    VLLM_PORT = os.environ.get('VLLM_PORT')

    vllm_host = f"http://{VLLM_HOST}:{VLLM_PORT}"
    url = f"{vllm_host}/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": text,
        "max_tokens":512,
        "stop":["<|eot_id|>"],
        "top_p":0.9,
        "temperature":0.6
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    answer = response.json()['text'][0].split('<|start_header_id|>assistant<|end_header_id|>\n\n')[1]

    return answer
