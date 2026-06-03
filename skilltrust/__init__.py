"""SkillTrust: intent-bound permission governance for AI Skills."""

from .analyzer import SkillTrustAnalyzer
from .models import AnalysisResult, Finding

__all__ = ["SkillTrustAnalyzer", "AnalysisResult", "Finding"]

__version__ = "0.1.0"
