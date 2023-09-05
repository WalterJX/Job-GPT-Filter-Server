import openai
import time


def gpt_extract_info(jobDescription):
    OPENAI_API_KEY = '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'
    openai.api_key = OPENAI_API_KEY

    prompt_message = """
    You are a experienced software engineer with 10 year of experience, and you are seeking new job opportunities.
    I will provide you with a job description, You will need to answer based on the following requirements & questions.
    1. What is the minimum year of experience required for this job with a Master degree? Answer with number.
    2. Does the description mention that this role needs any kind of security clearance? Answer Yes or No.
    3. Does the description mention that it will not provide visa sponsorship? Answer Yes or No.
    4. Does the description mentioned that this role requires U.S. citizenship? Answer Yes or No.
    If you are unsure about the answer to any of the questions above, just answer 'Unsure' to that question.
    
    Output format requirement:
    Surround your whole output format with @. Use comma to separate your answer to each question. No space allowed.
    An example output would be like this: @1,No,Yes,Unsure@
    
    Below is the job description:
     
    """
    input = prompt_message + jobDescription

    messages = [{"role": "user",
                 "content": input}]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages)

    # print(jobDescription)
    print(response["choices"][0]["message"]["content"])

    time.sleep(0.5)

    return response["choices"][0]["message"]["content"]