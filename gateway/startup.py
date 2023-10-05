from flask import Flask, request
import llm_index_storage as llm_index_storage
import llm_index as aiindex
import core_data_folder as core_data_folder
import core_search_documentation
import core_llm_model_mapper
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'gpt-3.5-turbo'


@app.route('/index', methods=['GET'])
def index():
    # get flask request query string parameters
    llm_model = request.args.get('llm_model')
    if not llm_model:
        llm_model = "gpt-3.5-turbo"
    # return 400 if llm model is not in the list
    available_models = core_llm_model_mapper.get_available_models()    
    if llm_model not in available_models:
        return "BAD REQUEST - llm_model is not in the list of available models:"+str(available_models), 400
    print('LLM MODEL is '+ llm_model)
    storage_context = llm_index_storage.get_storage_context()
    datafolderFullPath = core_data_folder.get_data_folder_full_path()
    index,token_counter = aiindex.build_index(llm_model, datafolderFullPath, storage_context)
    index_response ={}
    index_response["success"] = True
    index_response["message"] = f'Index is build based on {datafolderFullPath}'
    index_response["cost"] = core_search_documentation.getPriceResponseObject(llm_model,token_counter)
    index_response["token_count"] = core_search_documentation.getTokenCounterResponseObject(token_counter)
    index_response['llm_model'] = llm_model
    return index_response


@app.route('/query', methods=['POST'])
def query():
    request_body = request.get_json()
    query = request_body['query']
    llm_model = request_body.get('llm_model')
    if not llm_model:
        llm_model = "gpt-3.5-turbo"
    available_models = core_llm_model_mapper.get_available_models()    
    if llm_model not in available_models:
        return "BAD REQUEST - llm_model is not in the list of available models:"+str(available_models), 400    
    
    skip_price_calc, save_response = getFlagsFromRequestBody(request_body)
    teams_webhook_url = get_teams_webhook_url(request_body)

    result, price_response, token_counter_response = core_search_documentation.run_query(
        llm_model,query, skip_price_calc, save_response, teams_webhook_url)
    response_body = {}
    if price_response:
        response_body['price_response'] = price_response
    response_body['query'] = query
    response_body['query_response'] = result.response
    response_body['llm_model'] = llm_model
    response_body['token_counter_response='] = token_counter_response
    return response_body


def getFlagsFromRequestBody(request_body):
    skip_price_calc = False
    save_response = False
    if 'skip_price_calc' in request_body:
        skip_price_calc = request_body['skip_price_calc']
    if 'save_response' in request_body:
        save_response = request_body['save_response']
    return skip_price_calc, save_response


def get_teams_webhook_url(request_body):
    return request_body.get('teams_webhook_url')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
