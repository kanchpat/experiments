from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import asyncio

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
    # Simulate network delay
    await asyncio.sleep(2)
    
    # Simulate random failure
    if random.random() < 0.2:
        raise HTTPException(
            status_code=500, 
            detail="North Pole internet connection frosty. Try again later."
        )
    
    transcript = f"""Ho ho ho! Merry Christmas! 
      
Well now, let me see... Ah, yes! {details.name}! I've been looking at my list.
      
I see you've been doing some wonderful things, like: {details.niceItems or 'being a good child'}. That's what I like to see!
      
Now, I also see a few things we might need to work on, like: {details.naughtyItems or 'nothing at all! You\\'ve been perfect'}. But don't worry, I know you'll try harder next year!
      
And about those gifts... I see you're wishing for {details.gifts}. Well, the elves and I will see what we can do! 
      
Keep being good, and I'll see you on Christmas Eve! Ho ho ho!"""
    
    return {"transcript": transcript}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
