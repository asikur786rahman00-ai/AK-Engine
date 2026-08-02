from ak_engine.providers.gemini import GeminiProvider

provider = GeminiProvider()

reply = provider.chat(
    "Say exactly: Hello AK! Your engine is alive!"
)

print(reply)
