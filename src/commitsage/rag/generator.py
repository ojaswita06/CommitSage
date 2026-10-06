import ollama


class LLMGenerator:
    def __init__(self):
        self.model = "qwen2.5:3b"

    def generate(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]