"""OutputExtractor and StepValidator classes for quality validation."""

import re
from typing import Optional, List, Dict, Any


class OutputExtractor:
    """Extracts structured data from step outputs with multiple fallback strategies."""

    @staticmethod
    def extract_recommended_title(step4_output: str) -> str:
        """Extract the recommended title from Step 4 output."""
        if not step4_output:
            return ""

        # Strategy 1: Look for explicit "Best Title:" or "RECOMMENDED TITLE:"
        patterns = [
            r"(?:Best Title|BEST TITLE|Recommended Title|RECOMMENDED TITLE)[:\s]*[\"']?(.+?)[\"']?\s*$",
            r"(?:THE BEST TITLE|Winner|Final Recommendation)[:\s]*[\"']?(.+?)[\"']?\s*$",
            r"(?:I recommend|My recommendation)[:\s]*[\"']?(.+?)[\"']?\s*$",
        ]
        for pattern in patterns:
            match = re.search(pattern, step4_output, re.MULTILINE | re.IGNORECASE)
            if match:
                title = match.group(1).strip().strip("\"'")
                if len(title) > 5:
                    return title

        # Strategy 2: Look for numbered titles and pick the one marked best
        title_pattern = r'(?:\d+[\.\)]\s*)[\""](.+?)[\""]'
        titles = re.findall(title_pattern, step4_output)
        if titles:
            return titles[0]

        # Strategy 3: Return first quoted string that looks like a title
        quoted = re.findall(r'[\""]([^"\"]{15,100})[\""]', step4_output)
        if quoted:
            return quoted[0]

        return ""

    @staticmethod
    def extract_recommended_angle(step1_output: str) -> str:
        """Extract the recommended angle from Step 1 output."""
        if not step1_output:
            return ""

        patterns = [
            r"(?:Best Angle|BEST ANGLE|Recommended Angle|RECOMMENDED ANGLE)[:\s]*(.+?)(?:\n|$)",
            r"(?:THE SINGLE BEST ANGLE|THE BEST ANGLE)[:\s]*(.+?)(?:\n|$)",
            r"(?:I recommend|Recommendation)[:\s]*(.+?)(?:\n|$)",
        ]
        for pattern in patterns:
            match = re.search(pattern, step1_output, re.MULTILINE | re.IGNORECASE)
            if match:
                angle = match.group(1).strip().strip("\"'-")
                if len(angle) > 5:
                    return angle

        # Fallback: Look for angle after separator
        sections = step1_output.split("=" * 10)
        for section in reversed(sections):
            if "angle" in section.lower() and "recommend" in section.lower():
                lines = [l.strip() for l in section.strip().split("\n") if l.strip() and len(l.strip()) > 10]
                if lines:
                    return lines[-1].strip("\"'-:. ")

        return ""

    @staticmethod
    def extract_entities(step2_output: str) -> Dict[str, List[str]]:
        """Extract semantic entities from Step 2 output."""
        if not step2_output:
            return {"high": [], "medium": []}

        high_entities = []
        medium_entities = []

        # Look for high-priority section
        high_match = re.search(
            r"(?:HIGH[- ]PRIORITY|High Priority)[^\n]*\n([\s\S]*?)(?:MEDIUM|Medium|$)",
            step2_output, re.IGNORECASE
        )
        if high_match:
            lines = high_match.group(1).strip().split("\n")
            for line in lines:
                clean = re.sub(r'^[\s\-\d\.\)]+', '', line).strip()
                if clean and len(clean) > 2:
                    # Extract just the entity name (before any parenthetical)
                    entity = re.split(r'\s*[\(\[\-:]', clean)[0].strip()
                    if entity:
                        high_entities.append(entity)

        # Look for medium-priority section
        medium_match = re.search(
            r"(?:MEDIUM[- ]PRIORITY|Medium Priority)[^\n]*\n([\s\S]*?)(?:VAGUE|Vague|LOW|Low|$)",
            step2_output, re.IGNORECASE
        )
        if medium_match:
            lines = medium_match.group(1).strip().split("\n")
            for line in lines:
                clean = re.sub(r'^[\s\-\d\.\)]+', '', line).strip()
                if clean and len(clean) > 2:
                    entity = re.split(r'\s*[\(\[\-:]', clean)[0].strip()
                    if entity:
                        medium_entities.append(entity)

        return {"high": high_entities[:12], "medium": medium_entities[:15]}

    @staticmethod
    def extract_outline(step5_output: str) -> str:
        """Extract the script outline from Step 5 output."""
        if not step5_output:
            return ""
        return step5_output

    @staticmethod
    def extract_safety_concerns(step7_output: str) -> Dict[str, Any]:
        """Extract GARM safety review results from Step 7."""
        if not step7_output:
            return {"risk_level": "Unknown", "concerns": [], "monetization": "Unknown"}

        risk_match = re.search(
            r"(?:Overall Risk|Risk Level|RISK LEVEL)[:\s]*(Low|Medium|High)",
            step7_output, re.IGNORECASE
        )
        risk_level = risk_match.group(1).title() if risk_match else "Unknown"

        monetization_match = re.search(
            r"(?:Monetization|MONETIZATION)[:\s]*(Full Ads|Limited|None|Full)",
            step7_output, re.IGNORECASE
        )
        monetization = monetization_match.group(1) if monetization_match else "Unknown"

        concerns = []
        concern_patterns = re.findall(
            r"(?:High Severity|CONCERN|Warning|Flag)[:\s]*(.+?)(?:\n|$)",
            step7_output, re.IGNORECASE
        )
        concerns = [c.strip() for c in concern_patterns if c.strip()]

        return {
            "risk_level": risk_level,
            "concerns": concerns,
            "monetization": monetization,
        }

    @staticmethod
    def extract_density_fixes(step6_output: str) -> List[str]:
        """Extract critical fixes from Step 6 output."""
        if not step6_output:
            return []

        fixes = []
        fix_section = re.search(
            r"(?:CRITICAL FIXES|Critical Fixes|FIXES NEEDED|Fixes)[^\n]*\n([\s\S]*?)(?:={5,}|$)",
            step6_output, re.IGNORECASE
        )
        if fix_section:
            lines = fix_section.group(1).strip().split("\n")
            for line in lines:
                clean = re.sub(r'^[\s\-\d\.\)]+', '', line).strip()
                if clean and len(clean) > 5:
                    fixes.append(clean)

        return fixes

    @staticmethod
    def extract_validation_score(step9_output: str) -> Dict[str, Any]:
        """Extract validation scores from Step 9 output."""
        if not step9_output:
            return {"overall": 0, "approval": "Unknown", "scores": {}}

        scores = {}
        score_patterns = [
            (r"Entity Optimization[:\s]*(\d+)", "entity_optimization"),
            (r"Net Information Gain[:\s]*(\d+)", "information_gain"),
            (r"Semantic ID[:\s]*(\d+)", "semantic_id"),
            (r"GARM Safety[:\s]*(\d+)", "garm_safety"),
            (r"Quality[:\s]*(\d+)", "quality"),
        ]
        for pattern, key in score_patterns:
            match = re.search(pattern, step9_output, re.IGNORECASE)
            if match:
                scores[key] = int(match.group(1))

        overall_match = re.search(r"(?:Overall|OVERALL|Total)[:\s]*(\d+)", step9_output, re.IGNORECASE)
        overall = int(overall_match.group(1)) if overall_match else sum(scores.values())

        approval_match = re.search(
            r"(?:Approval|APPROVAL|Verdict)[:\s]*(YES|YES WITH EDITS|NEEDS REVISION)",
            step9_output, re.IGNORECASE
        )
        approval = approval_match.group(1).upper() if approval_match else "Unknown"

        return {"overall": overall, "approval": approval, "scores": scores}


