import openai
import re
import time


def gpt_extract_info(jobDescription):
    OPENAI_API_KEY = 'replace with your key'
    openai.api_key = OPENAI_API_KEY

    prompt_message = """
    I will provide you with a job description, You will need to answer based on the following requirements & questions.
    1. What is the minimum year of experience required for this job with a Master degree? Answer with number.
    2. Does the description mention that this role needs any kind of security clearance? Answer Yes or No.
    3. Does the description mention that it will not provide visa sponsorship? Answer Yes or No.
    4. Does the description mentioned that this role requires U.S. citizenship? Answer Yes or No.
    If you are unsure about the answer to any of the questions, answer 'Unsure' to that question.
    Output format requirement:
    Use comma to separate your answer to each question. No space allowed.
    An example output would be like:
    1,No,Yes,Unsure
    Below is the job description:
    """
    description = re.sub(r'^\s*\n', '', jobDescription, flags=re.MULTILINE)
    # input = prompt_message + description
    messages = [
        {"role": "system", "content": prompt_message},
        {"role": "user", "content": description}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages)

    # print(jobDescription)
    print(response["choices"][0]["message"]["content"])

    time.sleep(0.5)

    return response["choices"][0]["message"]["content"]