class ClientConstants:
    CUSTOMER_KEY_DATALINK = "dentalink"
    BASE_URL_DENTALINK = "https://api.dentalink.healthatom.com/api/v1/citas/"
    ERROR_REQUIRED_KEYWORD = "Keyword {keyword} is required"
    DENTALINK_CONFIRM_STATUS_ID = 3  # api/v1/citas/estados/3
    DENTALINK_CANCEL_STATUS_ID = 1  # api/v1/citas/estados/1
    ENV_KEY_DENTALINK_TOKEN = "DENTALINK_TOKEN"
    KEYWORD_DENTALINK_TOKEN = "token"
    ENV_KEY_TO_KEYWORD = {ENV_KEY_DENTALINK_TOKEN: KEYWORD_DENTALINK_TOKEN}
