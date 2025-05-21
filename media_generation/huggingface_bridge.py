"""
HuggingFace Bridge for Media Generation

This module provides integration with HuggingFace's models for generating
audio, images, and short video clips for the NerdsCourt system.
"""

import os
import io
import base64
import time
import uuid
import requests
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Get HuggingFace API token
HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

class HuggingFaceBridge:
    """Bridge to HuggingFace's models for media generation."""

    def __init__(self, api_token=None):
        """
        Initialize the HuggingFace bridge.

        Args:
            api_token: HuggingFace API token (defaults to env var)
        """
        self.api_token = api_token or HF_API_TOKEN

        if not self.api_token:
            raise ValueError("HuggingFace API token must be provided")

        self.headers = {
            "Authorization": f"Bearer {self.api_token}"
        }

    def generate_audio(self, text, voice="en_male_deep", output_path=None, use_dia=True):
        """
        Generate audio from text using HuggingFace's text-to-speech models.

        Args:
            text: Text to convert to speech
            voice: Voice to use (default: en_male_deep)
            output_path: Path to save the audio file (optional)
            use_dia: Whether to use the Dia model (default: True)

        Returns:
            str: Path to the generated audio file or base64-encoded audio data
        """
        if use_dia:
            return self.generate_audio_dia(text, voice, output_path)
        else:
            return self.generate_audio_speecht5(text, voice, output_path)

    def generate_audio_dia(self, text, voice="en_male_deep", output_path=None):
        """
        Generate audio from text using the Dia 1.6B model.

        Args:
            text: Text to convert to speech
            voice: Voice preset to use (default: en_male_deep)
            output_path: Path to save the audio file (optional)

        Returns:
            str: Path to the generated audio file or base64-encoded audio data
        """
        # Use Dia 1.6B model for ultra-high-quality TTS
        API_URL = "https://api-inference.huggingface.co/spaces/nari-labs/Dia-1-6B"

        # Map our voice presets to Dia-compatible presets
        voice_map = {
            "en_male_deep": "Narrator",
            "en_male_confident": "Confident",
            "en_male_authoritative": "Authoritative",
            "en_male_neutral": "Neutral",
            "en_female_emotional": "Emotional",
            "en_female_neutral": "Neutral Female"
        }

        dia_voice = voice_map.get(voice, "Narrator")

        # Prepare payload
        payload = {
            "data": [
                text,
                dia_voice,
                1.0,  # Temperature
                1.0,  # Top P
                1.0,  # Typical P
                1.0,  # Repetition Penalty
                44100,  # Sample Rate
                False,  # Use Streaming
                ""  # Custom Voice
            ]
        }

        try:
            # Make request to HuggingFace Spaces API
            response = requests.post(
                f"{API_URL}/run/predict",
                headers={"Authorization": f"Bearer {self.api_token}"},
                json=payload
            )
            response.raise_for_status()

            # Parse the response
            result = response.json()

            # The response contains a data field with the audio file URL
            if "data" in result and len(result["data"]) > 0:
                audio_url = result["data"][0]

                # Download the audio file
                audio_response = requests.get(audio_url)
                audio_response.raise_for_status()
                audio_data = audio_response.content

                # Save to file if output_path is provided
                if output_path:
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(audio_data)
                    return output_path

                # Otherwise, return base64-encoded audio data
                return base64.b64encode(audio_data).decode("utf-8")
            else:
                print(f"Error generating audio with Dia: {result}")
                return None

        except Exception as e:
            print(f"Error generating audio with Dia: {e}")
            # Fall back to SpeechT5 if Dia fails
            return self.generate_audio_speecht5(text, voice, output_path)

    def generate_audio_speecht5(self, text, voice="en_male_deep", output_path=None):
        """
        Generate audio from text using the SpeechT5 model.

        Args:
            text: Text to convert to speech
            voice: Voice to use (default: en_male_deep)
            output_path: Path to save the audio file (optional)

        Returns:
            str: Path to the generated audio file or base64-encoded audio data
        """
        # Use SpeechT5 model for high-quality TTS
        API_URL = "https://api-inference.huggingface.co/models/microsoft/speecht5_tts"

        # Prepare payload
        payload = {
            "inputs": text,
            "parameters": {
                "voice": voice
            }
        }

        try:
            # Make request to HuggingFace API
            response = requests.post(API_URL, headers=self.headers, json=payload)
            response.raise_for_status()

            # Get audio data
            audio_data = response.content

            # Save to file if output_path is provided
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                return output_path

            # Otherwise, return base64-encoded audio data
            return base64.b64encode(audio_data).decode("utf-8")

        except Exception as e:
            print(f"Error generating audio with SpeechT5: {e}")
            return None

    def generate_image(self, prompt, negative_prompt=None, output_path=None, width=512, height=512):
        """
        Generate an image using HuggingFace's Stable Diffusion models.

        Args:
            prompt: Text prompt for image generation
            negative_prompt: Negative prompt for image generation (optional)
            output_path: Path to save the image file (optional)
            width: Image width (default: 512)
            height: Image height (default: 512)

        Returns:
            str: Path to the generated image file or base64-encoded image data
        """
        # Use Stable Diffusion XL for high-quality images
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

        # Prepare payload
        payload = {
            "inputs": prompt,
            "parameters": {
                "negative_prompt": negative_prompt or "low quality, blurry, distorted",
                "width": width,
                "height": height
            }
        }

        try:
            # Make request to HuggingFace API
            response = requests.post(API_URL, headers=self.headers, json=payload)
            response.raise_for_status()

            # Get image data
            image_data = response.content

            # Save to file if output_path is provided
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(image_data)
                return output_path

            # Otherwise, return base64-encoded image data
            return base64.b64encode(image_data).decode("utf-8")

        except Exception as e:
            print(f"Error generating image: {e}")
            return None

    def generate_video(self, prompt, negative_prompt=None, output_path=None, num_frames=24, fps=8):
        """
        Generate a short video clip using HuggingFace's video generation models.

        Args:
            prompt: Text prompt for video generation
            negative_prompt: Negative prompt for video generation (optional)
            output_path: Path to save the video file (optional)
            num_frames: Number of frames to generate (default: 24)
            fps: Frames per second (default: 8)

        Returns:
            str: Path to the generated video file or URL to the video
        """
        # Use Zeroscope for video generation
        API_URL = "https://api-inference.huggingface.co/models/cerspense/zeroscope_v2_576w"

        # Prepare payload
        payload = {
            "inputs": prompt,
            "parameters": {
                "negative_prompt": negative_prompt or "low quality, blurry, distorted",
                "num_frames": num_frames,
                "fps": fps
            }
        }

        try:
            # Make request to HuggingFace API
            response = requests.post(API_URL, headers=self.headers, json=payload)
            response.raise_for_status()

            # Get video data
            video_data = response.content

            # Save to file if output_path is provided
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(video_data)
                return output_path

            # Otherwise, we need to save it temporarily and return the path
            temp_path = f"media_generation/temp/video_{uuid.uuid4()}.mp4"
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(video_data)

            return temp_path

        except Exception as e:
            print(f"Error generating video: {e}")
            return None

    def generate_trial_media(self, trial_record, output_dir="media_generation/output"):
        """
        Generate media for a trial record.

        Args:
            trial_record: Trial record data
            output_dir: Directory to save media files

        Returns:
            dict: Paths to generated media files
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Generate unique ID for this trial's media
        trial_id = trial_record.get("id", str(uuid.uuid4()))
        trial_dir = f"{output_dir}/{trial_id}"
        os.makedirs(trial_dir, exist_ok=True)

        # Media paths
        media_paths = {
            "audio": {},
            "images": {},
            "videos": {}
        }

        # Generate audio for segments
        for i, segment in enumerate(trial_record.get("segments", [])):
            speaker = segment.get("speaker", "Unknown")
            lines = segment.get("lines", [])

            if lines:
                # Join lines for audio generation
                text = " ".join(lines)

                # Determine voice based on speaker
                voice = self._get_voice_for_speaker(speaker)

                # Generate audio
                audio_path = f"{trial_dir}/audio_{i}_{speaker}.mp3"
                result = self.generate_audio(text, voice, audio_path)

                if result:
                    media_paths["audio"][f"segment_{i}"] = audio_path

        # Generate image for trial setting
        title = trial_record.get("title", "Trial")
        image_prompt = f"Courtroom scene for '{title}', dramatic lighting, official setting"
        image_path = f"{trial_dir}/trial_scene.jpg"
        result = self.generate_image(image_prompt, output_path=image_path)

        if result:
            media_paths["images"]["trial_scene"] = image_path

        # Generate images for plaintiffs and defendants
        for plaintiff in trial_record.get("plaintiffs", []):
            image_prompt = f"Portrait of {plaintiff}, serious expression, courtroom setting"
            image_path = f"{trial_dir}/{plaintiff.replace(' ', '_')}.jpg"
            result = self.generate_image(image_prompt, output_path=image_path)

            if result:
                media_paths["images"][f"plaintiff_{plaintiff}"] = image_path

        for defendant in trial_record.get("defendants", []):
            image_prompt = f"Portrait of {defendant}, defensive expression, courtroom setting"
            image_path = f"{trial_dir}/{defendant.replace(' ', '_')}.jpg"
            result = self.generate_image(image_prompt, output_path=image_path)

            if result:
                media_paths["images"][f"defendant_{defendant}"] = image_path

        # Generate video for verdict
        verdict = trial_record.get("verdict", "PENDING")
        post_credit_scene = trial_record.get("post_credit_scene", {})
        setting = post_credit_scene.get("setting", "Courtroom")

        video_prompt = f"Dramatic courtroom scene, judge announcing '{verdict}' verdict, tense atmosphere, cinematic lighting"
        video_path = f"{trial_dir}/verdict.mp4"
        result = self.generate_video(video_prompt, output_path=video_path)

        if result:
            media_paths["videos"]["verdict"] = video_path

        # Generate video for post-credit scene
        if post_credit_scene:
            quote = post_credit_scene.get("quote", "")
            present = ", ".join(post_credit_scene.get("present", []))

            video_prompt = f"Scene in {setting} with {present}, dramatic moment, character saying '{quote}', cinematic"
            video_path = f"{trial_dir}/post_credit.mp4"
            result = self.generate_video(video_prompt, output_path=video_path)

            if result:
                media_paths["videos"]["post_credit"] = video_path

        return media_paths

    def _get_voice_for_speaker(self, speaker):
        """
        Get the appropriate voice for a speaker.

        Args:
            speaker: Name of the speaker

        Returns:
            str: Voice identifier
        """
        # Map speakers to voices
        voice_map = {
            "Springer": "en_male_deep",
            "Prosecutor": "en_female_emotional",
            "Defense": "en_male_confident",
            "Judge": "en_male_authoritative"
        }

        # Default to a generic voice based on first letter
        if speaker not in voice_map:
            first_letter = speaker[0].lower() if speaker else "a"
            if first_letter in "abcdefghijklm":
                return "en_male_neutral"
            else:
                return "en_female_neutral"

        return voice_map[speaker]
