
def get_cost_model_name(llm_model):
    if llm_model == "gpt-3.5-turbo":
        return "GPT-3.5 Turbo","4K context"
    if llm_model == "babbage-002":
        return "Base models","babbage-002"
    if llm_model == "babbage":
        return "Base models","babbage-002"
    if llm_model == "gpt-4":
        return "GPT-4","8K context"
    
def get_available_models():
    return ["gpt-3.5-turbo","babbage-002","gpt-4"]