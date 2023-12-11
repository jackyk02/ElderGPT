import together
together.api_key = "9f8e886eb131e97e1f010cab3ede5ed32dd955b1561005cfcb9d9aad6188c951"
prompt = "Who are you?"

output = together.Complete.create(
    prompt="[INST] " + prompt + " [/INST]",
    model="togethercomputer/llama-2-7b-chat",
    max_tokens=512,
    temperature=0.7,
    top_k=50,
    top_p=0.7,
    repetition_penalty=1,
    stop=[
        "[/INST]",
        "</s>"
    ]
)

print("Prompt: " + prompt)

# print generated text
print("Response: " + output['output']['choices'][0]['text'])
