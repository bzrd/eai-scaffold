"""Unit-Tests für convert.py – PlanPro XML → plain-dict JSON."""
import pytest

# from planpro_ingest.convert import convert  # uncomment when implemented


@pytest.mark.unit
def test_valid_planpro_1_9_returns_objects() -> None:
    """Gültige PlanPro 1.9 → korrekte JSON-Objekte mit erwarteten Keys."""
    pass  # TODO: implement with fixture


@pytest.mark.unit
def test_valid_planpro_1_10_returns_objects() -> None:
    """Gültige PlanPro 1.10 → korrekte JSON-Objekte."""
    pass  # TODO: implement with fixture


@pytest.mark.unit
def test_invalid_guid_is_rejected_rest_processed() -> None:
    """Objekt mit ungültiger GUID wird abgewiesen, Rest wird verarbeitet."""
    pass  # TODO: implement


@pytest.mark.unit
def test_unknown_object_type_is_rejected() -> None:
    """Objekt mit unbekanntem Objekttyp wird abgewiesen."""
    pass  # TODO: implement


@pytest.mark.unit
def test_minimal_file_extracts_one_object() -> None:
    """Minimale PlanPro-Datei → 1 Objekt extrahiert."""
    pass  # TODO: implement


@pytest.mark.unit
def test_planpro_version_correctly_extracted() -> None:
    """PlanPro-Version korrekt aus XML ermittelt."""
    pass  # TODO: implement
