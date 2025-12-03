import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [name, setName] = useState('')
  const [naughtyItems, setNaughtyItems] = useState('')
  const [niceItems, setNiceItems] = useState('')
  const [gifts, setGifts] = useState('')
  const [transcript, setTranscript] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [videoUri, setVideoUri] = useState('')
  const [videoLoading, setVideoLoading] = useState(false)
  const [currentImageIndex, setCurrentImageIndex] = useState(0)

  const images = ['/santa1.png', '/santa2.png', '/santa3.png']

  useEffect(() => {
    let interval;
    if (transcript) {
      interval = setInterval(() => {
        setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length)
      }, 4000)
    }
    return () => clearInterval(interval)
  }, [transcript, images.length])

  const generateTranscript = async (e) => {
    e.preventDefault()
    setLoading(true)
    setTranscript('')
    setError('')

    try {
      const response = await fetch('/api/generate-transcript', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          niceItems,
          naughtyItems,
          gifts,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to generate transcript')
      }

      const data = await response.json()
      setTranscript(data.transcript)

      // Start video generation in parallel
      setVideoLoading(true)
      fetch('/api/generate-video', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: "Santa Claus in a joyous mood, background with elves packing gifts, cinematic style, high quality, 4k"
        }),
      })
        .then(res => res.json())
        .then(data => {
          if (data.video_uri) {
            setVideoUri(data.video_uri)
          }
        })
        .catch(err => console.error("Video generation failed:", err))
        .finally(() => setVideoLoading(false))

    } catch (err) {
      setError(err.message || 'An error occurred. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <header className="header">
        <h1>Santa Wishing Machine</h1>
        <div className="status-indicators">
          <span className="status-item"><span className="dot green"></span> Connected</span>
          <span className="status-item">Voice: Santa</span>
          <span className="status-item">Persona: Jolly</span>
        </div>
      </header>

      <main className="main-content">
        {!transcript ? (
          <div className="card input-card">
            <h2>Child's Details</h2>
            {error && <div className="error-message">{error}</div>}
            <form onSubmit={generateTranscript}>
              <div className="form-group">
                <label htmlFor="name">Child's Name</label>
                <input
                  type="text"
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  placeholder="Enter child's name"
                />
              </div>
              <div className="form-group">
                <label htmlFor="niceItems">Nice Things Done</label>
                <textarea
                  id="niceItems"
                  value={niceItems}
                  onChange={(e) => setNiceItems(e.target.value)}
                  placeholder="What good things did they do?"
                  rows="3"
                />
              </div>
              <div className="form-group">
                <label htmlFor="naughtyItems">Naughty Things Done</label>
                <textarea
                  id="naughtyItems"
                  value={naughtyItems}
                  onChange={(e) => setNaughtyItems(e.target.value)}
                  placeholder="Any naughty things?"
                  rows="3"
                />
              </div>
              <div className="form-group">
                <label htmlFor="gifts">Gift Wishes</label>
                <textarea
                  id="gifts"
                  value={gifts}
                  onChange={(e) => setGifts(e.target.value)}
                  required
                  placeholder="What would they like for Christmas?"
                  rows="3"
                />
              </div>
              <button type="submit" disabled={loading}>
                {loading ? 'Consulting Santa...' : 'Generate Video Transcript'}
              </button>
            </form>
          </div>
        ) : (
          <div className="full-screen-video">
            <div className="video-container">
              <div className="video-player">
                  {videoUri ? (
                    <video
                      src={videoUri}
                      controls
                      autoPlay
                      loop
                      className="santa-video"
                    />
                  ) : (
                    <div className="video-placeholder">
                      {videoLoading ? (
                        <div className="loading-state">
                          <div className="spinner"></div>
                          <p>Generating magical video from the North Pole... (this may take a minute)</p>
                        </div>
                      ) : (
                        images.map((img, index) => (
                          <img
                            key={img}
                            src={img}
                            alt="Santa"
                            className={`santa-image ${index === currentImageIndex ? 'active' : ''}`}
                          />
                        ))
                      )}
                    </div>
                  )}
                <div className="transcript-overlay">
                  <p>{transcript}</p>
                </div>
              </div>
            </div>
              <button className="back-button" onClick={() => {
                setTranscript('')
                setVideoUri('')
              }}>
              Create Another Message
            </button>
          </div>
        )}
      </main>
      <footer className="footer">
        <p>Want to see where Santa is right now? <a href="https://santatracker.google.com/" target="_blank" rel="noopener noreferrer">Check the Santa Tracker!</a></p>
      </footer>
    </div>
  )
}

export default App