class StepValidator:
    """Validates step output quality."""

    @staticmethod
    def validate_step_output(step_number: int, output: str) -> Dict[str, Any]:
        """Validate output quality for a given step. Returns validation result."""
        if not output or len(output.strip()) < 50:
            return {
                "valid": False,
                "score": 0,
                "message": "Output too short or empty.",
            }

        validators = {
            1: StepValidator._validate_step1,
            2: StepValidator._validate_step2,
            3: StepValidator._validate_step3,
            4: StepValidator._validate_step4,
            5: StepValidator._validate_step5,
            6: StepValidator._validate_step6,
            7: StepValidator._validate_step7,
            8: StepValidator._validate_step8,
            9: StepValidator._validate_step9,
            10: StepValidator._validate_step10,
        }

        validator = validators.get(step_number)
        if validator:
            return validator(output)

        return {"valid": True, "score": 5, "message": "No validator for this step."}

    @staticmethod
    def _validate_step1(output: str) -> Dict[str, Any]:
        checks = {
            "has_angles": bool(re.search(r"(?:angle|unique|differentiat)", output, re.IGNORECASE)),
            "has_entities": bool(re.search(r"(?:entit|semantic)", output, re.IGNORECASE)),
            "has_recommendation": bool(re.search(r"(?:best|recommend)", output, re.IGNORECASE)),
            "sufficient_length": len(output) > 500,
        }
        score = sum(checks.values()) * 2.5
        return {
            "valid": score >= 5,
            "score": score,
            "message": f"Step 1 validation: {sum(checks.values())}/4 checks passed.",
            "checks": checks,
        }

    @staticmethod
    def _validate_step2(output: str) -> Dict[str, Any]:
        entities = OutputExtractor.extract_entities(output)
        has_high = len(entities["high"]) >= 3
        has_medium = len(entities["medium"]) >= 3
        score = (5 if has_high else 2) + (5 if has_medium else 2)
        return {
            "valid": has_high and has_medium,
            "score": score,
            "message": f"Found {len(entities['high'])} high and {len(entities['medium'])} medium entities.",
        }

    @staticmethod
    def _validate_step3(output: str) -> Dict[str, Any]:
        has_analysis = len(output) > 300
        has_gaps = bool(re.search(r"(?:gap|opportunity|white space)", output, re.IGNORECASE))
        score = (5 if has_analysis else 2) + (5 if has_gaps else 2)
        return {"valid": score >= 7, "score": score, "message": f"Competitive analysis score: {score}/10"}

    @staticmethod
    def _validate_step4(output: str) -> Dict[str, Any]:
        title = OutputExtractor.extract_recommended_title(output)
        title_count = len(re.findall(r'(?:\d+[\.\)])', output))
        has_scores = bool(re.search(r"(?:score|Semantic Strength|CTR)", output, re.IGNORECASE))
        score = (3 if title else 0) + (4 if title_count >= 5 else 2) + (3 if has_scores else 0)
        return {"valid": score >= 7, "score": score, "message": f"Title optimization score: {score}/10. Best: '{title[:50]}'"}

    @staticmethod
    def _validate_step5(output: str) -> Dict[str, Any]:
        has_sections = bool(re.search(r"(?:hook|intro|main|conclusion)", output, re.IGNORECASE))
        has_timestamps = bool(re.search(r"\d+:\d+", output))
        score = (5 if has_sections else 2) + (5 if has_timestamps else 2)
        return {"valid": score >= 7, "score": score, "message": f"Outline score: {score}/10"}

    @staticmethod
    def _validate_step6(output: str) -> Dict[str, Any]:
        has_score = bool(re.search(r"(?:Semantic Strength Score|density)", output, re.IGNORECASE))
        has_fixes = bool(re.search(r"(?:fix|replace|vague)", output, re.IGNORECASE))
        score = (5 if has_score else 2) + (5 if has_fixes else 2)
        return {"valid": score >= 7, "score": score, "message": f"Density check score: {score}/10"}

    @staticmethod
    def _validate_step7(output: str) -> Dict[str, Any]:
        safety = OutputExtractor.extract_safety_concerns(output)
        has_risk = safety["risk_level"] != "Unknown"
        has_monetization = safety["monetization"] != "Unknown"
        score = (5 if has_risk else 2) + (5 if has_monetization else 2)
        return {"valid": score >= 7, "score": score, "message": f"GARM review: Risk={safety['risk_level']}, Monetization={safety['monetization']}"}

    @staticmethod
    def _validate_step8(output: str) -> Dict[str, Any]:
        word_count = len(output.split())
        has_hook = bool(re.search(r"(?:hook|HOOK|\[HOOK\])", output, re.IGNORECASE))
        sufficient = word_count >= 500
        score = (3 if has_hook else 1) + (4 if sufficient else 1) + (3 if word_count >= 800 else 1)
        return {"valid": score >= 7, "score": score, "message": f"Script: {word_count} words. Score: {score}/10"}

    @staticmethod
    def _validate_step9(output: str) -> Dict[str, Any]:
        validation = OutputExtractor.extract_validation_score(output)
        has_scores = len(validation["scores"]) >= 3
        has_approval = validation["approval"] != "Unknown"
        score = (5 if has_scores else 2) + (5 if has_approval else 2)
        return {"valid": score >= 7, "score": score, "message": f"Validation: {validation['approval']}, Overall: {validation['overall']}/50"}

    @staticmethod
    def _validate_step10(output: str) -> Dict[str, Any]:
        has_description = bool(re.search(r"(?:description|DESCRIPTION)", output, re.IGNORECASE))
        has_tags = bool(re.search(r"(?:tag|TAG)", output, re.IGNORECASE))
        has_chapters = bool(re.search(r"(?:chapter|timestamp)", output, re.IGNORECASE))
        score = (3 if has_description else 1) + (4 if has_tags else 1) + (3 if has_chapters else 1)
        return {"valid": score >= 7, "score": score, "message": f"Metadata package score: {score}/10"}
