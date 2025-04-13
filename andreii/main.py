from pyrogram import Client, filters
import asyncio
import os
import requests

app = Client("pyrogi/my_account_PC")
username = "Andrei_hooh"

# Хранилище контекста для пользователей
user_histories = {}

@app.on_message(filters.text & filters.private)
async def response(client, message):
    if message.from_user.username == username:
        user_id = message.from_user.id
        await asyncio.sleep(3)
        # Инициализируем историю сообщений для пользователя, если ещё не создана
        if user_id not in user_histories:
            user_histories[user_id] = [
                {
                    "role": "system",
                    "content": "Вы - обычный человек, довольно остроумный, не используй эмодзи и не говори что ты ИИ, тот с кем ты говоришь этого не знает",
                }
            ]

        # Добавляем новое пользовательское сообщение
        user_histories[user_id].append({
            "role": "user",
            "content": message.text,
        })

        # ⚠️ API-ключ OpenRouter
        api_key = "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"  # начинающийся с "sk-or-"
        api_key2 = "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"    
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "MyApp",
        }

        data = {
            "model": "google/learnlm-1.5-pro-experimental:free",
            "messages": user_histories[user_id],  # передаём весь диалог
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

        if response.ok:
            result = response.json()
            reply_text = result["choices"][0]["message"]["content"]
            print(result)
            # Добавляем ответ бота в историю
            user_histories[user_id].append({
                "role": "assistant",
                "content": reply_text,
            })

            await message.reply_text(reply_text)
        else:
            print("Ошибка:", response.status_code, response.text)

app.run()
