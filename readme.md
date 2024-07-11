# 🌱 Cropify AI: Your Intelligent Farming Companion 🌾
Welcome to Cropify AI, the cutting-edge agricultural solution that harnesses the power of artificial intelligence to revolutionize your farming experience! 🚀

![Cropify Banner](https://github.com/K-RED90/Cropify-AI/blob/main/images/Designer.jpeg)

## 🌾 Major Components
With our three innovative features, we empower you to unlock the full potential of your crops and maximize your yields like never before.
- 🔍 **AgriScan**: Diagnose Crop Issues with AI Image Analysis
Simply upload images of your affected plants, and our advanced AI system, powered by GPT-4V, will accurately identify diseases, pests, and insect infestations. Get detailed descriptions, potential impacts, and recommended treatments – all at your fingertips! 🌿
- **💬 AgroAssist**: Your Virtual Farm Advisor
Engage in natural conversations with our intelligent chatbot, AgroAssist. Leveraging weather tools and search engines, it provides expert guidance on crop cultivation, pest management, and farming best practices. Plus, it shares valuable links for further reading! 🌍
- **📊 AgriAdvisor**: Data-Driven Farm Management
By analyzing your farm data, such as crop types, soil conditions, and real-time weather information, AgriAdvisor delivers tailored recommendations for optimizing fertilizer application, pest control, soil health, and crop management. Maximize your yields with data-driven insights! 📈

## ✨ Major Details
###  1. Agent Workflow Breakdown: AgriScan and AgroAssist
The agent goes through a lot of steps to provide the best possible assistance to the user. The agent can handle both text and image inputs, providing a comprehensive solution for various user queries. The workflow is divided into two main sections: text input and image input.

![Agent Workflow](https://github.com/K-RED90/Cropify-AI/blob/main/images/Agent%20Workflow.png)

The workflow operates differently depending on the user input type: text or image.

**Text Input:**

1. **Query Classification:** The system utilizes `GPT-3.5-turbo-0125` to classify the text input into three categories: farm query, weather query, or "other."

2. **Farm Query:**
    - **Search Query Generation:** If classified as a farm query, `GPT-3.5-turbo-0125` again generates 1-3 relevant search queries to answer the farmer's question.
    - **Search Engine:** The generated queries are then routed to the `search_engine` node for execution. 
    - **Answer Writing:** Retrieved search results are sent to the `answer_writer` node, which utilizes them to formulate an answer for the farmer.
    - **Answer Evaluation:** The `evaluator` node assesses the completeness of the answer.
      - **Incomplete Answer:** If the answer is deemed incomplete, the evaluator generates feedback and sends it, along with the initial answer, to the `specialist` node. The specialist (Agriculture specialist) refines the answer based on the feedback.
      - **Complete Answer:** If the answer is complete, it bypasses the specialist and proceeds to the `final` node.
    - **Final Formatting:**  The `final` node formats the answer for a polished presentation before delivery.

3. **Weather Query:** Weather-related queries are routed directly to the `meteorologist` node.
    - **Weather Tools:** The `meteorologist` utilizes two tools:
        - `GetWeatherDataByCityName`
        - `GetWeatherForecastByCityName`
    - **OpenWeatherMap API Integration:** Both tools leverage the OpenWeatherMap API to retrieve weather data based on the specified location.
    - **Looping Execution:** The `meteorologist` runs in a loop, repeatedly checking for tool usage.
      - **No Tool Usage:** If no tools are called, it signifies completion, and the workflow proceeds to the `final` node for formatting.
      - **Tool Usage:** When a tool is used, the results are sent back to the `meteorologist` for further processing. This loop continues until an `AgentFinish` signal is received.

4. **Other Queries:** Queries not related to farm or weather are directed to the `fallback` node. This node is restricted to providing basic responses related to greetings and appreciation, not offering solutions beyond agriculture. Finally, the answer is formatted in the `final` node.

**Image Input:**

1. **Image Classification:** The system employs `GPT-4V` to categorize the uploaded image as a pest, crop disease, or "other."

2. **Pest/Crop Disease Image:**
    - **Specialist Routing:** Images classified as pests or crop diseases are routed to the corresponding specialist nodes (e.g., `pest_specialist` and `crop_disease_specialist`). 
    - **Identification & Description:** The specialists identify the pest/disease in the image and provide a description of its symptoms.
    - **Agent State Storage:** The specialists' findings are intelligently stored within the `agent_state` for future reference.
    - **Query Writing:** The `queries_writer` node generates 1-3 search queries to manage or treat the identified pest/disease.
    - **Workflow Continuation:** The workflow then continues as outlined in the text input section (steps 2 onwards).
    - **Final Answer Formatting:** In the `final` node, the findings from the specialists and the treatment/management recommendations are combined to create a comprehensive answer, which is then formatted for delivery.

3. **Unrelated Image:** Images not classified as pests or crop diseases are handled by the `unrelated_image` node. This node informs the user that the image doesn't depict a pest or disease. Finally, the answer is formatted in the `final` node.

### 2. AgriAdvisor: Data-Driven Farm Management
AgriAdvisor is a powerful feature of Cropify AI that provides data-driven farm management recommendations. By analyzing your farm data, such as crop types, soil conditions, and real-time weather information, AgriAdvisor delivers tailored recommendations for optimizing fertilizer application, pest control, soil health, and crop management strategies.

One of the key challenges in developing AgriAdvisor is the time-consuming and expensive process of calling multiple APIs to analyze the farm data and augment the AI's answer. To address this challenge, we leverage the agent's learned knowledge and its weights to analyze the farm data and provide recommendations.

However, to ensure the best possible results, we employ more effective prompting techniques, such as the `Chain of Thought (COT)` prompting method. This approach encourages the AI agent to break down complex problems into a series of intermediate steps, explicitly reasoning through the problem and explaining its thought process.

The `Chain of Thought (COT)` prompting method works as follows:

1. **Problem Decomposition**: The AI agent breaks down the given problem into smaller, more manageable sub-problems or steps.
2. **Step-by-Step Reasoning**: For each sub-problem, the agent reasons through the necessary steps to solve it, explicitly expressing its thought process and intermediate conclusions.
3. **Final Solution**: After working through the intermediate steps, the agent arrives at the final solution to the original problem, combining the insights gained from the step-by-step reasoning.

By employing the `Chain of Thought (COT)` prompting method, AgriAdvisor can provide more transparent and interpretable recommendations. The agent's reasoning process is laid out in a structured manner, allowing users to understand how the AI arrived at its recommendations and the factors it considered.

Overall, AgriAdvisor combines the power of learned knowledge, efficient data analysis, and the `Chain of Thought (COT)` prompting method to deliver accurate and transparent farm management recommendations, helping farmers maximize their yields and achieve sustainable agricultural practices.

## AgriScan Evaluation

![AgriScan Evaluation](https://github.com/K-RED90/Cropify-AI/blob/d6b8af0efe3222b01b554b47e8b85021af158aaf/images/evaluation.png)
[Evaluation Codes can be found here](https://github.com/K-RED90/Cropify-AI/blob/main/evaluator.ipynb)

The image above showcases a comprehensive evaluation of Cropify AI's image analysis capabilities. It presents a diverse set of images depicting various agricultural scenarios, each accompanied by the model's prediction and the actual label.

## Evaluation Methodology

The evaluation process involves comparing the model's predictions with the actual annotated images. The accuracy score `(77.27%)` represents the overall performance of the image analysis model across the given set of examples.

To ensure a robust evaluation, the following considerations are taken into account:

1. **Label Variations**: The evaluation accounts for variations in label phrasing and terminology. For instance, "Apple Scab" and "applescab leaf" are treated as equivalent labels, ensuring that minor linguistic differences do not impact the accuracy assessment.

2. **Alternative Names and Synonyms**: Agricultural terminology often includes multiple synonyms or alternative names for the same condition or organism. The evaluation process considers these variations, recognizing that "Corn Smut" and "corn-fungus" refer to the same disease.

3. **Visual Diversity**: The image set covers a wide range of visual representations, including different crop types, disease manifestations, pest appearances, and environmental conditions. This diversity ensures that the model's performance is evaluated across a broad spectrum of real-world scenarios encountered in agricultural settings.

### Analysis and Insights

By examining the image, several observations can be made regarding AgriScan image analysis capabilities:

1. **Correct Predictions**: The model demonstrates accurate predictions for various conditions, such as "Aphid Infestation," "Corn Smut," "Monarch Caterpillar," "Japanese Beetle," and "Gray mold (Botrytis cinerea)." These correct identifications highlight the model's ability to recognize and classify different diseases, pests, and insects effectively.

2. **Challenging Cases**: Certain examples reveal the model's limitations or areas for improvement. For instance, the model incorrectly predicted "Cabbage Looper" for a "Cutworm" case and "Tomato Early Blight" for a "Late tomato blight" scenario. These misclassifications indicate potential challenges in distinguishing between visually similar conditions or subtle variations in disease progressions.

3. **Fine-grained Differentiation**: The evaluation also reveals the model's capability to differentiate between closely related conditions. For example, it correctly distinguished between "Tomato Early Blight" and "tomato-late-blight," demonstrating its ability to capture nuanced visual cues and make accurate diagnoses.

## Evaluation of AgroAssist Chatbot

We evaluated the performance of our `AgroAssist` chatbot by using another instance of the GPT-3.5-turbo model to respond to the same queries that were previously answered by our AgroAssist. We then employed another instance of the GPT-3.5-turbo-0125 model to compare the answers provided by AgroAssist and the answers provided by the GPT-3.5-turbo-0125 model.

All the answers given by our AgroAssist were marked as correct, except for the queries that required the model to call the weather API. Since we did not provide the GPT-3.5-turbo-0125 model with access to the weather API, it always responded that it does not have access to real-time weather data. This resulted in an accuracy score of `89%.`

However, we manually evaluated the queries related to weather by comparing AgroAssist's responses with the responses from the weather API tool, and they were all correct. We are very excited about the idea of `augmenting a language model with real-time search engine results and a weather API` for seamless and accurate responses, and we are confident in the continued performance of our chatbot in solving agricultural problems.

The runs and evaluations can be accessed at `Langsmith` with this link: [Cropify AI-ATF Hackathon](https://smith.langchain.com/public/b69761e9-ef28-4f50-bb02-abc4df6f3ae5/d/compare?selectedSessions=68321f62-abc5-4002-ac8b-0eb21091c641&baseline=undefined&activeSession=68321f62-abc5-4002-ac8b-0eb21091c641)


## 🛠️ Built With
- **Language Models**: GPT-3.5-turbo-0125, gpt-4-vision-preview (Fallback to Claude-3-Haiku when error is encountered)
- **APIs**: OpenWeatherMap, Tavily AI and DuckDuckGo
- **Frameworks**: FastAPI, LangChain, LangGraph, LangSmith, Pydantic, React and more.
- **Tools**: Docker, GitHub Actions, Postman, Swagger UI
- **Languages**: Python, JavaScript, HTML, CSS
- **Data Storage**: MongoDB
- **Deployment**: Vercel

## Demo Video
[![ATF-Hackathon-Demo](https://res.cloudinary.com/marcomontalbano/image/upload/v1715393486/video_to_markdown/images/google-drive--1Dtpewpa3F40mVLb-6Npb4RpKBSOAyMS9-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://drive.google.com/file/d/1L0TrLB48xJLkxnZIJd42ShnRP3XBtNpj/view?usp=sharing "ATF-Hackathon-Demo")

## 🚀 Getting Started

### Run Locally
To get a local copy up and running follow these simple steps.
1. Clone the repo
   ```sh
   git clone https://github.com/K-RED90/Cropify-AI.git
    ```
2. Install dependencies
    ```sh
    pip install -r requirements.txt
    ```
3. Set up your environment variables
    ```sh
    cp .env.example .env
    ```
    Edit the `.env` file and provide the necessary API keys and configuration settings.
4. Run the Cropify application
    ```sh
    python run.py
    ```
5. Navigate to `client` folder
    ```sh
    cd client
    ```
6. Install dependencies
    ```sh
    npm install
    ```
7. Start the React app
    ```sh
    npm start
    ```
8. Open your browser and go to `http://localhost:3000/` to view the app

## License
Cropify AI is released under the [MIT License](https://opensource.org/licenses/MIT).

## Resources and Tools
- [OpenAI](https://www.openai.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://langchain.com/)
- [LangSmith](https://smith.langchain.com/)
- [LangGraph](https://graph.langchain.com/)
- [Tavily AI](https://tavily.com/)
- [DuckDuckGo](https://duckduckgo.com/)
- [OpenWeatherMap](https://openweathermap.org/)

## 🤗 Acknowledgement
We thank the [African Technology Forum](https://www.linkedin.com/in/african-technology-forum-638bb02aa?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app) for organizing this hackathon and [OpenAI](https://www.openai.com/) for sponsoring it, enabling us to learn and explore innovative solutions for agricultural challenges.

**🌾 Happy Farming! 🚜🌞**
