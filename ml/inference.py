import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from peft import PeftModel

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

CATEGORY_MODEL_PATH = os.path.join(CURRENT_DIR, "ticket_lora_adapter")
URGENCY_MODEL_PATH = os.path.join(CURRENT_DIR, "urgency_lora_adapter")
BASE_MODEL = "distilbert-base-uncased"

category_list = [
    "billing", "account", "orders", "shipping",
    "refund", "technical", "product", "subscription",
]
urgency_list = ["low", "medium", "high"]

category_id2label = {i: l for i, l in enumerate(category_list)}
category_label2id = {l: i for i, l in enumerate(category_list)}
urgency_id2label = {i: l for i, l in enumerate(urgency_list)}
urgency_label2id = {l: i for i, l in enumerate(urgency_list)}

# module-level cache so models load only once per process
_category_tokenizer = None
_category_model = None
_urgency_tokenizer = None
_urgency_model = None


def _load_category_model():
    global _category_tokenizer, _category_model
    if _category_model is None:
        _category_tokenizer = AutoTokenizer.from_pretrained(CATEGORY_MODEL_PATH)
        base = AutoModelForSequenceClassification.from_pretrained(
            BASE_MODEL,
            num_labels=len(category_list),
            id2label=category_id2label,
            label2id=category_label2id,
        )
        _category_model = PeftModel.from_pretrained(base, CATEGORY_MODEL_PATH)
        _category_model.eval()
    return _category_tokenizer, _category_model


def _load_urgency_model():
    global _urgency_tokenizer, _urgency_model
    if _urgency_model is None:
        _urgency_tokenizer = AutoTokenizer.from_pretrained(URGENCY_MODEL_PATH)
        base = AutoModelForSequenceClassification.from_pretrained(
            BASE_MODEL,
            num_labels=len(urgency_list),
            id2label=urgency_id2label,
            label2id=urgency_label2id,
        )
        _urgency_model = PeftModel.from_pretrained(base, URGENCY_MODEL_PATH)
        _urgency_model.eval()
    return _urgency_tokenizer, _urgency_model


def predict(subject: str, body: str):
    """
    Returns a dict:
    {
        "category": str, "category_confidence": float,
        "urgency": str, "urgency_confidence": float,
    }
    """
    text = f"{subject} {body}"

    cat_tokenizer, cat_model = _load_category_model()
    urg_tokenizer, urg_model = _load_urgency_model()

    cat_inputs = cat_tokenizer(text, truncation=True, padding="max_length", max_length=128, return_tensors="pt")
    urg_inputs = urg_tokenizer(text, truncation=True, padding="max_length", max_length=128, return_tensors="pt")

    with torch.no_grad():
        cat_logits = cat_model(**cat_inputs).logits
        cat_probs = torch.softmax(cat_logits, dim=1)
        cat_conf, cat_id = torch.max(cat_probs, dim=1)

        urg_logits = urg_model(**urg_inputs).logits
        urg_probs = torch.softmax(urg_logits, dim=1)
        urg_conf, urg_id = torch.max(urg_probs, dim=1)

    return {
        "category": cat_model.config.id2label[cat_id.item()],
        "category_confidence": cat_conf.item(),
        "urgency": urg_model.config.id2label[urg_id.item()],
        "urgency_confidence": urg_conf.item(),
    }