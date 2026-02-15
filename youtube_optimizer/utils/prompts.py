"""All 10 step prompts for the YouTube Semantic Optimizer workflow."""

import re
from typing import Dict, Any, List, Optional
from utils.validators import OutputExtractor


def get_step1_prompt(topic: str, target_audience: str = "",
                     youtube_data: str = "") -> str:
    """Step 1: Topic Research & Differentiation Analysis."""
    yt_section = ""
    if youtube_data and youtube_data != "No YouTube data available.":
        yt_section = f"""
REAL YOUTUBE DATA (use this for your analysis - do NOT fabricate data):
{youtube_data}
"""
    else:
        yt_section = """
NOTE: No real YouTube data available. Base your analysis on your knowledge of the topic landscape.
Be honest about this limitation - do not fabricate view counts or specific video references.
"""

    return f"""You are a YouTube content strategist and semantic SEO expert.

TASK: Perform a comprehensive Topic Research & Differentiation Analysis for a YouTube video.

TOPIC: {topic}
TARGET AUDIENCE: {target_audience or 'General YouTube audience'}

{yt_section}

================================================================
REQUIRED OUTPUT FORMAT:
================================================================

1. CONTENT LANDSCAPE ASSESSMENT
   - Classification: [Niche / Moderate / Saturated]
   - Explain why with data points

2. SATURATED ANGLES TO AVOID (15-20)
   List angles that are overdone. Number each one.

3. UNIQUE ANGLES (7-10)
   For each angle provide:
   - Angle name
   - Originality Score (1-10)
   - Why it's different
   - Target viewer appeal

4. SEMANTIC ENTITY MAP (20-30 entities)
   Categorize as:
   - HIGH PRIORITY (must include, 5-8 mentions each)
   - MEDIUM PRIORITY (supporting, 2-4 mentions each)

5. THE SINGLE BEST ANGLE RECOMMENDATION
   Best Angle: [Your recommended angle]

   Provide detailed reasoning:
   - Why this angle wins
   - Expected differentiation impact
   - Audience appeal
   - Semantic richness potential

================================================================
"""


def get_step2_prompt(topic: str, selected_angle: str,
                     step1_output: str) -> str:
    """Step 2: Semantic Entity Extraction."""
    return f"""You are a semantic SEO specialist for YouTube content.

TOPIC: {topic}
SELECTED ANGLE: {selected_angle}

CONTEXT FROM STEP 1:
{step1_output[:3000]}

================================================================
TASK: Extract and organize all semantic entities for this video.
================================================================

REQUIRED OUTPUT:

1. HIGH-PRIORITY ENTITIES (8-12 entities)
   For each:
   - Entity name
   - Target frequency: 5-8 mentions
   - Context: Where/how to use in script
   - Related terms/synonyms

2. MEDIUM-PRIORITY ENTITIES (10-15 entities)
   For each:
   - Entity name
   - Target frequency: 2-4 mentions
   - Context: Where/how to use

3. VAGUE TERMS TO AVOID → SPECIFIC REPLACEMENTS
   Format: "Vague term" → "Specific entity replacement"
   List at least 10 replacements.

4. ENTITY DISTRIBUTION STRATEGY
   - Hook section: Which entities to front-load
   - Context/Setup: Which entities for background
   - Main Content: Primary entity density
   - Conclusion/CTA: Which entities to reinforce

5. ENTITY DENSITY TARGETS
   - Target entity density per 100 words
   - Minimum unique entities per section
   - Total entity coverage goal

================================================================
"""


