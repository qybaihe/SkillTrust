"""SkillTrust: intent-bound permission governance for AI Skills."""

from .analyzer import SkillTrustAnalyzer
from .models import AnalysisResult, Finding
from .skill_optimizer import analyze_skill_optimization

__all__ = ["SkillTrustAnalyzer", "AnalysisResult", "Finding", "analyze_skill_optimization"]

__version__ = "0.1.0"
