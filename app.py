import math
import os
import re
import time
from collections import Counter
from typing import Any, Optional

from flask import Flask, jsonify, render_template, request


EXAMPLES = [
    "The new onboarding flow is clean, fast, and surprisingly easy to use.",
    "I waited three hours for support and still did not get a helpful answer.",
    "The product works, but the pricing feels a little confusing for new users.",
    "Absolutely love the design, speed, and overall polish of this release!",
]

POSITIVE_WORDS = {
    "amazing": 2.3,
    "awesome": 2.2,
    "brilliant": 2.0,
    "calm": 1.0,
    "clean": 1.2,
    "confident": 1.4,
    "delightful": 2.2,
    "easy": 1.4,
    "efficient": 1.7,
    "enjoyed": 1.9,
    "excellent": 2.6,
    "fantastic": 2.5,
    "fast": 1.4,
    "flexible": 1.2,
    "good": 1.3,
    "great": 1.9,
    "happy": 1.8,
    "helpful": 1.8,
    "impressive": 1.9,
    "improved": 1.5,
    "incredible": 2.4,
    "intuitive": 1.7,
    "love": 2.5,
    "loved": 2.5,
    "nice": 1.2,
    "optimistic": 1.5,
    "outstanding": 2.6,
    "perfect": 2.5,
    "polished": 1.7,
    "powerful": 1.6,
    "quick": 1.2,
    "reliable": 1.7,
    "relaxed": 1.1,
    "responsive": 1.5,
    "safe": 1.2,
    "satisfied": 1.7,
    "smooth": 1.4,
    "solid": 1.2,
    "stable": 1.3,
    "strong": 1.3,
    "success": 1.8,
    "superb": 2.5,
    "supportive": 1.7,
    "useful": 1.5,
    "valuable": 1.6,
    "wins": 1.4,
    "wonderful": 2.4,
}

NEGATIVE_WORDS = {
    "angry": 2.1,
    "annoying": 1.9,
    "awful": 2.5,
    "bad": 1.7,
    "blocked": 1.6,
    "broken": 2.0,
    "buggy": 1.8,
    "clunky": 1.6,
    "confusing": 1.8,
    "crash": 2.1,
    "crashes": 2.1,
    "delay": 1.4,
    "disappointed": 2.0,
    "disappointing": 2.0,
    "expensive": 1.5,
    "failure": 2.2,
    "frustrated": 2.1,
    "frustrating": 2.1,
    "hard": 1.1,
    "hate": 2.5,
    "horrible": 2.5,
    "issue": 1.2,
    "laggy": 1.8,
    "messy": 1.5,
    "negative": 1.3,
    "painful": 1.9,
    "poor": 1.8,
    "regression": 1.8,
    "risky": 1.4,
    "slow": 1.5,
    "stuck": 1.6,
    "terrible": 2.7,
    "tired": 1.3,
    "unclear": 1.3,
    "unhappy": 2.0,
    "unreliable": 1.9,
    "upset": 1.7,
    "worried": 1.5,
    "worse": 1.8,
    "worst": 2.6,
}

NEGATIONS = {
    "barely",
    "cannot",
    "cant",
    "didnt",
    "doesnt",
    "dont",
    "hardly",
    "isnt",
    "never",
    "no",
    "none",
    "not",
    "nothing",
    "wasnt",
    "without",
    "wont",
}

INTENSIFIERS = {
    "absolutely": 1.45,
    "deeply": 1.25,
    "extremely": 1.4,
    "highly": 1.25,
    "incredibly": 1.35,
    "really": 1.2,
    "remarkably": 1.25,
    "so": 1.15,
    "super": 1.25,
    "too": 1.15,
    "totally": 1.35,
    "very": 1.2,
}

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "had",
    "has",
    "have",
    "i",
    "if",
    "in",
    "is",
    "it",
    "its",
    "my",
    "of",
    "on",
    "or",
    "our",
    "so",
    "that",
    "the",
    "their",
    "this",
    "to",
    "too",
    "was",
    "we",
    "were",
    "with",
    "you",
    "your",
}

