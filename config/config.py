from dotenv import load_dotenv
import os

load_dotenv()

CLICKUP_TOKEN = os.getenv("CLICKTOKEN")
URL_CLICKUP = "https://api.clickup.com/api/v2"
HEADERS_TODO = {
    "Authorization": f"{CLICKUP_TOKEN}"
}
abs_path = os.path.abspath(__file__ + "../../../")
CLICKUP_ID = os.getenv("CLICKUPID")
CLICKUP_SECRET = os.getenv("CSECRET")
CODE_APP = os.getenv("CODE")

MAX_SPACES = 5
