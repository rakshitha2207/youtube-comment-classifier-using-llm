# Fine-Tuned BERT Model for YouTube Comment Classification

This repository hosts a fine-tuned [BERT](https://huggingface.co/transformers/model_doc/bert.html) model for classifying YouTube comments into specific categories. The model is designed to support both fine-tuned classification and **zero-shot classification** for flexible and efficient comment analysis.

## Model Overview

### Capabilities:

1. **Fine-Tuned Classification**: Predicts predefined categories for YouTube comments:
   - **Relevant Discussion**
   - **Spam or Promotional Content**
   - **Appreciation or Praise**
   - **Complaint or Criticism**
   
2. **Zero-Shot Classification**: Leverages [Hugging Face zero-shot classification](https://huggingface.co/models?pipeline_tag=zero-shot-classification) to handle unseen labels or dynamic categories without requiring additional fine-tuning.

### Use Cases:
- Automated comment moderation.
- Sentiment and behavior analysis in YouTube comment sections.
- Filtering spam and promotional comments.

---

## Model Details

- **Base Model**: `bert-base-uncased`
- **Training Dataset**: Custom dataset of YouTube comments labeled for specific categories.
- **Zero-Shot Model**: [facebook/bart-large-mnli](https://huggingface.co/facebook/bart-large-mnli) integrated for zero-shot capabilities.
- **Framework**: Hugging Face Transformers.

---

## Usage

### Installation

Install the necessary libraries:

```bash
pip install transformers torch

## Fine-Tuning Details

The fine-tuned BERT model was trained on a dataset of YouTube comments labeled with categories like relevant, spam, appreciation, and grievance. The training parameters were as follows:

- **Epochs**: 3
- **Batch Size**: 16
- **Learning Rate**: 5e-5
- **Warmup Steps**: 500
- **Weight Decay**: 0.01

The **zero-shot classification** leverages the pre-trained `facebook/bart-large-mnli` model, which is fine-tuned for textual entailment and allows the model to classify comments into any set of categories without additional training.

---

## Contribution

Contributions are welcome to enhance the model's capabilities. Feel free to fork the repository and submit pull requests for improvements or new features.

---

## License

This project is licensed under the MIT License. For more information, see the `LICENSE` file.

---

## Acknowledgments

- Hugging Face for providing the BERT and BART models.
- PyTorch for enabling fast and efficient model training and evaluation.
- The developers of the YouTube API for providing an easy way to fetch and analyze YouTube comments.

---

## Push to Hugging Face Model Hub

After fine-tuning the model, you can push it to the Hugging Face Model Hub to make it publicly available. Here’s an example of how to push the model:

```python
from huggingface_hub import login

# Log in to Hugging Face Hub using your API token
login(token="YOUR_TOKEN")

# Push the fine-tuned model to the Hugging Face Model Hub
model.push_to_hub("RAKSHITHA7/bert_yc")
tokenizer.push_to_hub("RAKSHITHA7/bert_yc")

