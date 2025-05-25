## Large language model : ` SOTA LLms  and our Approach `



### LangChain-Compatible LLM Inference Providers

| Provider         | LangChain Integration Package | Supported Models                    | Inference Speed (tokens/sec) | Context Length | Open Source | Notes                                                                                    |                                                                                                                      |
| ---------------- | ----------------------------- | ----------------------------------- | ---------------------------- | -------------- | ----------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Cerebras**     | `langchain-cerebras`          | LLaMA 3.1 (8B, 70B, 405B)           | Up to 2,200 (70B model)      | 128K           | ✅ Yes       | Utilizes Wafer-Scale Engine for unparalleled speed. Offers OpenAI-compatible endpoints.  |                                                                                                                      |
| **Groq**         | `langchain-groq`              | Mixtral 8x7B, LLaMA 3               | Notably high                 | Varies         | ✅ Yes       | Known for low latency and high throughput.                                               |                                                                                                                      |
| **Fireworks AI** | `langchain-fireworks`         | DeepSeek, LLaMA 3, Mixtral          | Competitive speeds           | Varies         | ✅ Yes       | Developer-friendly with support for fine-tuning.                                         |                                                                                                                      |
| **Together AI**  | `langchain-together`          | Mixtral, LLaMA, Zephyr              | Varies                       | Varies         | ✅ Yes       | Offers a broad range of models for experimentation.                                      |                                                                                                                      |
| **OpenAI**       | `langchain-openai`            | GPT-4, GPT-4-turbo, GPT-4o, GPT-3.5 | High performance             | Up to 128K     | ❌ No        | Industry standard with robust ecosystem.                                                 | ([Reuters][1], [langtrace.ai][2], [LangChain][3], [GitHub][4], [LangChain][5], [langchain.com.cn][6], [Cerebras][7]) |


`We will be using cerebras as our inference provider`