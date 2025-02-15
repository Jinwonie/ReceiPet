from conf import GPT, PERPLEXITY
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatPerplexity
from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_community.agent_toolkits import create_sql_agent

# agent의 답변을 생성하는 함수

# 영수증 내 정보 OCR
def receipt_to_text(image, api_key, temperature=0.1):
    llm = ChatOpenAI(model=f"{GPT.GPT_MODEL_NAME}", temperature=temperature, openai_api_key=api_key)
    
    system = SystemMessage(
        content=f"{GPT.GPT_SYSTEM}"
    )
    
    human = HumanMessage(
        content=[
            {
                "type": "text",
                "text": f"{GPT.GPT_QUESTION}"
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image}"}
            },
        ]
    )
    response = llm.invoke([system, human])
    result = response.content
    
    return result

# perplexity 질문 생성
def generate_perplexity_question(receipt, add_ingredients, sub_ingredients):
    question = f"""1. 가지고 있는 재료
    {receipt}, {add_ingredients}

    2. 사용하면 안 되는 재료
    {sub_ingredients}

    1번 재료들을 사용해서 만들 수 있는 요리 레시피를 알려주세요.

    반드시 모든 재료를 사용할 필요는 없고 일부 재료만 활용하여도 됩니다.

    음식 레시피 중 2번 재료가 사용된다면 해당 레시피는 추천하면 안 됩니다.

    레시피를 참고할 수 있도록 url을 제공해주세요
    
    같거나 비슷한 레시피는 한 번만 추천해주세요(중복 절대 불가)

    언어: 한국어

    포맷(최대 5개 레시피까지 추천하세요. 포맷에 적힌 내용 외의 말은 하지 마세요.)
    레시피 명:
    재료:
    만드는 법:
    url:(youtube)"""
    
    return question

def question_to_answer(input_text, api_key):
    chat = ChatPerplexity(
        api_key=api_key,
        model=f"{PERPLEXITY.PERPLEXITY_MODEL_NAME}",
        temperature=0.1
    )
    
    human = "{input}"
    prompt = ChatPromptTemplate.from_messages([("human", human)])
    
    chain = prompt | chat | StrOutputParser()
    
    response = chain.invoke({"input": input_text})
    
    return response
