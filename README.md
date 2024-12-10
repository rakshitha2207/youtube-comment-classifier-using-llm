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

To use the model, install the necessary libraries:

```bash
pip install transformers torch


