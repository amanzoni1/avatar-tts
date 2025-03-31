import React, { useRef, useEffect } from "react";
import Image from "next/image";
import styles from "../../app/page.module.css";

interface AvatarProps {
  videoUrl: string | null;
  isPlaying: boolean;
  onVideoEnd: () => void;
  onReplay: () => void;
}

const Avatar: React.FC<AvatarProps> = ({ videoUrl, isPlaying, onVideoEnd, onReplay }) => {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.play().catch((error) => {
          console.error("Error playing video:", error);
        });
      } else {
        videoRef.current.pause();
      }
    }
  }, [isPlaying]);

  // Wrap the content in a clickable container that calls onReplay when clicked
  if (!videoUrl) {
    return (
      <div className={styles.avatarContainer} onClick={onReplay}>
        <Image
          src="https://res.cloudinary.com/drvwan14l/image/upload/v1743239627/magen_igp4ts.png"
          alt="Default Avatar"
          className={styles.avatarMedia}
          width={400}
          height={400}
        />
      </div>
    );
  }

  return (
    <div className={styles.avatarContainer} onClick={onReplay}>
      <video
        ref={videoRef}
        src={videoUrl}
        className={styles.avatarMedia}
        onEnded={onVideoEnd}
        playsInline
      />
    </div>
  );
};

export default Avatar;
