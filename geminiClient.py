from google import genai

def clienteLLM(request : str) -> str:
    client = genai.Client(api_key="Aqui va tu API Key de Gemini")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=request,
    )
    return(response.text)