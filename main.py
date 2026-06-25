import asyncio
import os
from ollamafreeapi import OllamaFreeAPI

def generate_fact():
    print("🧠 توليد معلومة غريبة...")
    api = OllamaFreeAPI()
    prompt = """اكتب معلومة غريبة وطريفة ومثيرة للاهتمام.
الشكل:
- العنوان: جملة قصيرة جذابة
- المعلومة: شرح بـ 3-4 جمل
- مثال: مثال توضيحي
اكتب بالعربية فقط."""
    response = api.chat(model='llama3:latest', prompt=prompt)
    print(f"✅ المعلومة: {response[:100]}...")
    return response

def verify_fact(fact):
    print("✅ مراجعة صحة المعلومة...")
    api = OllamaFreeAPI()
    prompt = f"""راجع هذه المعلومة وقل هل هي صحيحة:
{fact}
أجب بـ:
- الحكم: صحيحة / غير صحيحة
- السبب: جملة واحدة"""
    response = api.chat(model='llama3:latest', prompt=prompt)
    return response

async def text_to_speech(text, output_file="voice.mp3"):
    print("🎙️ تحويل النص لصوت...")
    import edge_tts
    voice = "ar-SA-ZariyahNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    return output_file

def create_video(fact_text, audio_file, output_file="short.mp4"):
    print("🎬 إنشاء الفيديو...")
    from moviepy import AudioFileClip, TextClip, CompositeVideoClip, ColorClip
    audio = AudioFileClip(audio_file)
    duration = audio.duration
    background = ColorClip(size=(1080, 1920), color=(10, 10, 40), duration=duration)
    txt_clip = TextClip(
        text=fact_text[:300],
        font_size=55,
        color='white',
        size=(900, None),
        method='caption',
        duration=duration
    ).with_position('center')
    video = CompositeVideoClip([background, txt_clip])
    video = video.with_audio(audio)
    video.write_videofile(output_file, fps=24, logger=None)
    return output_file

async def run_pipeline():
    print("🚀 بدء Pipeline...\n")
    fact = generate_fact()
    verification = verify_fact(fact)
    if "غير صحيحة" in verification:
        fact = generate_fact()
    audio = await text_to_speech(fact[:500])
    video = create_video(fact, audio)
    print("\n✅ الفيديو جاهز:", video)
    return video

if __name__ == "__main__":
    asyncio.run(run_pipeline())
