"use client";

import { useState } from "react";
import axios from "axios";
import styles from "./page.module.css";
import Avatar from "../components/Avatar/Avatar";

interface AvatarResponse {
  talk_id: string;
  status: string;
  result_url?: string;
}

interface VideoHistoryItem {
  url: string;
  text: string;
}

export default function Home() {
  const [text, setText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [videoHistory, setVideoHistory] = useState<VideoHistoryItem[]>([]);
  const maxChars = 350;

  // Function to poll the GET endpoint for talk status.
  const pollTalkStatus = async (talkId: string, inputText: string) => {
    const SERVER_URL = "http://localhost:5003";
    let elapsed = 0;
    const timeout = 120; // seconds
    const pollInterval = 10; // seconds

    while (elapsed < timeout) {
      try {
        const res = await axios.get<AvatarResponse>(`${SERVER_URL}/api/talk/${talkId}`);
        const status = res.data.status;
        console.log("Talk status:", status);
        if (status === "done" && res.data.result_url) {
          const videoUrl = res.data.result_url;
          setVideoUrl(videoUrl);
          setIsPlaying(true);

          // Update history if valid URL.
          setVideoHistory((prev) => {
            const newHistory = [
              { url: videoUrl, text: inputText },
              ...prev,
            ].slice(0, 3);
            return newHistory;
          });
          return;
        }
      } catch (err) {
        console.error("Failed to fetch talk status:", err);
      }
      await new Promise((resolve) => setTimeout(resolve, pollInterval * 1000));
      elapsed += pollInterval;
    }
    setError("Timed out waiting for avatar video.");
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;

    setIsLoading(true);
    setError("");
    setVideoUrl(null);
    setIsPlaying(false);

    const SERVER_URL = "http://localhost:5003";
    try {
      const response = await axios.post<AvatarResponse>(
        `${SERVER_URL}/api/generate`,
        { text },
        { headers: { "Content-Type": "application/json" } }
      );

      if (response.data.talk_id) {
        console.log("Talk ID:", response.data.talk_id);
        await pollTalkStatus(response.data.talk_id, text);
      } else {
        setError("Avatar generation failed.");
      }
    } catch (err: any) {
      console.error("Error during generation:", err);
      setError("Generation error. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReplay = (url: string) => {
    setVideoUrl(url);
    setIsPlaying(true);
  };

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <h1 className={styles.title}>AI Avatar Text-to-Speech</h1>

        {/* Subtitle placed right under the title */}
        <div className={styles.subtitle}>
          <p>
            GitHub Repo: <a href="https://github.com/amanzoni1/avatar-tts" target="_blank" rel="noopener noreferrer">View Code</a> |
            Short Video: <a href="https://youtu.be/yourvideoid" target="_blank" rel="noopener noreferrer">Watch Presentation</a>
          </p>
        </div>

        <div className={styles.twoColumn}>
          {/* Left Column: Avatar container */}
          <div className={styles.avatarContainer}>
            <Avatar
              videoUrl={videoUrl}
              isPlaying={isPlaying}
              onVideoEnd={() => setIsPlaying(false)}
              onReplay={() => videoUrl && handleReplay(videoUrl)}
            />
          </div>

          {/* Right Column: Form container */}
          <div className={styles.formContainer}>
            <form onSubmit={handleGenerate} className={styles.form}>
              <div className={styles.formGroup}>
                <label htmlFor="text" className={styles.label}>
                  Enter text to convert to speech
                </label>
                <textarea
                  id="text"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  className={styles.textarea}
                  placeholder="Type your text here..."
                  maxLength={maxChars}
                />
                <p className={styles.charCounter}>{text.length} / {maxChars}</p>
              </div>
              <div className={styles.buttonRow}>
                <button
                  type="submit"
                  disabled={isLoading || !text.trim()}
                  className={styles.generateButton}
                >
                  {isLoading ? "Generating..." : "Generate Avatar's Speech"}
                </button>
              </div>
              {error && <p className={styles.error}>{error}</p>}

              {/* History Section */}
              {videoHistory.length > 0 && (
                <div className={styles.historySection}>
                  <h3 className={styles.historyTitle}>Recent Generations</h3>
                  <div className={styles.historyList}>
                    {videoHistory.map((video, index) => (
                      <button
                        key={index}
                        onClick={() => handleReplay(video.url)}
                        className={styles.historyButton}
                        title={video.text}
                        type="button"
                      >
                        <span className={styles.replayIcon}>↺</span>
                        <span className={styles.historyText}>
                          {video.text.length > 30 ? `${video.text.slice(0, 30)}...` : video.text}
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </form>
          </div>
        </div>
      </div>
    </main>
  );
}
