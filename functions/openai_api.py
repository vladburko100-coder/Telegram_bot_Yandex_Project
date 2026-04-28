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
             "content": "Отвечай на русском языке, пиши только название города, без кавычек и других знаков. "
                        "Никаких дополнительных слов, эмодзи или пояснений. НЕ пиши 'Загадана страна: ...'."
                        " Только чистое название города."},
            {
                "role": "user",
                "content": "Загадай случайный город-миллионник из любой страны мира. "
                           "Напиши только название города на русском языке."
            },
        ],
    )
    result = completion.choices[0].message.content.strip()
    print(result)
    return result


def get_secret_country():
    client = OpenAI(api_key=TOKEN_OPEN_AI)

    completion = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {"role": "developer",
             "content": "Отвечай на русском языке, пиши только название страны, без кавычек и других знаков. "
                        "Никаких дополнительных слов, эмодзи или пояснений."
                        " НЕ пиши 'Загадана страна: ...'. Только чистое название страны."},
            {
                "role": "user",
                "content": "Загадай случайную страну мира. Напиши только название страны на русском языке."
            },
        ],
    )
    result = completion.choices[0].message.content
    print(result)
    return result


def get_help_from_ai(toponim, mode="city"):
    client = OpenAI(api_key=TOKEN_OPEN_AI)

    if mode == "city":
        prompt = (f"Тебе был загадан город: {toponim}."
                  f" Дай интересную подсказку об этом городе (население, достопримечательности, известные факты)."
                  f" Не называй город напрямую. Подсказка должна быть на русском языке, 1-2 предложения, без эмодзи.")
    else:
        prompt = (f"Тебе была загадана страна: {toponim}."
                  f" Дай интересную подсказку об этой стране (столица, язык, известные факты)."
                  f" Не называй страну напрямую. Подсказка должна быть на русском языке, 1-2 предложения, без эмодзи")

    completion = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {"role": "developer",
             "content": "Отвечай на русском языке, пиши только подсказку, без лишних слов,"
                        " можешь добавлять различные теги HTML для выделения важных слов"
                        " Не называй загаданный объект напрямую."},
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return completion.choices[0].message.content
