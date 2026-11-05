from pathlib import Path
from db import collection
from contextifier import DocumentProcessor


def load_documents():
    processor = DocumentProcessor()

    all_documents = []
    all_ids = []
    all_metadatas = []

    docs_dir = Path('docs')

    for file_path in docs_dir.glob('*'):
        if file_path.suffix.lower() not in ['.pdf', '.txt', '.docx']:
            continue

        result = processor.extract_chunks(str(file_path), chunk_size=500, chunk_overlap=100)

        if not result.chunks:
            print(f'Файл {file_path.name} не містить тексту')

        file_stem = file_path.stem

        for i, chunk in enumerate(result.chunks, start=1):
            all_documents.append(chunk)
            all_ids.append(f'{file_stem}_{i}')
            all_metadatas.append({'source': file_stem, 'chunk': i})

    if all_documents:
        collection.upsert(
            documents=all_documents,
            ids=all_ids,
            metadatas=all_metadatas,
        )
        print(f'Успішно завантажено {len(all_documents)} чанків')
    else:
        print('Не знайдено тексту для завантаження')

if __name__ == '__main__':
    load_documents()