# AI Avatar Text-to-Speech Animation System

A web application that synchronizes synthetic voice with facial animations using pre-trained Text-to-Speech (TTS) models and avatar animation services.

## 📋 Overview

This project creates a simplified version of an AI avatar system where:

- Text input is converted to speech using ElevenLabs' TTS API
- The generated speech is synchronized with facial animations using D-ID's animation API
- The result is a realistic avatar that speaks the provided text with appropriate facial movements

## 🔍 Live Demo & Usage

- **Live Demo**:
  <!-- [https://avatar-tts-demo.vercel.app](https://avatar-tts-demo.vercel.app) -->

  On the main page, enter text in the input field and click "Generate Avatar's Speech." The client will show the avatar speaking once the video is processed.

- **Presentation Page**:
  Navigate to `/presentation` to view a pre-recorded presentation video.

## 🛠️ Technology Stack

### Backend (Flask)

- Python Flask server with Socket.IO for real-time communication
- ElevenLabs API integration for high-quality text-to-speech
- D-ID API integration for facial animation
- RESTful API endpoints for handling text-to-speech generation and avatar animation

### Frontend (Next.js)

- Next.js React framework
- Socket.IO client for receiving real-time updates
- Responsive design for both desktop and mobile viewing
- Video playback with replay functionality
- History tracking for recent generations

## 🏗️ Processing Flow

### Direct Generation Flow (`/fast-generate` endpoint):

1. Client sends text to the Flask server
2. Server forwards text to D-ID which internally uses ElevenLabs for TTS
3. D-ID generates the avatar video and notifies server via webhook
4. Server notifies client via Socket.IO when the video is ready
5. Client displays the video with synchronized speech and facial animations

### Step-by-Step Generation Flow (`/generate` endpoint - for demonstration):

1. Client sends text to the Flask server
2. Server generates audio using ElevenLabs TTS API
3. Server sends audio URL to D-ID for avatar animation
4. D-ID generates the avatar video and notifies server via webhook
5. Server notifies client via Socket.IO when the video is ready
6. Client displays the video with synchronized speech and facial animations

## 📂 Project Structure

```
client/
├── public/
│   └── talks.mp4            # Demo video for presentation
├── src/
│   ├── components/
│   │   └── Avatar/
│   └── app/
│       ├── page.tsx         # Main page with avatar display and text input
│       ├── presentation/    # Page for demo video presentation
│       └── global.css       # Global styles
└── ...

server/
├── app.py                   # Flask application setup
├── config.py                # Configuration variables
├── run.py                   # Server entry point
├── create_speech.py         # Script for creating demo videos
├── routes/
│   ├── api.py               # API endpoint definitions
│   └── health.py            # Health check endpoint
└── services/
    ├── avatar_service.py    # D-ID API integration for avatar creation
    ├── fast_gen.py          # Direct D-ID integration with ElevenLabs
    └── tts_service.py       # ElevenLabs API integration for TTS
```

## 📊 Technical Implementation Details

### TTS Service

The TTS service uses ElevenLabs' API to generate high-quality speech from text. The service:

- Handles text validation and truncation
- Manages audio file storage with cleanup functionality
- Provides configurable voice settings including stability, similarity boost, and speed

### Avatar Service

The avatar service uses D-ID's API to generate animated videos. The service:

- Supports both audio-based and text-based animation
- Includes fallback mechanisms if audio validation fails
- Configures animation settings for fluency and stitching

### FastGen Service

The FastGen service combines TTS and animation in a single step:

- Sends text directly to D-ID with ElevenLabs provider configuration
- Improves performance by reducing API round-trips
- Maintains the same quality as the two-step process

### Real-time Updates

Socket.IO is used for real-time communication:

- Server emits events when videos are ready
- Client listens for events and updates the UI accordingly
- Provides a seamless user experience without polling

## 🔧 Setup and Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- ElevenLabs API key
- D-ID API key
- Ngrok (for local development to expose webhook endpoint)

### Backend Setup

1. Clone the repository

   ```bash
   git clone https://github.com/amanzoni1/avatar-tts.git
   cd avatar-tts/server
   ```

2. Create and activate a virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API keys

   ```
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   DID_API_KEY=your_did_api_key
   NGROK_URL=your_ngrok_url
   ```

5. Start the server
   ```bash
   python run.py
   ```

### Frontend Setup

1. Navigate to the client directory

   ```bash
   cd ../client
   ```

2. Install dependencies

   ```bash
   npm install
   ```

3. Start the development server

   ```bash
   npm run dev
   ```

4. Open your browser to `http://localhost:3003`

## 🙏 Acknowledgements

- [ElevenLabs](https://elevenlabs.io/) for providing the TTS API
- [D-ID](https://www.d-id.com/) for providing the avatar animation API
- [Next.js](https://nextjs.org/) and [Flask](https://flask.palletsprojects.com/) for the web frameworks

---

_This project was created as a technical task demonstration._