TONE_MAP = {
    "optimistic": {"great", "love", "amazing", "excellent", "success", "confident", "wins"},
    "frustrated": {"bad", "broken", "frustrating", "angry", "awful", "slow", "stuck"},
    "trusting": {"reliable", "safe", "stable", "helpful", "supportive", "responsive"},
    "uncertain": {"maybe", "perhaps", "confusing", "unclear", "worried", "issue"},
}

LOCAL_PIPELINE = None
LOCAL_PIPELINE_ATTEMPTED = False
LOCAL_PIPELINE_ERROR = None


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def home() -> str:
        return render_template("index.html", examples=EXAMPLES)

    @app.get("/api/health")
    def health() -> Any:
        engine = get_engine_details()
        return jsonify(
            {
                "ok": True,
                "app": "Sentiment Studio",
                "engine": engine,
                "timestamp": int(time.time()),
            }
        )

    @app.post("/api/analyze")
    @app.post("/analyze")
    def analyze() -> Any:
        payload = request.get_json(silent=True) or request.form.to_dict(flat=True)
        text = str(payload.get("text", "")).strip()
        batch_mode = str(payload.get("mode", "single")).lower() == "batch"

        if not text:
            return jsonify({"ok": False, "error": "Please enter some text to analyze."}), 400

        if batch_mode:
            entries = [line.strip() for line in text.splitlines() if line.strip()]
            if len(entries) < 2:
                return jsonify(
                    {
                        "ok": False,
                        "error": "Batch mode needs at least two non-empty lines.",
                    }
                ), 400
            analyses = [build_analysis(item, include_sentences=False) for item in entries]
            aggregate_source = " ".join(entries)
            aggregate = build_analysis(aggregate_source, include_sentences=True)
            return jsonify(
                {
                    "ok": True,
                    "mode": "batch",
                    "engine": get_engine_details(),
                    "analysis": aggregate,
                    "entries": analyses,
                    "count": len(entries),
                }
            )

        return jsonify(
            {
                "ok": True,
                "mode": "single",
                "engine": get_engine_details(),
                "analysis": build_analysis(text, include_sentences=True),
            }
        )

    return app


def get_engine_details() -> dict[str, Any]:
    pipeline = get_local_pipeline()
    if pipeline is not None:
        return {
            "name": "huggingface-local",
            "label": "Local Hugging Face model",
            "deploy_ready": False,
            "notes": "Enabled with ENABLE_LOCAL_TRANSFORMERS=1. Great locally, but not ideal for Vercel bundles.",
        }
    if LOCAL_PIPELINE_ERROR:
        return {
            "name": "rule-based",
            "label": "Advanced rule-based engine",
            "deploy_ready": True,
            "notes": f"Falling back because local transformer setup failed: {LOCAL_PIPELINE_ERROR}",
        }
    return {
        "name": "rule-based",
        "label": "Advanced rule-based engine",
        "deploy_ready": True,
        "notes": "Default engine chosen for fast cold starts and easy Vercel deployment.",
    }


def get_local_pipeline() -> Any:
    global LOCAL_PIPELINE, LOCAL_PIPELINE_ATTEMPTED, LOCAL_PIPELINE_ERROR

    if os.getenv("ENABLE_LOCAL_TRANSFORMERS", "0") != "1":
        return None

    if LOCAL_PIPELINE_ATTEMPTED:
        return LOCAL_PIPELINE

    LOCAL_PIPELINE_ATTEMPTED = True
    try:
        from transformers import pipeline  # type: ignore

        model_name = os.getenv(
            "LOCAL_SENTIMENT_MODEL",
            "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
        )
        LOCAL_PIPELINE = pipeline("sentiment-analysis", model=model_name)
    except Exception as exc:  # pragma: no cover - best effort optional path
        LOCAL_PIPELINE_ERROR = str(exc)
        LOCAL_PIPELINE = None
    return LOCAL_PIPELINE


