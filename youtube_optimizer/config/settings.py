"""Configuration settings for YouTube Semantic Optimizer."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = DATA_DIR / "exports"
DB_PATH = DATA_DIR / "youtube_optimizer.db"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

# Default Gemini model
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"

# Claude model for script writing
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# Step definitions
STEPS = {
    1: "Topic Research & Differentiation Analysis",
    2: "Semantic Entity Extraction",
    3: "Competitive Analysis",
    4: "Title Optimization",
    5: "Script Outline",
    6: "Semantic Density Pre-Check",
    7: "GARM Brand Safety Review",
    8: "Script Writing",
    9: "Script Validation",
    10: "Metadata Package",
}

# Step API mapping
STEP_API = {
    1: "gemini",
    2: "gemini",
    3: "gemini",
    4: "gemini",
    5: "gemini",
    6: "gemini",
    7: "gemini",
    8: "claude",
    9: "gemini",
    10: "gemini",
}

# Script length options (word counts)
SCRIPT_LENGTHS = {
    "Short (800-1,200 words)": (800, 1200),
    "Medium (1,500-2,000 words)": (1500, 2000),
    "Long (2,500-3,500 words)": (2500, 3500),
    "Custom": None,
}

# Script style options
SCRIPT_STYLES = [
    "Educational Authoritative",
    "Storytelling Narrative",
    "Investigative Journalistic",
    "Conversational Friend",
    "Analytical Deep Dive",
    "Provocative Challenger",
    "Documentary Observational",
    "Tutorial Practical",
]

# Video length targets (minutes)
VIDEO_LENGTHS = {
    "Short (5-8 min)": (5, 8),
    "Medium (10-15 min)": (10, 15),
    "Long (20-30 min)": (20, 30),
    "Custom": None,
}

# YouTube API settings
YOUTUBE_MAX_RESULTS = 20
YOUTUBE_SEARCH_ORDER = "relevance"

# GARM Categories
GARM_CATEGORIES = [
    "Adult & Explicit Sexual Content",
    "Arms & Ammunition",
    "Crime & Harmful Acts to Individuals and Society & Human Right Violations",
    "Death, Injury, or Military Conflict",
    "Online Piracy",
    "Hate Speech & Acts of Aggression",
    "Obscenity and Profanity",
    "Illegal Drugs, Tobacco, E-cigarettes, Vaping & Alcohol",
    "Spam or Harmful Content",
    "Terrorism",
    "Debated Sensitive Social Issue",
]
