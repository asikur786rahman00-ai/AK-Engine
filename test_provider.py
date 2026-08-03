from ak_engine.providers.universal_provider import UniversalProvider

provider = UniversalProvider()

reply = provider.chat("Reply with exactly: Hermes is alive!")

print(reply)
