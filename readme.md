# Cropify - AI-Powered Smart Farming Solution

Cropify is a cutting-edge AI-powered platform designed to revolutionize modern farming practices. By leveraging advanced technologies such as GPT-4-turbo and the OpenWeatherMap API, Cropify provides farmers with tailored recommendations and insights to optimize crop yield, minimize losses, and enhance overall farm productivity.

![Cropify Banner](https://github.com/K-RED90/Cropify-AI/blob/main/image/Designer.jpeg)

## Features

- **Crop Disease and Pest Control**: Identify and analyze crop diseases and pests from images, providing comprehensive recommendations for effective control and prevention strategies.
- **Soil Fertility Analysis**: Evaluate soil health and fertility levels, offering personalized recommendations for optimal fertilizer application and soil management practices.
- **Weather Forecast Integration**: Access real-time weather data and forecasts tailored to your farm's location, enabling informed decision-making for irrigation, planting, and harvesting schedules.
- **Crop Growth Monitoring**: Monitor crop growth stages and receive timely alerts and recommendations for optimizing yield and quality.
- **Fertilizer Recommendation**: Receive data-driven fertilizer recommendations based on your farm's specific soil conditions, crop types, and weather patterns.
- **Irrigation Optimization**: Leverage irrigation recommendations tailored to your farm's water requirements, crop types, and local weather conditions.
- **AI-Powered Chat**: Engage in natural language conversations with Cropify's AI assistant, allowing you to ask questions, seek advice, and gain valuable insights for enhancing your farming practices.

## Technologies

- **Python**: The core programming language used for developing Cropify's backend and AI models.
- **GPT-4-turbo**: Cropify harnesses the power of OpenAI's GPT-4-turbo language model, enabling advanced natural language processing and generation capabilities.
- **OpenWeatherMap API**: Cropify integrates with the OpenWeatherMap API to provide accurate and up-to-date weather data for farm locations worldwide.
- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python.
- **LangChain**: A framework for building applications with large language models (LLMs) through composability.

## Installation

1. Clone the Cropify repository:

```bash
git clone https://github.com/your-repo/cropify.git
```

2. Install the required dependencies:

```bash
cd cropify
pip install -r requirements.txt
```

3. Set up your environment variables:

```bash
cp .env.example .env
```

Edit the `.env` file and provide the necessary API keys and configuration settings.

4. Run the Cropify application:

```bash
python main.py
```

## API Endpoints

Cropify provides a comprehensive RESTful API for integrating with various farm management systems and tools. Here are some key endpoints:

### Root Endpoint

```http
GET /
```

Retrieves a welcome message for the Cropify API.

### Farm Data Management

```http
POST /data
```

Add farm data to the system, including information about crop types, soil composition, and other relevant details.

```http
POST /weather
```

Provide weather data for a specific location, enabling Cropify to generate accurate recommendations.

### Crop Recommendations

```http
GET /fertilizer/{farm_id}
GET /pest/{farm_id}
GET /weed/{farm_id}
GET /soil/{farm_id}
```

Retrieve personalized recommendations for fertilizer application, pest and disease control, weed management, and soil health improvement based on the farm's data and local weather conditions.

### Chat with AI

```http
POST /chat/
```

Initiate a chat session with Cropify's AI assistant, allowing you to ask questions, seek advice, and receive valuable insights for enhancing your farming practices.

### Image Analysis

```http
POST /image
```

Upload an image of a diseased crop or pest, and Cropify will analyze the image, identify the issue, and provide recommendations for control and prevention.

For detailed information on each endpoint's parameters, responses, and usage examples, please refer to the [API documentation](link-to-api-docs).

## Workflow Diagram

The following diagram illustrates the high-level workflow and decision process implemented by Cropify's AI agent:

![Workflow Diagram](https://github.com/K-RED90/Cropify-AI/blob/main/image/graph.png)

This workflow handles scenarios such as crop disease and pest identification, generating relevant recommendations, and providing appropriate responses or fallback options when necessary.

## Contributing

Contributions to Cropify are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/your-repo/cropify).

## License

Cropify is released under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgments

We would like to express our gratitude to the following organizations and projects for their valuable contributions:

- [OpenAI](https://www.openai.com/) for providing the GPT-4-turbo language model.
- [OpenWeatherMap](https://openweathermap.org/) for their reliable weather data API.
- [FastAPI](https://fastapi.tiangolo.com/) for the powerful and high-performance web framework.
- [LangChain](https://python.langchain.com/en/latest/index.html) for the language model integration tools.
