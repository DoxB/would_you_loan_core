# functions.py
import os
import json
import requests
from dotenv import load_dotenv
from transformers import AutoTokenizer
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import ElasticVectorSearch
from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults
import random

load_dotenv()

def retriever(user_question, top_num):
    ELASTIC_ID = os.environ.get('ELASTIC_ID')
    ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD')
    ELASTIC_HOST = os.environ.get('ELASTIC_HOST')
    ELASTIC_PORT = os.environ.get('ELASTIC_PORT')

    embeddings = HuggingFaceEmbeddings(
        model_name="./embedding/model/bge-m3",
        model_kwargs={'device':'cpu'}
    )

    es_url = f"http://{ELASTIC_ID}:{ELASTIC_PASSWORD}@{ELASTIC_HOST}:{ELASTIC_PORT}"

    vectorstore = ElasticVectorSearch(
        embedding=embeddings,
        elasticsearch_url=es_url,
        index_name="article-index"
    )

    # (Document, score) 형태 반환
    # score를 유사도(0~1)로 가정. 실제 반환 값이 거리인지 유사도인지에 따라 로직 조정 필요.
    results = vectorstore.similarity_search_with_score(user_question, k=top_num)
    return results

def augmented(user_question, doc: Document):
    model_id = './llm/model/llama-3-Korean-Bllossom-8B-gguf-Q4_K_M'
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    PROMPT = '''
    당신은 유용한 AI 어시스턴트입니다. 사용자의 질의에 대해 친절하고 정확하게 답변해야 합니다.
    '''

    question = f'''
    {user_question}

    답변은 추천하는 기사 내용을 요약하자면 이렇게 된다고 친절히 설명해주고 제목은 출력하지마.

    추천하는 기사의 내용은 다음과 같습니다.

    {doc.page_content}
    최종 답변은 500자로 한정해주고, 그 안에 완벽한 문장으로 마무리해줘
    '''

    messages = [
        {"role": "system", "content": PROMPT.strip()},
        {"role": "user", "content": question.strip()}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    return text

def augmented_tavily(user_question, tavily_results: str):
    # Tavily 검색 결과를 LLM에 전달하기 위한 프롬프트 구성
    model_id = './llm/model/llama-3-Korean-Bllossom-8B-gguf-Q4_K_M'
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    PROMPT = '''
    당신은 유용한 AI 어시스턴트입니다. 사용자의 질의에 대해 친절하고 정확하게 답변해야 합니다.
    '''

    question = f'''
    {user_question}

    저는 Tavily로 인터넷 검색을 했고, 다음과 같은 결과를 얻었습니다.
    이 검색 결과를 기반으로 사용자가 물어본 내용에 대해 친절하고 명확하게 답해주세요.
    결과를 요약하되, 불필요한 내용은 제외하고 핵심만 전달해주세요.

    Tavily 검색 결과:
    {tavily_results}

    처음에 Tavily로 인터넷 검색을 했다는 것을 명확하게 전달해주세요.
    '''

    messages = [
        {"role": "system", "content": PROMPT.strip()},
        {"role": "user", "content": question.strip()}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    return text

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
    response_json = response.json()
    # 모델 응답 파싱 로직은 모델 출력 형식에 따라 조정
    answer = response_json['text'][0].split('<|start_header_id|>assistant<|end_header_id|>\n\n')[1]
    return answer

def filter_answer(answer: str) -> str:
    forbidden_keywords = ["욕설", "민감한 기밀정보", "정치적인 발언"]
    for kw in forbidden_keywords:
        if kw in answer:
            answer = answer.replace(kw, "***")
    return answer

def tavily_search(query: str) -> str:
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        return "Tavily API 키가 설정되지 않았습니다."

    search = TavilySearchResults(tavily_api_key=tavily_api_key)
    search_results = search.run(query)

    # search_results의 타입을 확인 (print, logging 등)
    # 예: print("search_results type:", type(search_results))
    # TavilySearchResults의 run 메서드 반환값이 문자열이 아니라 파이썬 리스트나 딕셔너리라면 바로 사용 가능.

    # 만약 search_results가 이미 dict 형태라면 바로 사용
    # search_results가 만약 [{"title": "...", "snippet": "..."}] 형태의 리스트라면:
    if isinstance(search_results, list):
        data = {"results": search_results}
    elif isinstance(search_results, dict):
        data = search_results
    else:
        # 만약 여전히 문자열 형태라면 이 때만 json.loads 시도
        if isinstance(search_results, str):
            try:
                data = json.loads(search_results)
            except json.JSONDecodeError:
                return f"Tavily 검색 결과 파싱 중 오류: {search_results}"
        else:
            # 예상치 못한 타입일 경우 문자열 변환 후 반환
            return f"예상치 못한 Tavily 결과 형식: {str(search_results)}"

    results_list = data.get("results", [])
    if not results_list:
        return "Tavily 검색 결과가 없습니다."

    results_str = "\n".join([f"- {item.get('title', '제목없음')}: {item.get('snippet', '')}" for item in results_list])
    return results_str


def retriever_local(user_question, top_num):
    ELASTIC_ID = os.environ.get('ELASTIC_ID')
    ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD')
    ELASTIC_HOST = os.environ.get('ELASTIC_HOST')
    ELASTIC_PORT = os.environ.get('ELASTIC_PORT')

    embeddings = HuggingFaceEmbeddings(
        model_name="./embedding/model/bge-m3",
        model_kwargs={'device':'cpu'}
    )

    es_url = f"http://{ELASTIC_ID}:{ELASTIC_PASSWORD}@{ELASTIC_HOST}:{ELASTIC_PORT}"

    vectorstore = ElasticVectorSearch(
        embedding=embeddings,
        elasticsearch_url=es_url,
        index_name="article-index"
    )

    # (Document, score) 형태 반환
    # score를 유사도(0~1)로 가정. 실제 반환 값이 거리인지 유사도인지에 따라 로직 조정 필요.
    results = vectorstore.similarity_search_with_score(user_question, k=top_num)

    # Update "중립" sentiment with 50:50 "긍정" or "부정"
    updated_results = []
    for doc, score in results:
        if doc.metadata.get('sentiment') == "중립":
            doc.metadata['sentiment'] = random.choice(["긍정", "부정"])
        updated_results.append((doc, score))

    return updated_results