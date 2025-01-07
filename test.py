# Google PaLM API 
import google.generativeai as palm
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]

model = models[1].name
print("We will be using model:", model)