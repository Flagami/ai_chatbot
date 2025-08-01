from openai import OpenAI
# import custom module
from utils import setup_logger
from config import SILICON_FLOW_API_KEY,SILICON_FLOW_API_URL,TEMPERATURE,RETRY_TIME,MODEL_MAP

logger = setup_logger(__name__)

def call_silicon_cloud_api(messages,
                           model_name,
                           temperature:float=TEMPERATURE,
                           stream:bool = False,
                           api_key=SILICON_FLOW_API_KEY,
                           url=SILICON_FLOW_API_URL,
                           retry_times: int = RETRY_TIME, ):

    try:
        client = OpenAI(api_key=api_key, base_url=url)
        logger.info(f"Init openai client success!")
    except Exception as e:
        error_info = f"Initializing openai client for model 【{model_name}】 error: {e}"
        logger.error(error_info)
        raise e

    # Get full name of model based on Silicon flow's definition https://cloud.siliconflow.cn/me/models
    full_model_name = MODEL_MAP[model_name]

    for attempt in range(1, retry_times + 1):
        logger.debug(f"Requesting model:{model_name} with messages:{messages}")
        try:
            response = client.chat.completions.create(
                model=full_model_name,
                messages=messages,
                stream=stream,
                temperature=temperature
            )

            if stream:
                # Return a generator for streaming responses
                def stream_response():
                    for chunk in response:
                        yield chunk
                    logger.info(f"Streamed {model_name} API response successfully on attempt {attempt}")

                return stream_response()
            else:
                # Return the complete response for non-streaming
                logger.info(f"Called {model_name} API successfully on attempt {attempt}")
                return response

        except Exception as e:
            logger.error(f"API call failed on attempt {attempt}/{retry_times}: {str(e)}")
            if attempt == retry_times:
                error_msg = f"Exhausted {retry_times} retries for {model_name} API call"
                logger.error(error_msg)
                return error_msg


if __name__ == '__main__':
    query = "hello"
    model_name = "THUDM/GLM-4-9B-0414"
    response = call_silicon_cloud_api(query, model_name)
    print(response)