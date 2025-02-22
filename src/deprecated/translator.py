from util import deprecated
from openai import OpenAI
from cryption import CipherKey, Decrypt


@deprecated
class GptService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GptService, cls).__new__(cls)
            cls._instance._cipher = CipherKey()
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            dec = Decrypt(self._cipher)
            self.api_key = dec.decryption()
            self.client = OpenAI(api_key=self.api_key)
            self._initialized = True

    def _create_message(self, role, content):
        return {"role": role, "content": content}

    def kr_translator(self, role="user", content=""):
        if content:
            response = self.client.chat.completions.create(
                messages=[
                    self._create_message(
                        "system",
                        """You are an excellent Korean translator, and you can translate various languages, including English and German, into Korean.
                        Translate the English sentence sent by the user to Korean. and Return only the translated result in Korean. 
                        If the text is determined not to be in English, identify the appropriate language and translate it into Korean. 
                        If the text equal only language indicators like '[en]' or is empty, return an empty string.
                        You don't need to translate combinations of numbers and units like 5V, DC, 98mm.(in this case, return an empty string.)
                        """,
                    ),
                    self._create_message(role, content),
                ],
                model="gpt-4o-mini",
            )
            result = response.choices[0].message.content
            return result
        return ""
