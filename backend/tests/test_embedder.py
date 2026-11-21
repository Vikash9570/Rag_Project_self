from backend.app.services.embedder import get_embeddings
from langchain_core.documents import Document

# testig embedder

word="word"*10

def test_embedder(word):
    try:
        embd_config=get_embeddings()
        embd=embd_config.embed_query(word)
        print(embd)
        # print(generated_embd.type)

    except Exception as e:
        raise Exception(f'error happend while generating embedding: {e}')



if __name__=='__main__':
    test_embedder(word)