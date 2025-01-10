import requests
import json

#change based on model name
cpp_filename = "grokbeta_cpp_fixed_solutions.json"
java_filename = "grokbeta_java_fixed_solutions.json"

#change to google/gemini-flash-1.5-8b for the gemini model, based on model name.
model = "x-ai/grok-beta"
api_key = "placeholder"
sys_prompts = '''I have a set of programming problems with provided solutions, each of these solutions contains run-time errors 
For each problem, please analyze the code to identify the source of the error and fix it. Provide a corrected version of the solution given. 
For each problem only give the code solution in response, do not give any details regarding to what was fixed, why and how.
'''

with open("cpp_prompts.json", "r") as cpp_file:
    cpp_prompts = json.load(cpp_file)
    
with open("java_prompts.json", "r") as java_file:
    java_prompts = json.load(java_file)

cpp_fixed_solutions = []
java_fixed_solutions = []
for cpp_prompt in cpp_prompts:
    prompt_text = cpp_prompt['prompt']
    new_prompt = sys_prompts + '\n' + prompt_text + '\n'
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers = {
            "Authorization":f"Bearer {api_key}"
        },
        data=json.dumps({
            "model":model,
            "messages": [{
                "role":"user",
                "content":new_prompt
            }]
        }),
        timeout=60
    )
    if response.status_code == 200:
        response_data = response.json()
        solution = response_data['choices'][0]['message']['content']
        cpp_fixed_solutions.append({
            "id": cpp_prompt['id'],
            "programming_problem_name": cpp_prompt['programming_problem_name'],
            "fixed_solution": solution
        })

        print(f"Successfully processed cpp prompt ID {cpp_prompt['id']}")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)
        
for java_prompt in java_prompts:
    java_prompt_text = java_prompt['prompt']
    java_new_prompt = sys_prompts + '\n' + java_prompt_text + '\n'
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers = {
            "Authorization":f"Bearer {api_key}"
        },
        data=json.dumps({
            "model":model,
            "messages": [{
                "role":"user",
                "content":java_new_prompt
            }]
        }),
        timeout=60
    )
    if response.status_code == 200:
        response_data = response.json()
        solution = response_data['choices'][0]['message']['content']
        java_fixed_solutions.append({
            "id": java_prompt['id'],
            "programming_problem_name": java_prompt['programming_problem_name'],
            "fixed_solution": solution
        })

        print(f"Successfully processed java prompt ID {java_prompt['id']}")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)

with open(cpp_filename, "w") as cpp_output:
    json.dump(cpp_fixed_solutions, cpp_output, indent=4)
with open(java_filename, "w") as java_output:
    json.dump(java_fixed_solutions, java_output, indent=4)

print(f"Finished two files created: {cpp_filename} and {java_filename}")
