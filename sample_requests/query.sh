MODEL="babbage"
MODEL="gpt-3.5-turbo"
MODEL="gpt-4"
curl  -X POST \
  'http://localhost:5001/query' \
  --header 'Accept: */*' \
  --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "query":"based on given context, why should I use docusaurus? Can you respond in markdown format?",
  "skip_price_calc": false,
  "llm_model": "'$MODEL'"
}'
