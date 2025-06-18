import pytest
from utils.template_loader import render

def test_template_rendering():
    """Ensure template renders with given parameters."""
    result = render("cvb_summary", content="Trial with 30 calves showed...", compliance_note="Ensure all CFR regulations are met.")
    
    assert "Trial with 30 calves showed..." in result
    assert "Ensure all CFR regulations are met." in result
    assert "USDA-CVB product license application" in result  # Check template context