def get_step3_prompt(topic: str, youtube_data: str,
                     step1_output: str) -> str:
    """Step 3: Competitive Analysis."""
    yt_section = ""
    if youtube_data and youtube_data != "No YouTube data available.":
        yt_section = f"""
REAL YOUTUBE DATA FOR ANALYSIS:
{youtube_data}
"""
    else:
        yt_section = """
NOTE: No real YouTube data available. Provide analysis based on general knowledge of the topic space.
"""

    return f"""You are a YouTube competitive analysis expert.

TOPIC: {topic}

{yt_section}

PREVIOUS RESEARCH (Step 1):
{step1_output[:2000]}

================================================================
TASK: Perform comprehensive competitive analysis.
================================================================

REQUIRED OUTPUT:

1. TOP COMPETITORS ANALYSIS
   For each of the top 10 videos analyzed:
   - Title pattern analysis
   - Performance metrics assessment
   - Content approach

2. TITLE PATTERNS
   - Most common title structures
   - Overused words/phrases
   - Underused opportunities

3. TAG ANALYSIS
   - Most common tags
   - High-value underused tags
   - Tag strategy recommendations

4. CONTENT GAPS & WHITE SPACE
   - Topics not covered well
   - Angles missing from top content
   - Audience questions unanswered

5. DIFFERENTIATION STRATEGY
   - How our approach differs from top competitors
   - Specific advantages of our angle
   - Risk assessment

6. DATA-DRIVEN RECOMMENDATIONS
   - Optimal video length based on competition
   - Best posting strategy insights
   - Thumbnail pattern analysis

================================================================
"""


def get_step4_prompt(topic: str, step1_output: str,
                     step2_output: str, step3_output: str) -> str:
    """Step 4: Title Optimization."""
    angle = OutputExtractor.extract_recommended_angle(step1_output)

    return f"""You are a YouTube title optimization expert specializing in CTR and semantic SEO.

TOPIC: {topic}
SELECTED ANGLE: {angle or 'See Step 1 recommendation below'}

CONTEXT:
- Step 1 (Research): {step1_output[:1500]}
- Step 2 (Entities): {step2_output[:1000]}
- Step 3 (Competition): {step3_output[:1000]}

================================================================
TASK: Generate 10 optimized title options.
================================================================

REQUIRED OUTPUT:

For each of the 10 titles:
1. "Title text here"
   - Semantic Strength: X/10
   - Differentiation: X/10
   - CTR Potential: X/10
   - Thumbnail Text Suggestion: [complementary text]
   - Why it works: [brief explanation]

ANALYSIS:
- Overused patterns to avoid
- Underused patterns leveraged
- Emotional trigger analysis

================================================================
THE BEST TITLE RECOMMENDATION:
Best Title: "[Your #1 pick]"

Comprehensive reasoning:
- Why this title wins across all metrics
- Expected CTR performance
- Semantic SEO advantage
- How it complements the thumbnail
================================================================
"""


def get_step5_prompt(topic: str, target_length: str,
                     step1_output: str, step2_output: str,
                     step4_output: str) -> str:
    """Step 5: Script Outline."""
    title = OutputExtractor.extract_recommended_title(step4_output)
    entities = OutputExtractor.extract_entities(step2_output)
    entity_list = ", ".join(entities.get("high", [])[:8])

    return f"""You are a YouTube script architect and content strategist.

TOPIC: {topic}
SELECTED TITLE: {title or 'See Step 4 recommendation'}
TARGET VIDEO LENGTH: {target_length}
KEY ENTITIES TO DISTRIBUTE: {entity_list}

CONTEXT:
- Step 1 (Research): {step1_output[:1000]}
- Step 2 (Entities): {step2_output[:1500]}

================================================================
TASK: Create a detailed script outline with entity distribution.
================================================================

REQUIRED OUTPUT:

SCRIPT OUTLINE:

HOOK (0:00 - 0:30)
- Opening approach
- Key entities to introduce
- Viewer retention hook
- B-roll suggestions

INTRODUCTION/CONTEXT (0:30 - 2:00)
- Context setting
- Entity placement
- Transition to main content

MAIN CONTENT SECTIONS:
For each section provide:
- Timestamp range
- Section title
- Key points (3-5 per section)
- Entities to use in this section
- B-roll / visual suggestions
- Transition to next section

CONCLUSION & CTA
- Summary approach
- Final entity reinforcement
- Call to action strategy

================================================================
ENTITY DISTRIBUTION MAP:
Show which entities appear in which sections.

Total estimated entities per section.
================================================================
"""


