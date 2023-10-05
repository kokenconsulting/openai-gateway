
def query_index(index,token_counter, question_text):
    token_counter.reset_counts()
    query_engine = index.as_query_engine()
    response = query_engine.query(question_text)
    #index.storage_context.persist(storagepath)
    return response,token_counter