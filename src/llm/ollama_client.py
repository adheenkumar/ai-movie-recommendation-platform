"""
Ollama client.

Provides a reusable interface for interacting
with a locally running Ollama server.
"""

from __future__ import annotations

from ollama import Client

from src.utils.logger import get_logger

logger = get_logger(__name__)


class OllamaClient:
    """
    Wrapper around the Ollama Python client.
    """

    def __init__(
        self,
        model: str = "llama3.2:3b",
        host: str = "http://localhost:11434",
    ) -> None:
        """
        Initialize the Ollama client.

        Parameters
        ----------
        model:
            Default model name.

        host:
            Ollama server URL.
        """

        self.model = model
        self.client = Client(host=host)

        logger.info(
            "Ollama client initialized | model=%s",
            model,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from Ollama.

        Parameters
        ----------
        prompt:
            Prompt sent to the model.

        Returns
        -------
        str
            Generated response.
        """

        logger.info("Sending prompt to Ollama.")

        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            options={
                "temperature": 0.2,
                "num_predict": 600,
            },
        )

        logger.info("Received response from Ollama.")

        return response["response"].strip()