def get_step6_prompt(step2_output: str, step5_output: str) -> str:
    """Step 6: Semantic Density Pre-Check."""
    entities = OutputExtractor.extract_entities(step2_output)

    return f"""You are a semantic density analysis expert for YouTube content.

ENTITIES FROM STEP 2:
High Priority: {', '.join(entities.get('high', []))}
Medium Priority: {', '.join(entities.get('medium', []))}

SCRIPT OUTLINE FROM STEP 5:
{step5_output[:3000]}

================================================================
TASK: Validate entity frequency, distribution, and identify fixes.
================================================================

REQUIRED OUTPUT:

1. ENTITY FREQUENCY VALIDATION
   For each high-priority entity:
   - Current planned frequency
   - Target frequency
   - Status: OK / NEEDS MORE / REDUCE

2. ENTITY DISTRIBUTION ANALYSIS
   Section-by-section semantic node analysis:
   - Which sections are entity-rich
   - Which sections need more entities
   - Balance assessment

3. VAGUE LANGUAGE FLAGS
   Identify any vague language in the outline that should be replaced
   with specific entities. Format:
   - "Vague phrase" → "Entity replacement"

4. SEMANTIC STRENGTH SCORE: X/10
   Breakdown of scoring criteria.

5. CRITICAL FIXES NEEDED
   List specific, actionable fixes that must be applied
   before script writing begins.

================================================================
"""


def get_step7_prompt(topic: str, step1_output: str,
                     step5_output: str) -> str:
    """Step 7: GARM Brand Safety Review."""
    return f"""You are a brand safety and monetization compliance expert.

TOPIC: {topic}

CONTENT OUTLINE:
{step5_output[:3000]}

CONTENT APPROACH (from research):
{step1_output[:1000]}

================================================================
TASK: Review against all 11 GARM (Global Alliance for Responsible Media) categories.
================================================================

GARM CATEGORIES TO REVIEW:
1. Adult & Explicit Sexual Content
2. Arms & Ammunition
3. Crime & Harmful Acts to Individuals and Society & Human Rights Violations
4. Death, Injury, or Military Conflict
5. Online Piracy
6. Hate Speech & Acts of Aggression
7. Obscenity and Profanity
8. Illegal Drugs, Tobacco, E-cigarettes, Vaping & Alcohol
9. Spam or Harmful Content
10. Terrorism
11. Debated Sensitive Social Issue

REQUIRED OUTPUT:

1. CATEGORY-BY-CATEGORY REVIEW
   For each of the 11 categories:
   - Risk Level: None / Low / Medium / High
   - Specific concerns (if any)
   - Recommended modifications

2. OVERALL RISK ASSESSMENT
   Overall Risk Level: [Low/Medium/High]

3. MONETIZATION FORECAST
   Monetization: [Full Ads / Limited / None]
   Explanation of forecast.

4. HIGH SEVERITY CONCERNS (if any)
   List and explain.

5. MEDIUM SEVERITY CONCERNS (if any)
   List and explain.

6. ADVERTISER-FRIENDLY ALTERNATIVES
   For any flagged content, provide safe alternatives
   that maintain content quality.

================================================================
"""


