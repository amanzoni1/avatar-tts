"use client";

import React from "react";
import Link from "next/link";
import styles from "./page.module.css";

export default function Presentation() {
  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <h1 className={styles.title}>Presentation Video</h1>
        <div className={styles.subtitle}>
            <p>
            GitHub Repo: <a href="https://github.com/amanzoni1/avatar-tts" target="_blank" rel="noopener noreferrer">View Code</a> |
            Live Demo: <Link href="/">Watch Live</Link>
          </p>
        </div>
        <div className={styles.videoContainer}>
          <video controls width="100%" height="auto">
            <source src="/talks.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      </div>
    </main>
  );
}
