import os, sys,datetime
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import llm_index_storage as index_storage
import llm_index as aiindex
import llm_query as aiquery
import msteam_sendmessage
import core_llm_model_mapper
from llama_index.callbacks import CallbackManager, TokenCountingHandler
#import tiktoken
#from llama_index.callbacks import CallbackManager, TokenCountingHandler
#from llama_index import  ServiceContext
from lll_pricing_calculation import calculate_openai_pricing
from llama_index import set_global_service_context
from core_data_folder import get_data_folder_full_path



def run_query(llm_model,query_text,skip_price_calc, save_response, teams_webhook_url=None):
    vector_store = index_storage.get_vector_store()
    specificindex,token_counter = aiindex.get_index_from_vector_store(llm_model,vector_store)
    # check if request body has 'save' property
    result,token_counter = aiquery.query_index(specificindex, token_counter, query_text)
    price_response = None
    if teams_webhook_url:
        send_teams_notification("llm_model"+llm_model+"...query:"+query_text, teams_webhook_url, result)
    if not skip_price_calc:
        price_response = getPriceResponseObject(llm_model,token_counter)
    if save_response:
        #datafolderFullPath = data_folder.get_data_folder_full_path()
        datafolderFullPath = get_data_folder_full_path()
        saveResponse(query_text, datafolderFullPath, result)
    token_counter_response = getTokenCounterResponseObject(token_counter)
    return result,price_response,token_counter_response

def send_teams_notification(query_text, teams_webhook_url, result):
    teams_subject = "Query: "+query_text
    teams_body = "Answer: "+result.response
    msteam_sendmessage.send_teams_notification(teams_webhook_url,teams_subject,teams_body)

def saveResponse(query, datafolderFullPath, result):
    now = datetime.datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
    with open(os.path.join(datafolderFullPath, "result-"+dt_string+".txt"), "w") as f:
        f.write(f"Question: {query} \n")
        f.write(f"Answer: {result.response}")
        
def calculate_price(llm_model,token_counter):
    cost_category,cost_llm_model_name = core_llm_model_mapper.get_cost_model_name(llm_model)
    costForThousandCurrency,embeddingsCost,promptCost,completionTokenCost,total_cost = calculate_openai_pricing(cost_category,cost_llm_model_name,token_counter.total_embedding_token_count,token_counter.prompt_llm_token_count,token_counter.completion_llm_token_count)
    print("currency:"+costForThousandCurrency)
    print("embeddingsCost:"+str(embeddingsCost))
    print("promptCost:"+str(promptCost))
    print("completionTokenCost:"+str(completionTokenCost))
    print("total cost:"+str(total_cost)+ " US Dollars")
    return costForThousandCurrency,embeddingsCost,promptCost,completionTokenCost,total_cost

def getTokenCounterResponseObject(token_counter):
    token_counter_response ={}
    token_counter_response['total_embedding_token_count'] = token_counter.total_embedding_token_count
    token_counter_response['prompt_llm_token_count'] = token_counter.prompt_llm_token_count
    token_counter_response['completion_llm_token_count'] = token_counter.completion_llm_token_count
    return token_counter_response

def getPriceResponseObject(llm_model,token_counter):
    costForThousandCurrency,embeddingsCost,promptCost,completionTokenCost,total_cost = calculate_price(llm_model,token_counter)
    price_response= {}
    price_response['costForThousandCurrency'] = costForThousandCurrency
    price_response['embeddingsCost'] = embeddingsCost
    price_response['promptCost'] = promptCost
    price_response['completionTokenCost'] = completionTokenCost
    price_response['total_cost'] = total_cost
    return price_response