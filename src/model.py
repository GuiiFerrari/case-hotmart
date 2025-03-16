import os
import glob

from llama_cpp import Llama

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MODELS_PATH = os.path.join(BASE_PATH, "models")

models = glob.glob(os.path.join(MODELS_PATH, "*.gguf"))

LLAMA_MODEL_PATH = models[0]


class LLMModel:
    def __init__(self, temperature: float = 0.8, max_tokens: int = 1024):
        self._temperature = temperature
        self._max_tokens = max_tokens
        self.model = Llama(
            model_path=LLAMA_MODEL_PATH, max_tokens=self._max_tokens, n_ctx=10000
        )

    def ask_question(self, question: str, context: str = None):
        enhanced_question = (
            f"Background: \n{context}\n\nQuestion: {question}\n\nAnswer:"
            # if context
            # else question
        )
        return self.model(
            enhanced_question,
            temperature=self._temperature,
            stop=["Q:", "\n", "<|im_end|>", "</s>", "###"],
            stream=False,
            max_tokens=self._max_tokens,
        )

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value: float):
        self._temperature = value

    @property
    def max_tokens(self):
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, value: int):
        self._max_tokens = value


if __name__ == "__main__":
    model = LLMModel(temperature=0.0)
    response = model.ask_question("Qual a capital do Brasil?")
    print(response)
    print()
