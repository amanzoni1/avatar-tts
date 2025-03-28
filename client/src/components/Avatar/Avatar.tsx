import React, { useRef, useEffect } from 'react';

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
        videoRef.current.play().catch(error => {
          console.error('Error playing video:', error);
        });
      } else {
        videoRef.current.pause();
      }
    }
  }, [isPlaying]);

  if (!videoUrl) {
    return (
      <img
        src="https://d-id-public-bucket.s3.us-west-2.amazonaws.com/alice.jpg"
        alt="Default Avatar"
        className="w-full h-full object-contain"
      />
    );
  }

  return (
    <video
      ref={videoRef}
      src={videoUrl}
      className="w-full h-full object-contain"
      onEnded={onVideoEnd}
      playsInline
    />
  );
};

export default Avatar;
