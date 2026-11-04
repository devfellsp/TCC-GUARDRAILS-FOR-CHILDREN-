import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import guardkids as g
import pytest


def test_help_flag_cannot_be_silently_omitted():
    with pytest.raises(ValueError):
        g.Classification(category="hate", needs_protection=True, educational_predation=False, reason="ajuda")


@pytest.mark.parametrize("category", ["danger", "sexual", "hate", "substance"])
def test_help_has_fixed_guidance_but_harm_is_blocked(category):
    for policy in g.config()["policies"].values():
        request = g.Classification(category=category, needs_protection=True, educational_predation=False,
                                   help_seeking=True, reason="Relato ficticio")
        assert g.decision(request, policy) == "safe_guidance"
        assert g.protected_message("safe_guidance", request) == g.MESSAGES[category]
        harmful = request.model_copy(update={"help_seeking": False})
        assert g.decision(harmful, policy) == "block"


def test_attempt_to_override_rules_does_not_become_guidance():
    request = g.Classification(category="prompt_injection", needs_protection=True,
                               educational_predation=True, help_seeking=True, reason="Teste adversarial")
    assert g.decision(request, {"allow_educational_predation": True}) == "block"