def get_step8_prompt(user_inputs: Dict[str, Any],
                     previous_outputs: Dict[int, str]) -> str:
    """Step 8: Script Writing (Claude). Packages all context from previous steps."""

    # Extract structured data from previous outputs
    step1 = previous_outputs.get(1, "")
    step2 = previous_outputs.get(2, "")
    step4 = previous_outputs.get(4, "")
    step5 = previous_outputs.get(5, "")
    step6 = previous_outputs.get(6, "")
    step7 = previous_outputs.get(7, "")

    title = OutputExtractor.extract_recommended_title(step4)
    angle = OutputExtractor.extract_recommended_angle(step1)
    entities = OutputExtractor.extract_entities(step2)
    safety = OutputExtractor.extract_safety_concerns(step7)
    fixes = OutputExtractor.extract_density_fixes(step6)

    topic = user_inputs.get("topic", "")
    script_length = user_inputs.get("script_length", "Medium (1,500-2,000 words)")
    script_style = user_inputs.get("script_style", "Educational Authoritative")
    word_range = user_inputs.get("word_range", (1500, 2000))

    # Build style profile
    style_profiles = _get_style_profiles()
    style_profile = style_profiles.get(script_style, style_profiles["Educational Authoritative"])

    high_entities = ", ".join(entities.get("high", []))
    medium_entities = ", ".join(entities.get("medium", []))
    fixes_text = "\n".join(f"- {f}" for f in fixes) if fixes else "No critical fixes identified."
    safety_text = f"Risk: {safety['risk_level']}, Monetization: {safety['monetization']}"
    concerns = "\n".join(f"- {c}" for c in safety.get("concerns", []))

    return f"""You are an expert YouTube scriptwriter. Write a complete, production-ready script.

================================================================
STRUCTURED RESEARCH PACKAGE
================================================================

TOPIC: {topic}
TITLE: {title or 'See context below'}
ANGLE: {angle or 'See context below'}

HIGH-PRIORITY ENTITIES (use 5-8 times each): {high_entities}
MEDIUM-PRIORITY ENTITIES (use 2-4 times each): {medium_entities}

SCRIPT OUTLINE:
{step5[:2500] if step5 else 'No outline available - create your own structure.'}

CRITICAL FIXES TO APPLY:
{fixes_text}

GARM SAFETY REQUIREMENTS:
{safety_text}
{f'Concerns to avoid: {concerns}' if concerns else 'No specific concerns.'}

================================================================
SCRIPT REQUIREMENTS
================================================================

WORD COUNT: {word_range[0]}-{word_range[1]} words
THIS IS STRICTLY ENFORCED. Your script MUST be within this range.

SCRIPT STYLE: {script_style}
{style_profile}

================================================================
ANTI-TEMPLATE DETECTION INSTRUCTIONS
================================================================

Your script must NOT feel formulaic or AI-generated. Specifically:
- DO NOT use "In this video, we'll explore..."
- DO NOT use "Let's dive in" or "Without further ado"
- DO NOT use "In today's video"
- DO NOT use generic transitions like "Moving on" or "Next up"
- DO NOT start with a question followed by "Well, you're in the right place"
- VARY sentence length dramatically (5-word sentences mixed with 25-word sentences)
- Use unexpected analogies and references
- Include specific numbers, dates, names where appropriate
- Write like a human with opinions, not a neutral AI

BANNED PHRASES:
- "Let's dive in"
- "Without further ado"
- "In this video"
- "Hey guys"
- "Smash that like button" (unless ironically)
- "So basically"
- "At the end of the day"

================================================================
WRITE THE COMPLETE SCRIPT NOW
================================================================

Format with clear section markers:
[HOOK]
[INTRO]
[SECTION 1: Title]
[SECTION 2: Title]
... etc
[CONCLUSION]
[CTA]

Include:
- Speaker directions in (parentheses)
- B-roll suggestions in [brackets]
- Emphasis markers for key words in **bold**

START WRITING:
"""


def get_step8_system_prompt(script_style: str = "Educational Authoritative") -> str:
    """System prompt for Claude when writing scripts."""
    return f"""You are a world-class YouTube scriptwriter known for creating viral,
high-retention content. Your scripts are engaging, entity-rich for SEO,
and never feel formulaic or AI-generated.

Your current style assignment: {script_style}

Rules:
1. Stay within the specified word count range - this is non-negotiable
2. Integrate ALL high-priority entities naturally (5-8 mentions each)
3. Integrate medium-priority entities (2-4 mentions each)
4. Follow the GARM safety requirements
5. Apply all critical fixes from the density pre-check
6. Never use banned phrases
7. Make every sentence serve a purpose - no filler
8. Write for spoken delivery - use contractions, natural rhythm
9. Include specific data points, examples, and evidence
10. Create genuine moments of surprise, insight, or emotion"""


