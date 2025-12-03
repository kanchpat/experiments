from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import asyncio
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Add CORS support for Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChildDetails(BaseModel):
    name: str
    niceItems: str = ""
    naughtyItems: str = ""
    gifts: str

@app.post("/generate-transcript")
async def generate_transcript(details: ChildDetails):
    # Initialize Gemini
    try:
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = f"""Create a warm, jolly Santa Claus video message for a child named {details.name}. 
        
        Context:
        - Nice things they did: {details.niceItems or 'being a wonderful child'}
        - Naughty things (if any): {details.naughtyItems or 'nothing serious'}
        - Gifts they want: {details.gifts}
        
        Instructions:
        - Speak directly to the child.
        - Be encouraging about the nice things.
        - Gently mention the naughty things (if any) and encourage them to do better.
        - Mention the gifts they want and say you'll see what the elves can do.
        - Keep it under 2 minutes of speaking time.
        - Maintain a magical, jolly persona throughout.
        """
        
        response = model.generate_content(prompt)
        transcript = response.text
        
    except Exception as e:
        print(f"Error generating transcript: {e}")
        # Fallback to mock if API fails or key is missing
        transcript = f"""Ho ho ho! Merry Christmas! 
      
Well now, let me see... Ah, yes! {details.name}! I've been looking at my list.
      
I see you've been doing some wonderful things, like: {details.niceItems or 'being a good child'}. That's what I like to see!
      
Now, I also see a few things we might need to work on, like: {details.naughtyItems or "nothing at all! You've been perfect"}. But don't worry, I know you'll try harder next year!
      
And about those gifts... I see you're wishing for {details.gifts}. Well, the elves and I will see what we can do! 
      
Keep being good, and I'll see you on Christmas Eve! Ho ho ho!"""
    
    return {"transcript": transcript}

class VideoPrompt(BaseModel):
    prompt: str

@app.post("/generate-video")
async def generate_video(video_prompt: VideoPrompt):
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        
        print(f"Generating video for prompt: {video_prompt.prompt}")
        operation = client.models.generate_videos(
            model="veo-3.0-generate-001",
            prompt=video_prompt.prompt,
            config=types.GenerateVideosConfig(
                number_of_videos=1,
                duration_seconds=6,
            ),
        )
        
        # Poll for completion
        while not operation.done:
            await asyncio.sleep(5)
            operation = client.operations.get(operation)
            
        if operation.result:
            video_uri = operation.result.generated_videos[0].video.uri
            # Return a proxy URL instead of the direct URI
            return {"video_uri": f"/api/proxy-video?uri={video_uri}"}
        else:
            raise HTTPException(status_code=500, detail="Video generation failed")
            
    except Exception as e:
        print(f"Error generating video: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/proxy-video")
async def proxy_video(uri: str):
    try:
        import requests
        api_key = os.environ.get("GEMINI_API_KEY")
        # Append API key if not present (though usually passed in header or query)
        # The URI from Veo might already have it? No, usually not.
        # Let's try adding it as a query param if it's a googleapis URL
        
        target_url = uri
        if "googleapis.com" in uri and "key=" not in uri:
            target_url = f"{uri}&key={api_key}" if "?" in uri else f"{uri}?key={api_key}"
            
        # Stream the response
        def iterfile():
            with requests.get(target_url, stream=True) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=8192):
                    yield chunk
                    
        return StreamingResponse(iterfile(), media_type="video/mp4")
        
    except Exception as e:
        print(f"Error proxying video: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
