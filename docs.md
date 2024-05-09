# 🌱 Cropify AI: Your Intelligent Farming Companion 🌾
Welcome to Cropify AI, the cutting-edge agricultural solution that harnesses the power of artificial intelligence to revolutionize your farming experience! 🚀

![Cropify Banner](https://github.com/K-RED90/Cropify-AI/blob/main/image/Designer.jpeg)

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

**Reference Image:** ![Agent Workflow](https://github.com/K-RED90/Cropify-AI/blob/main/image/Agent%20Workflow.png)

The workflow operates differently depending on the user input type: text or image.

**Text Input:**

1. **Query Classification:** The system utilizes `GPT-3.5-turbo-0125` to classify the text input into three categories: farm query, weather query, or "other."

2. **Farm Query:**
    - **Search Query Generation:** If classified as a farm query, `GPT-3.5-turbo-0125` again generates 1-3 relevant search queries to answer the farmer's question.
    - **Search Engine:** The generated queries are then routed to the `search_engine` node for execution. 
    - **Answer Writing:** Retrieved search results are sent to the `answer_writer` node, which utilizes them to formulate an answer for the farmer.
    - **Answer Evaluation:** The `answer_evaluator` node assesses the completeness of the answer.
      - **Incomplete Answer:** If the answer is deemed incomplete, the evaluator generates feedback and sends it, along with the initial answer, to the `specialist` node. The specialist (e.g., Agriculture specialist) refines the answer based on the feedback.
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