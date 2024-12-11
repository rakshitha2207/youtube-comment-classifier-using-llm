from flask import Flask, request, jsonify, render_template_string
from googleapiclient.discovery import build
from transformers import pipeline
import os
import logging
from template import HTML_TEMPLATE  # We'll create this in a separate file
import torch

# Set up logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize the YouTube API client
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    logger.error("YouTube API key not found in environment variables!")
    raise ValueError("YouTube API key not found!")

youtube = build('youtube', 'v3', 
    developerKey=YOUTUBE_API_KEY,
    cache_discovery=False
)

# Initialize the classifier
try:
    classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=0 if torch.cuda.is_available() else -1
    )
    logger.info("Classifier initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize classifier: {e}")
    raise

def extract_video_id(video_url):
    """Extract video ID from various YouTube URL formats."""
    try:
        if 'v=' in video_url:
            return video_url.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in video_url:
            return video_url.split('youtu.be/')[1].split('?')[0]
        elif 'youtube.com/embed/' in video_url:
            return video_url.split('embed/')[1].split('?')[0]
        else:
            raise ValueError("Invalid YouTube URL format")
    except Exception as e:
        logger.error(f"Error extracting video ID: {e}")
        raise ValueError(f"Could not extract video ID: {str(e)}")

def get_video_comments(video_id):
    """Fetch comments from a YouTube video."""
    try:
        comments = []
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText"
        )

        while request and len(comments) < 100:
            try:
                response = request.execute()
                items = response.get('items', [])
                logger.info(f"Fetched {len(items)} comments")

                for item in items:
                    try:
                        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                        if comment.strip():
                            comments.append(comment)
                    except KeyError as e:
                        logger.error(f"Error extracting comment text: {e}")
                        continue

                request = youtube.commentThreads().list_next(request, response)

            except Exception as e:
                logger.error(f"Error executing request: {e}")
                break

        logger.info(f"Total comments collected: {len(comments)}")
        return comments

    except Exception as e:
        logger.error(f"Error in get_video_comments: {e}")
        raise

def classify_comment(comment):
    """Classify a single comment."""
    try:
        # First, check for spam characteristics
        spam_indicators = [
            comment.isupper(),  # ALL CAPS
            comment.count('#') > 3,  # Too many hashtags
            len(comment.split()) < 3,  # Too short
            'http' in comment.lower() or 'www.' in comment.lower(),  # Contains links
            comment.count('@') > 2,  # Too many mentions
            any(phrase in comment.lower() for phrase in [
                'subscribe', 'check out my', 'visit my', 'follow me',
                'check my channel', 'sub4sub', 'subscribe to my'
            ])
        ]

        if sum(spam_indicators) >= 2:
            return "spam"

        results = classifier(
            sequences=comment,
            candidate_labels=[
                "relevant discussion",
                "promotional or spam",
                "appreciation or praise",
                "complaint or criticism"
            ],
            multi_label=False
        )

        label_mapping = {
            "relevant discussion": "relevant",
            "promotional or spam": "spam",
            "appreciation or praise": "appreciation",
            "complaint or criticism": "grievance"
        }

        return label_mapping[results['labels'][0]]

    except Exception as e:
        logger.error(f"Error classifying comment: {e}")
        raise

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze_video_comments():
    try:
        data = request.get_json()
        video_url = data.get('video_url')

        if not video_url:
            logger.error("No video URL provided")
            return jsonify({'error': 'No video URL provided'}), 400

        # Extract video ID
        try:
            video_id = extract_video_id(video_url)
            logger.info(f"Processing video ID: {video_id}")
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        # Get comments
        try:
            comments = get_video_comments(video_id)
            if not comments:
                return jsonify({'error': 'No comments found or unable to fetch comments'}), 400
        except Exception as e:
            logger.error(f"Error fetching comments: {e}")
            return jsonify({'error': f'Failed to fetch comments: {str(e)}'}), 400

        # Classify comments
        classified_comments = {
            'relevant': [],
            'spam': [],
            'appreciation': [],
            'grievance': []
        }

        for i, comment in enumerate(comments):
            try:
                classification = classify_comment(comment)
                classified_comments[classification].append(comment)
                if i % 10 == 0:
                    logger.info(f"Processed {i+1}/{len(comments)} comments")
            except Exception as e:
                logger.error(f"Error classifying comment: {e}")
                continue

        # Log results
        for category, comments_list in classified_comments.items():
            logger.info(f"{category}: {len(comments_list)} comments")

        return jsonify(classified_comments)

    except Exception as e:
        logger.error(f"Unexpected error in analyze_video_comments: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    logger.info("Starting YouTube Comment Classifier application...")
    app.run(debug=True)