def get_step9_prompt(step2_output: str, step7_output: str,
                     step8_output: str) -> str:
    """Step 9: Script Validation."""
    entities = OutputExtractor.extract_entities(step2_output)

    return f"""You are a YouTube content quality assurance expert.

SCRIPT TO VALIDATE:
{step8_output[:5000]}

REQUIRED ENTITIES:
High Priority: {', '.join(entities.get('high', []))}
Medium Priority: {', '.join(entities.get('medium', []))}

GARM SAFETY REVIEW (Step 7):
{step7_output[:1500]}

================================================================
TASK: Validate the script across 5 dimensions.
================================================================

REQUIRED OUTPUT:

1. ENTITY OPTIMIZATION SCORE: X/10
   - Check each high-priority entity frequency (target: 5-8)
   - Check each medium-priority entity frequency (target: 2-4)
   - List entities below target
   - List entities above target

2. NET INFORMATION GAIN SCORE: X/10
   - Does the script provide new/unique information?
   - Are there specific data points, examples, evidence?
   - Is there filler content that should be removed?

3. SEMANTIC ID SCORE: X/10
   - Would YouTube's algorithm understand the topic?
   - Is entity density sufficient?
   - Are related terms and synonyms used effectively?

4. GARM SAFETY SCORE: X/10
   - Any brand safety violations?
   - Monetization risk assessment
   - Specific concerns

5. QUALITY SCORE: X/10
   - Engagement potential
   - Hook effectiveness
   - Pacing and flow
   - Call to action strength

================================================================
OVERALL SCORE: X/50

FINAL APPROVAL: [YES / YES WITH EDITS / NEEDS REVISION]

If YES WITH EDITS, list specific edits needed.
If NEEDS REVISION, explain what needs major changes.
================================================================
"""


def get_step10_prompt(topic: str, step4_output: str,
                      step2_output: str, step8_output: str,
                      step3_output: str) -> str:
    """Step 10: Metadata Package."""
    title = OutputExtractor.extract_recommended_title(step4_output)
    entities = OutputExtractor.extract_entities(step2_output)

    return f"""You are a YouTube metadata and discoverability expert.

TOPIC: {topic}
TITLE: {title or 'See Step 4 output below'}

ENTITY MAP:
High: {', '.join(entities.get('high', []))}
Medium: {', '.join(entities.get('medium', []))}

SCRIPT EXCERPT (for timestamps):
{step8_output[:3000]}

COMPETITIVE CONTEXT:
{step3_output[:1000]}

================================================================
TASK: Generate the complete metadata package.
================================================================

REQUIRED OUTPUT:

1. YOUTUBE DESCRIPTION (350-500 words)
   - Hook paragraph (first 2 lines visible before "Show More")
   - Key timestamps/chapters
   - Detailed content summary with entities
   - Related resources
   - Social links section
   - Hashtags (3-5)

2. TAGS (20-25 tags)
   Categorized by priority:
   - HIGH PRIORITY (8-10 tags): Direct topic + main entities
   - MEDIUM PRIORITY (8-10 tags): Related topics + secondary entities
   - LOW PRIORITY (5-7 tags): Broad category + trending related

3. THUMBNAIL TEXT OPTIONS (3 options)
   For each:
   - Primary text (2-4 words, high contrast)
   - Secondary text (optional, smaller)
   - Color scheme suggestion
   - Emotional trigger

4. YOUTUBE CHAPTERS (key moments)
   Format: 0:00 - Chapter Title
   Based on script structure.

5. SEARCH OPTIMIZATION STRATEGY
   - Primary search terms targeted
   - Long-tail keyword opportunities
   - Related search suggestions to capture

6. DISCOVERABILITY PREDICTION
   - Expected search ranking potential
   - Suggested video optimization (end screens, cards)
   - Cross-promotion opportunities

================================================================
"""


