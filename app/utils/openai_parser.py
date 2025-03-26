import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_query(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that extracts restaurant search criteria from user input. "
                        "Extract the city, state (2-letter abbreviation), cuisine, and optional price level (1 to 4). "
                        "Respond ONLY in JSON format like: "
                        "{\"city\": \"Austin\", \"state\": \"TX\", \"cuisine\": \"Tacos\", \"price\": \"2\"}"
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        content = response.choices[0].message.content
        print("🤖 AI Response:", content)

        parsed = json.loads(content)
        return parsed.get("city", ""), parsed.get("state", ""), parsed.get("cuisine", ""), parsed.get("price", "")

    except Exception as e:
        print("❌ Error parsing query with OpenAI:", e)
        return "", "", "", ""
