import google.generativeai as genai

genai.configure(api_key="AIzaSyD7t8EeFcNc33sbDbO5Uyci1_GZX98ZWEs")  # Replace with your valid API key

model = genai.GenerativeModel("gemini-1.5-pro")  # Use a correct model name
response = model.generate_content("Hello, Gemini!")
print(response.text)









#import google.generativeai as genai

#genai.configure(api_key="your-valid-api-key")

#models = genai.list_models()
#print("Available models:", [model.name for model in models])