def build_analysis(text: str, include_sentences: bool) -> dict[str, Any]:
    text = normalize_text(text)
    transformer_result = analyze_with_local_transformer(text)
    lexical_result = analyze_rule_based(text)
    result = transformer_result or lexical_result
    result["source_text"] = text

    if include_sentences:
        sentences = split_sentences(text)
        result["sentence_breakdown"] = [
            compress_sentence_analysis(sentence, analyze_rule_based(sentence))
            for sentence in sentences
        ]
    else:
        result["sentence_breakdown"] = []

    return result


def analyze_with_local_transformer(text: str) -> Optional[dict[str, Any]]:
    pipeline = get_local_pipeline()
    if pipeline is None:
        return None

    prediction = pipeline(text[:512])[0]
    raw_label = str(prediction.get("label", "NEUTRAL")).upper()
    raw_score = float(prediction.get("score", 0.5))

    if raw_label == "POSITIVE":
        score = raw_score
    elif raw_label == "NEGATIVE":
        score = -raw_score
    else:
        score = 0.0

    label = classify_score(score)
    metrics = build_metrics(text)
    keywords = build_keyword_summary(tokenize(text))
    tones = detect_tones(tokenize(text), score)

    return {
        "label": label,
        "score": round(score, 4),
        "confidence": round(min(0.99, max(raw_score, 0.55)), 4),
        "magnitude": round(min(1.0, abs(score)), 4),
        "emoji": emoji_for_label(label),
        "summary": summary_for_label(label, score, raw_score),
        "engine": "huggingface-local",
        "metrics": metrics,
        "keywords": keywords,
        "tones": tones,
        "suggestions": build_suggestions(label, metrics, tones),
        "sentence_breakdown": [],
    }


def analyze_rule_based(text: str) -> dict[str, Any]:
    tokens = tokenize(text)
    original_tokens = tokenize(text, preserve_case=True)
    score = 0.0
    positive_hits: list[str] = []
    negative_hits: list[str] = []
    negation_hits: list[str] = []
    intensifier_hits: list[str] = []

    for index, token in enumerate(tokens):
        previous_tokens = tokens[max(0, index - 2) : index]
        modifier = 1.0

        if any(word in NEGATIONS for word in previous_tokens):
            modifier *= -1.0
            negation_hits.extend([word for word in previous_tokens if word in NEGATIONS])

        for word in previous_tokens:
            modifier *= INTENSIFIERS.get(word, 1.0)
            if word in INTENSIFIERS:
                intensifier_hits.append(word)

        token_score = 0.0
        if token in POSITIVE_WORDS:
            token_score = POSITIVE_WORDS[token] * modifier
        elif token in NEGATIVE_WORDS:
            token_score = -NEGATIVE_WORDS[token] * modifier

        if token_score:
            if original_tokens[index].isupper() and len(original_tokens[index]) > 2:
                token_score *= 1.12
            score += token_score
            if token_score >= 0:
                positive_hits.append(token)
            else:
                negative_hits.append(token)

    emphasis = min(text.count("!"), 4) * 0.12
    if score > 0:
        score += emphasis
    elif score < 0:
        score -= emphasis

    normalized_score = normalize_score(score, len(tokens))
    label = classify_score(normalized_score)
    metrics = build_metrics(text)
    keywords = build_keyword_summary(tokens)
    keywords["positive"] = unique_preserve_order(positive_hits)[:6]
    keywords["negative"] = unique_preserve_order(negative_hits)[:6]
    keywords["negations"] = unique_preserve_order(negation_hits)[:4]
    keywords["intensifiers"] = unique_preserve_order(intensifier_hits)[:4]
    tones = detect_tones(tokens, normalized_score)
    confidence = estimate_confidence(normalized_score, positive_hits, negative_hits, metrics)

    return {
        "label": label,
        "score": round(normalized_score, 4),
        "confidence": round(confidence, 4),
        "magnitude": round(min(1.0, abs(normalized_score)), 4),
        "emoji": emoji_for_label(label),
        "summary": summary_for_label(label, normalized_score, confidence),
        "engine": "rule-based",
        "metrics": metrics,
        "keywords": keywords,
        "tones": tones,
        "suggestions": build_suggestions(label, metrics, tones),
        "sentence_breakdown": [],
    }


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [part.strip() for part in parts if part.strip()]


