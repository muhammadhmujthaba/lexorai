from groq import Groq

client = Groq(api_key="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")

models = client.models.list()

for m in models.data:
    print(m.id)
