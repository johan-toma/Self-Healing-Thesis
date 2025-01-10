import openai
import json

openai.api_key = "placeholder"
model = "gpt-4o-mini"
max_tokens = 1200
temperature = 1

cpp_corrected_solutions = []
java_corrected_solutions = []
with open('cpp_prompts.json', 'r') as file:
    cpp_prompts = json.load(file)
with open('java_prompts.json', 'r') as file:
    java_prompts = json.load(file)
    

sys_prompts = '''I have a set of programming problems with provided solutions, each of these solutions contains run-time errors 
For each problem, please analyze the code to identify the source of the error and fix it. Provide a corrected version of the solution given. 
For each problem only give the code solution in response, do not give any details regarding to what was fixed, why and how.
'''

for prompt in cpp_prompts:
    text = prompt['prompt']
    
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages= [{"role":"user", "content":sys_prompts},{"role":"user","content":text}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        solution = response['choices'][0]['message']['content']
        cpp_corrected_solutions.append({
            "id":prompt["id"],
            "programming_problem_name": prompt["programming_problem_name"],
            "fixed_solution" : solution
        })
    except Exception as Error:
        print(f"Error processing prompt ID {prompt['id']}: {Error}")
        cpp_corrected_solutions.append({
            "id": prompt["id"],
            "programming_problem_name": prompt["programming_problem_name"],
            "error": str(Error)
        })
    else:
        print(f"Successfully processed cpp prompt ID {prompt['id']}")

for prompt in java_prompts:
    text = prompt['prompt']
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages= [{"role":"user", "content":sys_prompts},{"role":"user","content":text}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        solution = response['choices'][0]['message']['content']
        java_corrected_solutions.append({
            "id":prompt["id"],
            "programming_problem_name": prompt["programming_problem_name"],
            "fixed_solution" : solution
        })
    except Exception as Error:
        print(f"Error processing cpp prompt ID {prompt['id']}: {Error}")
        java_corrected_solutions.append({
            "id": prompt["id"],
            "programming_problem_name": prompt["programming_problem_name"],
            "error": str(Error)
        })
    else:
        print(f"Successfully processed java prompt ID {prompt['id']}")

with open("gpt4omini_cpp_fixed_solutions.json", "w") as output:
    json.dump(cpp_corrected_solutions, output, indent=4)
with open("gpt4omini_java_fixed_solutions.json", "w") as output:
    json.dump(java_corrected_solutions, output, indent=4)

print("Finished two files created: gpto1_cpp_fixed_solutions.json and gpto1_java_fixed_solutions.json")
