"""Unit tests for AI engine."""

from scanlytic.ai.engine import AIEngine


def test_ai_engine_disabled():
    """AI engine returns disabled status when not enabled."""
    engine = AIEngine(enabled=False)
    result = engine.score({}, {})

    assert result['status'] == 'disabled'
    assert result['score'] is None


def test_ai_engine_missing_model():
    """AI engine reports unavailable model when enabled without assets."""
    engine = AIEngine(enabled=True, model_path='/tmp/missing_model.joblib')
    result = engine.score({}, {})

    assert result['status'] == 'model_unavailable'
    assert result['score'] is None
