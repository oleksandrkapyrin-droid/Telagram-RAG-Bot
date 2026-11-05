from db import collection
from llm import llm_request


def answer_question(question):
    result = collection.query(query_texts=question, n_results=3)
    if not result['documents'][0]:
        return {'answer': 'База знань порожня', 'sources': []}

    documents = result['documents'][0]
    metadatas = result['metadatas'][0]

    llm_answer = llm_request(question, documents)
    if llm_answer is None:
        return {'answer': 'Сталася помилка при зверненні до LLM. Спробуйте пізніше.', 'sources': []}

    sources = [f'Файл: {meta['sources']}, Чанк: {meta['chunk']}' for meta in metadatas]
    if llm_answer == 'У документі немає відповіді на це питання.':
        sources = ''
    answer = {'answer': llm_answer, 'sources': sources}

    return answer


if __name__=='__main__':
    response = answer_question(input('Ваше питання: '))

    print(response['answer'])
    for src in response['sources']:
        print(src)