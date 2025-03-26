import os
import json
import openai

# Set the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_query(user_input):
    try:
        response = openai.ChatCompletion.create(
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

        # Extract the content from the AI response
        content = response["choices"][0]["message"]["content"]
        print("🤖 AI Response:", content)

        # Parse the returned JSON
        parsed = json.loads(content)
        return parsed.get("city", ""), parsed.get("state", ""), parsed.get("cuisine", ""), parsed.get("price", "")

    except Exception as e:
        print("❌ Error parsing query with OpenAI:", e)
        return "", "", "", ""
