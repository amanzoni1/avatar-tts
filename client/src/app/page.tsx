'use client';

import { useState, useRef } from 'react';
import axios from 'axios';

export default function Home() {
  const [text, setText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [isAudioLoading, setIsAudioLoading] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setIsPlaying(false);
    setIsAudioLoading(true);

    try {
      const response = await axios.post('http://localhost:5003/api/tts',
        { text },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.data.success && response.data.audio_url) {
        // Set the audio source and play it
        if (audioRef.current) {
          audioRef.current.src = response.data.audio_url;
          audioRef.current.play().catch(err => {
            console.error('Audio playback error:', err);
            setError('Failed to play audio. Please try again.');
          });
          setIsPlaying(true);
        }
      }

    } catch (err) {
      setError('Failed to generate speech. Please try again.');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play().catch(err => {
          console.error('Audio playback error:', err);
          setError('Failed to play audio. Please try again.');
        });
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleAudioEnded = () => {
    setIsPlaying(false);
    setIsAudioLoading(false);
  };

  const handleAudioError = (e: React.SyntheticEvent<HTMLAudioElement, Event>) => {
    console.error('Audio error:', e);
    setError('Failed to load audio. Please try again.');
    setIsAudioLoading(false);
  };

  const handleAudioLoadStart = () => {
    setIsAudioLoading(true);
  };

  const handleAudioCanPlay = () => {
    setIsAudioLoading(false);
  };

  return (
    <main>
      <div className="container">
        <h1 className="title">
          AI Avatar Text-to-Speech
        </h1>

        <div className="card">
          <form onSubmit={handleSubmit} className="form">
            <div className="form-group">
              <label htmlFor="text" className="label">
                Enter text to convert to speech
              </label>
              <textarea
                id="text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="textarea"
                placeholder="Type your text here..."
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="button"
            >
              {isLoading ? 'Generating...' : 'Generate Speech'}
            </button>

            {error && (
              <p className="error">{error}</p>
            )}
          </form>

          <div className="avatar-section">
            <h2 className="avatar-title">Avatar Display Area</h2>
            <div className="avatar-container">
              <p className="avatar-placeholder">Avatar will be displayed here</p>
            </div>
          </div>

          {/* Audio Controls */}
          <div className="audio-controls">
            <button
              onClick={handlePlayPause}
              disabled={!audioRef.current?.src || isLoading || isAudioLoading}
              className="button"
            >
              {isAudioLoading ? 'Loading...' : isPlaying ? 'Pause' : 'Play'}
            </button>
          </div>

          {/* Hidden Audio Element */}
          <audio
            ref={audioRef}
            onEnded={handleAudioEnded}
            onError={handleAudioError}
            onLoadStart={handleAudioLoadStart}
            onCanPlay={handleAudioCanPlay}
            style={{ display: 'none' }}
          />
        </div>
      </div>
    </main>
  );
}
