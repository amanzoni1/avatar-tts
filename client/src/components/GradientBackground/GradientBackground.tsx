"use client";

import React, { useEffect, useRef } from "react";
import styles from "./GradientBackground.module.css";

const GradientBackground: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const colors = [
      "#FFA500", // Orange
      "#FFD700", // Gold/Yellow
      "#FF69B4", // Hot Pink
      "#6A5ACD", // SlateBlue (purple-blue)
    ];

    const drawGradient = () => {
      const width = canvas.width;
      const height = canvas.height;

      ctx.clearRect(0, 0, width, height);

      const gradient = ctx.createLinearGradient(0, 0, width, height * 0.6);
      colors.forEach((color, index) => {
        gradient.addColorStop(index / (colors.length - 1), color);
      });

      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, width, height);

      // Draw angled bottom edge
      ctx.beginPath();
      ctx.moveTo(0, height);
      ctx.lineTo(width, height * 0.9);
      ctx.lineTo(width, height);
      ctx.closePath();
      ctx.fillStyle = "#ebeef1";
      ctx.fill();
    };

    const handleResize = () => {
      if (canvas) {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
        drawGradient();
      }
    };

    window.addEventListener("resize", handleResize);
    handleResize();

    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return <canvas ref={canvasRef} className={styles.gradientCanvas} />;
};

export default GradientBackground;
