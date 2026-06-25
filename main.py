import asyncio
import os
import google.generativeai as genai

GEMINI_KEY = os.environ.get("GEMINI_KEY", "AQ.Ab8RN6KVemeou-4WuXE1E-BjZoD04xGg-f4hF1kOP8-a_xVjPw")
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_fact():
    print("🧠 توليد معلومة غريبة...")
    response = model.generate_content("اكتب معلومة غريبة وطريفة بالعربية في 4 جمل")
    return response.text

def verify_fact(fact):
    print("✅ مراجعة صحة المعلومة...")
    response = model.generate_content(f"هل هذه المعلومة صحيحة علمياً؟ أجب بكلمة واحدة صحيحة أو غير صحيحة:\n{fact}")
    return response.text

async def text_to_speech(text, output_file="voice.mp3"):
    print("🎙️ تحويل النص لصوت...")
    import edge_tts
    communicate = edge_tts.Communicate(text, "ar-SA-ZariyahNeural")
    await communicate.save(output_file)
    return output_file

def create_video(fact_text, audio_file, output_file="short.mp4"):
    print("🎬 إنشاء الفيديو...")
    from moviepy import AudioFileClip, TextClip, CompositeVideoClip, ColorClip
    audio = AudioFileClip(audio_file)
    bg = ColorClip(size=(1080, 1920), color=(10, 10, 40), duration=audio.duration)
    txt = TextClip(text=fact_text[:300], font_size=55, color='white', size=(900, None), method='caption', duration=audio.duration).with_position('center')
    video = CompositeVideoClip([bg, txt]).with_audio(audio)
    video.write_videofile(output_file, fps=24, logger=None)
    return output_file

async def run_pipeline():
    print("🚀 بدء Pipeline...\n")
    fact = generate_fact()
    verify_fact(fact)
    audio = await text_to_speech(fact[:500])
    video = create_video(fact, audio)
    print("\n✅ الفيديو جاهز:", video)

if __name__ == "__main__":
    asyncio.run(run_pipeline())
