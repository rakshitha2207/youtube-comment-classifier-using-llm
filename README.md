# Fine-Tuned BERT Model for YouTube Comment Classification

This repository hosts a fine-tuned [BERT](https://huggingface.co/transformers/model_doc/bert.html) model for classifying YouTube comments into specific categories. The model is designed to support both fine-tuned classification and **zero-shot classification** for flexible and efficient comment analysis.

## Model Overview

### Capabilities:

1. **Fine-Tuned Classification**: Predicts predefined categories for YouTube comments

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

### Fine-Tuning Details
The training parameters were as follows:

- **Epochs**: 3
- **Batch Size**: 16
- **Learning Rate**: 5e-5
- **Warmup Steps**: 500
- **Weight Decay**: 0.01

The **zero-shot classification** leverages the pre-trained `facebook/bart-large-mnli` model, which is fine-tuned for textual entailment and allows the model to classify comments into any set of categories without additional training.

---

## Hugging Face Model Hub

The fine-tuned model is available on the Hugging Face Model Hub. You can access the model and its tokenizer using the following:

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Load the fine-tuned BERT model and tokenizer from Hugging Face Model Hub
model = AutoModelForSequenceClassification.from_pretrained("RAKSHITHA7/bert_yc")
tokenizer = AutoTokenizer.from_pretrained("RAKSHITHA7/bert_yc")
```
---

## Contribution

Contributions are welcome to enhance the model's capabilities. Feel free to fork the repository and submit pull requests for improvements or new features.

---

## Acknowledgments

- Hugging Face for providing the BERT and BART models.
- PyTorch for enabling fast and efficient model training and evaluation.
- The developers of the YouTube API for providing an easy way to fetch and analyze YouTube comments.

---




