# OpenAI Adapter

Maps ThinkingOS requests to the OpenAI Responses API. The caller supplies the
model and performs the API request. When an output schema is present, the
adapter requests strict JSON Schema output and normalizes `output_text`.

The mapping follows the official [Responses API documentation](https://developers.openai.com/api/reference/resources/responses/methods/create).
No model name is embedded because availability and model choice are deployment
decisions.
