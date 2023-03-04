import openai
from google.cloud import texttospeech
import io
import os

# 初始化OpenAI和Google Text-to-Speech客户端
openai.api_key = "YOUR_OPENAI_API_KEY"
client = texttospeech.TextToSpeechClient()

# 定义函数，用于生成播客内容并将其转换为语音
def generate_podcast(title):
    # 使用OpenAI的GPT API生成播客文本
    prompt = "生成一期题目为'" + title + "'的播客"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )
    podcast_text = response.choices[0].text.strip()

    # 使用Google Text-to-Speech将播客文本转换为语音
    synthesis_input = texttospeech.SynthesisInput(text=podcast_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # 将生成的音频文件保存到本地
    with open("podcast.mp3", "wb") as out:
        out.write(response.audio_content)

    print("播客生成完成！")

# 在主程序中调用函数并传入播客题目
generate_podcast("YOUR_PODCAST_TITLE")
