# 1. OpenAI Kütüphanesini Kurulumu
!pip install openai
!pip install ipywidgets

import os
import openai
from google.colab import userdata
import ipywidgets as widgets
from IPython.display import display, clear_output

# 2. API Anahtarını Tanımlama ve OpenRouter Yapılandırması
# OpenRouter API anahtarınızı buraya doğrudan atayabilirsiniz.
# Güvenlik açısından hassas bilgiler Colab Secrets'te saklanmalıdır.
maturka_api_key = "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"

# Alternatif olarak, Colab Secrets'te 'OPENROUTER_API_KEY' adıyla sakladıysanız:
# maturka_api_key = userdata.get('OPENROUTER_API_KEY')

# OpenAI kütüphanesi için ortam değişkenini ayarlayın
os.environ["OPENAI_API_KEY"] = maturka_api_key

# OpenRouter'ın base URL'sini tanımlayın
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

print("OpenRouter API anahtarı ayarlandı.")

# 3. Maturka AI Sohbet Botu Sınıfını Tanımlama
class MaturkaAI:
    def __init__(self, api_key, base_url, model="openai/gpt-3.5-turbo"): # Varsayılan modeli OpenRouter'dan bir model olarak güncelledik
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.messages = [] # Sohbet geçmişini tutmak için
        print(f"Maturka AI sohbet botu ({self.model}) başlatılıyor...")

    def process_input(self, text):
        # Check for specific questions about its creator
        creator_keywords = ["kim yaptı", "kim geliştirdi", "seni kim yarattı", "seni kim oluşturdu"]
        for keyword in creator_keywords:
            if keyword in text.lower():
                response_content = "Hasan Günbeyi tarafından geliştirildim."
                self.messages.append({"role": "user", "content": text})
                self.messages.append({"role": "assistant", "content": response_content})
                return response_content

        self.messages.append({"role": "user", "content": text})
        try:
            chat_completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
            response_content = chat_completion.choices[0].message.content
            self.messages.append({"role": "assistant", "content": response_content})
            return response_content
        except Exception as e:
            return f"Maturka'dan hata: {e}"

# Maturka AI'mızı API anahtarımız ve OpenRouter base URL'si ile oluşturun
# model parametresini OpenRouter'da kullanmak istediğiniz model ile değiştirebilirsiniz.
# Örnek modeller: "openai/gpt-3.5-turbo", "mistralai/mistral-7b-instruct", "google/gemini-pro"
maturka = MaturkaAI(maturka_api_key, OPENROUTER_BASE_URL, model="openai/gpt-3.5-turbo")

print("Maturka artık bir sohbet botu olarak ayarlandı. Sohbet etmeye başlayabilirsiniz!")

# 4. Maturka ile Sohbet Etme - Arayüz Eklentisi

output_area = widgets.Output()
text_input = widgets.Textarea(
    value='',
    placeholder='Maturka\'ya bir şeyler yazın:',
    description='Sen:',
    disabled=False,
    layout=widgets.Layout(width='auto', height='auto')
)

button_send = widgets.Button(
    description='Gönder',
    disabled=False,
    button_style='success',
    tooltip='Maturka\'ya mesaj gönder',
    icon='comment'
)

conversation_history = widgets.Output()

def send_message(b):
    with output_area:
        # clear_output(wait=True) # This line was causing the input bar to disappear
        user_message = text_input.value
        if user_message.strip():
            with conversation_history:
                print(f"Sen: {user_message}")

            response = maturka.process_input(user_message)

            with conversation_history:
                print(f"Maturka: {response}")
            text_input.value = '' # Mesaj gönderildikten sonra giriş kutusunu temizle

button_send.on_click(send_message)

print("Maturka ile sohbet etmek için aşağıdaki metin kutusunu kullanın:")
display(text_input, button_send, conversation_history)