def tokenize(text: str, preserve_case: bool = False) -> list[str]:
    matches = re.findall(r"[A-Za-z']+", text)
    if preserve_case:
        return matches
    return [match.lower() for match in matches]


def normalize_score(score: float, token_count: int) -> float:
    scale = max(1.0, token_count * 0.8)
    return math.tanh(score / scale)


def classify_score(score: float) -> str:
    if score >= 0.25:
        return "Positive"
    if score <= -0.25:
        return "Negative"
    return "Neutral"


def estimate_confidence(
    score: float,
    positive_hits: list[str],
    negative_hits: list[str],
    metrics: dict[str, Any],
) -> float:
    weighted_hits = len(positive_hits) + len(negative_hits)
    punctuation_bonus = min(metrics["exclamation_marks"], 3) * 0.02
    base = 0.55 + min(abs(score), 0.35) + min(weighted_hits * 0.03, 0.12) + punctuation_bonus
    return min(0.98, max(0.51, base))


def build_metrics(text: str) -> dict[str, Any]:
    tokens = tokenize(text)
    characters = len(text)
    words = len(tokens)
    sentence_count = max(1, len(split_sentences(text)))
    uppercase_letters = sum(1 for char in text if char.isupper())
    alpha_letters = sum(1 for char in text if char.isalpha())
    uppercase_ratio = round((uppercase_letters / alpha_letters), 3) if alpha_letters else 0.0

    return {
        "characters": characters,
        "words": words,
        "sentences": sentence_count,
        "reading_time_seconds": max(1, math.ceil(words / 3.2)),
        "exclamation_marks": text.count("!"),
        "question_marks": text.count("?"),
        "uppercase_ratio": uppercase_ratio,
    }


def build_keyword_summary(tokens: list[str]) -> dict[str, Any]:
    filtered = [token for token in tokens if token not in STOPWORDS and len(token) > 2]
    common = [word for word, _ in Counter(filtered).most_common(5)]
    return {
        "top_terms": common,
        "positive": [],
        "negative": [],
        "negations": [],
        "intensifiers": [],
    }


def detect_tones(tokens: list[str], score: float) -> list[str]:
    found = []
    token_set = set(tokens)
    for tone, words in TONE_MAP.items():
        if token_set.intersection(words):
            found.append(tone)

    if not found:
        if score >= 0.25:
            found.append("encouraging")
        elif score <= -0.25:
            found.append("critical")
        else:
            found.append("measured")
    return found[:4]


def build_suggestions(label: str, metrics: dict[str, Any], tones: list[str]) -> list[str]:
    suggestions = []
    if label == "Positive":
        suggestions.append("This reads well for testimonials, product wins, or launch updates.")
    if label == "Negative":
        suggestions.append("Consider softer phrasing if this message is meant for customers or teammates.")
    if label == "Neutral":
        suggestions.append("Add more detail or emotional context if you want a stronger tone signal.")
    if metrics["question_marks"] > 1:
        suggestions.append("Multiple questions can make the tone feel uncertain or exploratory.")
    if metrics["uppercase_ratio"] > 0.18:
        suggestions.append("High uppercase usage adds intensity and can make the message feel urgent.")
    if "uncertain" in tones:
        suggestions.append("Clarifying the main point could make the wording sound more confident.")
    return suggestions[:4]


def summary_for_label(label: str, score: float, confidence: float) -> str:
    intensity = "strong" if abs(score) >= 0.55 else "moderate" if abs(score) >= 0.25 else "light"
    return f"{intensity.title()} {label.lower()} sentiment with {confidence:.0%} confidence."


def emoji_for_label(label: str) -> str:
    if label == "Positive":
        return "Upbeat"
    if label == "Negative":
        return "Concerned"
    return "Balanced"


def compress_sentence_analysis(sentence: str, analysis: dict[str, Any]) -> dict[str, Any]:
    return {
        "sentence": sentence,
        "label": analysis["label"],
        "score": analysis["score"],
        "confidence": analysis["confidence"],
    }


def unique_preserve_order(items: list[str]) -> list[str]:
    seen = set()
    unique_items = []
    for item in items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)
    return unique_items


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
