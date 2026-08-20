"""
Simple Ollama connectivity test.
"""

from src.llm.ollama_client import OllamaClient


def main() -> None:
    client = OllamaClient()

    response = client.generate(
        "Say hello in one short sentence."
    )

    print("\nOllama Response:\n")
    print(response)


if __name__ == "__main__":
    main()
