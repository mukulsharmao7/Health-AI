from backend.services.rag_service import answer_question, retrieve_evidence


def test_activity_question_retrieves_cited_cdc_source():
    evidence = retrieve_evidence("How much physical activity do adults need?")
    assert evidence
    assert "cdc.gov" in evidence[0]["url"]
    assert "150 minutes" in evidence[0]["text"]


def test_rag_falls_back_to_extracts_without_local_model(monkeypatch):
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    result = answer_question("How many hours of sleep do adults need?")
    assert result["generated_by"] == "extractive"
    assert result["sources"]
    assert "not a diagnosis" in result["answer"]


def test_unrelated_question_does_not_invent_an_answer():
    result = answer_question("What is the capital of France?")
    assert result["sources"] == []
    assert "could not find relevant information" in result["answer"]
