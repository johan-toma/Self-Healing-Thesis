import json
from time import sleep

##change based on the json-file
with open('cpp.json', 'r+') as file:
    cpp_data = json.load(file)
with open('java.json', 'r+') as file:
    java_data = json.load(file)
    

prompt_data = []
java_prompt_data = []
i = 0

for cpp_problem in cpp_data:
    prompt = f'''
        Please help me solve this code with {cpp_problem['programming_language']}\n
        This is the programming problems desc: {cpp_problem['programming_problem_name']}\n
        {cpp_problem['desc']}\n
        This code contains a run-time error.\n
        {cpp_problem['additional_information']}
        {cpp_problem['solution']}
    '''
    #print(prompt)
    prompt_data.append({"id": i, "programming_problem_name":cpp_problem["programming_problem_name"],"prompt": prompt, "extra error": ""})
    i += 1

i = 0
for java_problem in java_data:
    prompt = f'''
    Please help me solve this code with {java_problem['programming_language']}\n
        {java_problem['programming_problem_name']}\n
        This is the programming problems desc: {java_problem['desc']}\n
        This code contains a run-time error.\n
        {java_problem['additional_information']}
        {java_problem['solution']}
    '''
    java_prompt_data.append({"id": i, "programming_problem_name":java_problem["programming_problem_name"],"prompt": prompt, "extra error": ""})
    i += 1
    
with open('cpp_prompts.json', "w") as prompt_file:
    json.dump(prompt_data, prompt_file, indent=4)

with open('java_prompts.json', 'w') as prompt_file:
    json.dump(java_prompt_data, prompt_file, indent=4)
        