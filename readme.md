# OPENAI EXPERIMENTAL GATEWAY

## TL;DR:

```bash
# Start the app with Web API and Redis Vector DB
docker-compose build; docker-compose up -d

# Choose a model
MODEL="babbage"
MODEL="gpt-3.5-turbo"
MODEL="gpt-4"

# Build the index
curl -X GET \
  "http://localhost:5001/index?llm_model=$MODEL" \
  --header 'Accept: */*' \
  --header 'User-Agent: Thunder Client (https://www.thunderclient.com)'

# Query
curl -X POST \
  'http://localhost:5001/query' \
  --header 'Accept: */*' \
  --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "query": "Based on the given context, why should I use Docusaurus? Can you respond in Markdown format?",
  "skip_price_calc": false,
  "llm_model": "'$MODEL'"
}'
docker-compose down

```

## Introduction

This experimental project aims to showcase Retrieval Augmented Generation (RAG) for GEN-AI and also emphasize the cost of each GEN-AI query.

For cost calculations, the [OpenAI API Pricing Library](https://github.com/kokenconsulting/openai-api-pricing) is used.

For RAG, the [llama-index framework](https://github.com/run-llama/llama_index) is utilized.

## Requirements

* Ensure you have a valid OPENAI API KEY. See [How to Get an OpenAI API Key](https://www.maisieai.com/help/how-to-get-an-openai-api-key-for-chatgpt).
  * The value of the API key must be set in the `OPENAI_API_KEY` environment variable.
* The easiest way to run the application is via Docker. Otherwise, ensure that a Redis Vector DB is running.
  * Run `docker-compose build; docker-compose up` in the root directory.
  * This command will build and run the Redis database and Web API, while mapping data to the `data` folder (which contains pages from Docusaurus).
* To map your own directory, update the volume mapping in the Docker Compose file.
* If you don't skip cost calculations, ensure that [OpenAI API Pricing Web API](https://openai-api-pricing-web-api.onrender.com/openai) is responsive, as pricing depends on this.
* Only three models are available: "gpt-3.5-turbo", "babbage-002", and "gpt-4".
* Refer to `build_index.sh` and `query.sh` for sample requests.

## Contact

If you have any questions or remarks, please send an email to ali@koken-consulting.com.

## Todo
- Validate Input and return errors
- Publish Swagger Specification
- Introduce authentication and authorization.
- Use Python modules for better file management.
- Check if the Redis Vector database is available before building indexes and running queries.
- When querying, check if the index is already built. If not, return an error or a suggestion.
- Add information about CLI