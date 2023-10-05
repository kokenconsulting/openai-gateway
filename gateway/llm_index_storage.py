import os
from llama_index.vector_stores import RedisVectorStore
from llama_index import StorageContext

openaikey = os.environ.get('OPENAI_API_KEY', 'OPENAI_API_KEY')
# print first 5 characters of openai key
print("OPENAI_API_KEY STARTS WITH::: " + openaikey[0:5])


def get_storage_context():
    vector_store = get_vector_store()
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )
    return storage_context

def get_vector_store():
    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379')
    print("REDIS URL IS "+redis_url)
    vector_store = RedisVectorStore(
        index_name="llm-project",
        redis_url=redis_url,
        overwrite=True
    )

    return vector_store
