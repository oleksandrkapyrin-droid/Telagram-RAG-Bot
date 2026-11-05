from db import collection


def answer_question(question):
    result = collection.query(query_texts=question, n_results=3)
    if not result['documents'][0]:
        return {'answer': 'База знань порожня', 'source': []}

    documents = result['documents'][0]
    metadatas = result['metadatas'][0]

    return documents, metadatas


if __name__=='__main__':
    response = answer_question(input('Ваше питання: '))

    print(response)