from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

checkpoint = "JohnOfGod33/distilbert-base-cased-squad-qa"
MAX_CONTEXT_TOKENS = 384
THRESHOLD = 0.05

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForQuestionAnswering.from_pretrained(checkpoint)

# DistilBERT QA does not use token_type_ids; ignore them if provided by the pipeline.
_original_forward = model.forward


def _forward_without_token_type_ids(*args, **kwargs):
    kwargs.pop("token_type_ids", None)
    return _original_forward(*args, **kwargs)


model.forward = _forward_without_token_type_ids
nlp = pipeline(
    "question-answering",
    model=model,
    tokenizer=tokenizer,
)


def truncate_context(context, max_tokens=MAX_CONTEXT_TOKENS):
    tokens = tokenizer.encode(context, add_special_tokens=False)
    if len(tokens) <= max_tokens:
        return context, False
    truncated_tokens = tokens[:max_tokens]
    return tokenizer.decode(truncated_tokens, skip_special_tokens=True), True


def predict(question, context):
    context, was_truncated = truncate_context(context)
    response = nlp(question=question, context=context)
    if response["score"] < THRESHOLD or not response["answer"].strip():
        return "No answer found", response["score"], was_truncated
    return response["answer"], response["score"], was_truncated
