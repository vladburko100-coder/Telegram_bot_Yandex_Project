import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TOKEN_OPEN_AI = os.getenv("TOKEN_OPEN_AI")


def get_secret_city():
    client = OpenAI(api_key=TOKEN_OPEN_AI)

    completion = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {"role": "developer",
             "content": "Отвечай на русском языке, пиши только то что просят, НЕ пиши по типу:"
                        " Я загадал город..., нужно конкретно,"
                        " без эмодзи и других знаков препинания,"
                        " НЕ ПОВТОРЯЙ ОТВЕТЫ ИЗ ПРОШЛЫХ ЗАПРОСОВ! - НУЖНА УНИКАЛЬНОСТЬ ТВОИХ ОТВЕТОВ"
                        ", иначе умрет один котик"},
            {
                "role": "user",
                "content": "Загадай рандомный город миллионер из любой страны мира",
            },
        ],
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def get_help_from_ai(toponim):
    client = OpenAI(api_key=TOKEN_OPEN_AI)

    completion = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {"role": "developer",
             "content": "Отвечай на русском языке, пиши только то что просят,"
                        " без эмодзи, иначе умрет один котик"},
            {
                "role": "user",
                "content": f"Тебе был загадан город: {toponim}"
                           f" Подсказка должна быть интересной, но не слишком очевидной. Не называй город напрямую",
            },
        ],
    )
    return completion.choices[0].message.content
