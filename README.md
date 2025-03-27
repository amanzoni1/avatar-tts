# AI Avatar Text-to-Speech Animation

This project consists of a client-server application that creates animated avatars that speak text input using AI technology.

## Project Structure

- `client/`: Next.js frontend application
- `server/`: Flask backend application

## Setup Instructions

### Client Setup

1. Navigate to the client directory
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

### Server Setup

1. Navigate to the server directory
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask server:
   ```bash
   python app.py
   ```

## Features

- Text-to-speech conversion
- AI-powered avatar animation
- Real-time synchronization between speech and animation
