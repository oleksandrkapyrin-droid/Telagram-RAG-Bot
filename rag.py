from pathlib import Path



file_path = Path('knowledge.txt')
file_text = file_path.read_text(encoding='utf-8')

def split_text_to_chunks(file_text, chunk_size=500, overlap=100):
    if chunk_size <= overlap:
        raise ValueError('chunk_size повиннен бути більшим ніж overlap')
    
    chunks = []
    start = 0
    text_length = len(file_text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = file_text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


if __name__=='__main__':
    chanks_text = split_text_to_chunks(file_text)

    print(f'Перший шматок:\n {chanks_text[0]}')
    print(f'Загальна кількість шматків:{len(chanks_text)}')