def _get_style_profiles() -> Dict[str, str]:
    """Style profiles for Step 8 script writing."""
    return {
        "Educational Authoritative": """
STYLE: Educational Authoritative
- Voice: Confident expert sharing deep knowledge
- Tone: Authoritative but accessible, like a respected professor
- Structure: Thesis → Evidence → Analysis → Conclusion
- Pacing: Measured, building complexity gradually
- Language: Precise terminology with clear explanations
- Hook: Bold claim or surprising fact backed by data
- Transitions: Logical flow - "Here's why this matters..." / "The evidence shows..."
- Examples: Research studies, historical precedents, expert quotes
- CTA: "Apply this knowledge" oriented""",

        "Storytelling Narrative": """
STYLE: Storytelling Narrative
- Voice: Master storyteller weaving a compelling narrative
- Tone: Dramatic, emotionally engaging, cinematic
- Structure: Setup → Rising Action → Climax → Resolution → Lesson
- Pacing: Variable - slow for tension, fast for excitement
- Language: Vivid imagery, sensory details, emotional language
- Hook: Open mid-action or with a mystery/conflict
- Transitions: Narrative bridges - "But then..." / "What nobody expected..."
- Examples: Personal anecdotes, case studies told as stories
- CTA: "Be part of this story" oriented""",

        "Investigative Journalistic": """
STYLE: Investigative Journalistic
- Voice: Tenacious reporter uncovering truth
- Tone: Objective but compelling, evidence-driven
- Structure: Question → Investigation → Evidence → Revelation → Implications
- Pacing: Building suspense with each new piece of evidence
- Language: Precise, factual, with strategic dramatic moments
- Hook: Expose a contradiction or hidden truth
- Transitions: "Our investigation revealed..." / "The documents show..."
- Examples: Data analysis, interviews, document evidence
- CTA: "Stay informed" / "Share this investigation" oriented""",

        "Conversational Friend": """
STYLE: Conversational Friend
- Voice: Knowledgeable friend sharing over coffee
- Tone: Warm, relatable, slightly informal
- Structure: Natural conversation flow with key insights
- Pacing: Relaxed but engaging, like natural speech
- Language: Contractions, colloquialisms, personal pronouns
- Hook: "You know what drives me crazy?" / relatable frustration
- Transitions: "Here's the thing though..." / "And this is where it gets interesting..."
- Examples: Personal experiences, common scenarios, "you know when..."
- CTA: Casual ask - "If this helped, you know what to do" oriented""",

        "Analytical Deep Dive": """
STYLE: Analytical Deep Dive
- Voice: Methodical analyst breaking down complexity
- Tone: Thoughtful, thorough, intellectually stimulating
- Structure: Framework → Layer 1 → Layer 2 → Layer 3 → Synthesis
- Pacing: Deliberate, each point fully explored before moving on
- Language: Analytical vocabulary, cause-effect language
- Hook: Present a complex puzzle or counterintuitive finding
- Transitions: "Let's go deeper..." / "When we analyze this further..."
- Examples: Data visualizations, comparisons, multi-factor analysis
- CTA: "Think critically about this" oriented""",

        "Provocative Challenger": """
STYLE: Provocative Challenger
- Voice: Bold contrarian challenging conventional wisdom
- Tone: Direct, confident, slightly confrontational
- Structure: Controversial claim → Dismantling old thinking → New framework → Proof → Challenge
- Pacing: Punchy, high-energy, no wasted words
- Language: Strong verbs, declarative sentences, rhetorical questions
- Hook: "Everything you know about X is wrong"
- Transitions: "But here's what nobody tells you..." / "Let me prove it..."
- Examples: Myth-busting, contrarian data, paradigm shifts
- CTA: "Challenge yourself" / "Prove me wrong" oriented""",

        "Documentary Observational": """
STYLE: Documentary Observational
- Voice: Thoughtful observer documenting reality
- Tone: Reflective, immersive, cinematic
- Structure: Scene setting → Observation → Context → Deeper meaning → Reflection
- Pacing: Cinematic - wide shots (context) to close-ups (details)
- Language: Descriptive, evocative, present-tense for immediacy
- Hook: Drop viewer into a vivid scene
- Transitions: Scene changes, time shifts, perspective shifts
- Examples: Real-world observations, cultural phenomena, human behavior
- CTA: "See the world differently" oriented""",

        "Tutorial Practical": """
STYLE: Tutorial Practical
- Voice: Experienced practitioner teaching by doing
- Tone: Clear, encouraging, results-focused
- Structure: Problem → Solution overview → Step-by-step → Common mistakes → Results
- Pacing: Methodical, with clear signposting of steps
- Language: Action verbs, imperative mood, concrete instructions
- Hook: Show the end result first, then teach how
- Transitions: "Step 1..." / "Now that we've done X, let's..."
- Examples: Live demonstrations, before/after, troubleshooting
- CTA: "Try this yourself" / "Show me your results" oriented""",
    }
