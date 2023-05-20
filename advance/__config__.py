import os
from dotenv import load_dotenv

load_dotenv()

ALCHEMY_TOKEN = os.getenv("privateKeyToAccount") or os.getenv("ALCHEMY_TOKEN")

print("THIS IS ALCHEMY_TOKEN")
print(ALCHEMY_TOKEN)
BASE_URL = "eth-mainnet.g.alchemy.com/v2/"

CONTRACT_ADDRESS = "0xbaac2b4491727d78d2b78815144570b9f2fe8899"
