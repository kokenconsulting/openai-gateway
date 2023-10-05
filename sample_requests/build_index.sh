MODEL="babbage"
MODEL="gpt-3.5-turbo"
MODEL="gpt-4"
curl  -X GET \
  "http://localhost:5001/index?llm_model=$MODEL" \
  --header 'Accept: */*' \
  --header 'User-Agent: Thunder Client (https://www.thunderclient.com)'