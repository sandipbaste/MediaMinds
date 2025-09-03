from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_video(audio_path: str, text: str, file_id: str) -> str:
    """
    Create a video with audio and relevant text/images
    """
    try:
        # Load audio
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        # Create a simple video with text slides
        slides = create_text_slides(text, duration)
        
        # Create video clips for each slide
        clips = []
        for i, (slide_text, slide_duration) in enumerate(slides):
            # Create a simple text image
            img = create_text_image(slide_text)
            img_path = f"static/temp/temp_slide_{i}.png"
            os.makedirs(os.path.dirname(img_path), exist_ok=True)
            img.save(img_path)
            
            # Create clip
            clip = ImageClip(img_path, duration=slide_duration)
            clips.append(clip)
        
        # Concatenate clips
        video = concatenate_videoclips(clips)
        video = video.set_audio(audio)
        
        # Export video
        video_path = f"static/videos/{file_id}.mp4"
        os.makedirs(os.path.dirname(video_path), exist_ok=True)
        video.write_videofile(video_path, fps=24, codec='libx264', verbose=False, logger=None)
        
        # Clean up temporary files
        for i in range(len(slides)):
            temp_path = f"static/temp/temp_slide_{i}.png"
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
        return video_path
    
    except Exception as e:
        raise Exception(f"Error generating video: {str(e)}")

def create_text_slides(text: str, total_duration: float, max_slides: int = 10):
    """
    Split text into slides with appropriate durations
    """
    words = text.split()
    if not words:
        return [("No content", total_duration)]
    
    words_per_slide = max(1, len(words) // max_slides)
    
    slides = []
    for i in range(0, len(words), words_per_slide):
        slide_text = " ".join(words[i:i+words_per_slide])
        # Calculate duration for this slide (proportional to text length)
        duration = (len(slide_text) / len(text)) * total_duration
        slides.append((slide_text, min(duration, 10)))  # Max 10 seconds per slide
    
    return slides

def create_text_image(text: str, width: int = 1280, height: int = 720):
    """
    Create an image with text on it
    """
    # Create a blank image
    img = Image.new('RGB', (width, height), color=(30, 30, 60))
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fall back to default
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        try:
            font = ImageFont.load_default()
        except:
            font = None
    
    # Wrap text
    margin = 50
    max_width = width - 2 * margin
    lines = textwrap.wrap(text, width=60)
    
    # Draw text
    y = margin
    for line in lines:
        if font:
            draw.text((margin, y), line, font=font, fill=(255, 255, 255))
        else:
            draw.text((margin, y), line, fill=(255, 255, 255))
        y += 40
        if y > height - margin:
            break
    
    return img