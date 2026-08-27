from gemini_service import generate_response


def generate_notes(context, keywords, learning_level, study_mode):
    """
    Generate comprehensive, level-appropriate study notes with diagrams and flowcharts.
    """
    
    # Customize prompt based on learning level
    level_instructions = {
        "Beginner": """
- Use simple, clear language
- Define all technical terms
- Include basic examples
- Focus on fundamental concepts
- Use analogies to explain complex ideas
""",
        "Intermediate": """
- Balance technical terminology with explanations
- Include practical applications
- Connect concepts together
- Provide detailed examples
- Include comparative analysis
""",
        "Advanced": """
- Use precise technical language
- Include advanced concepts and theory
- Analyze complex relationships
- Provide in-depth analysis
- Include edge cases and nuances
"""
    }
    
    # Customize based on study mode
    mode_instructions = {
        "Quick Revision": """
- Create concise bullet points
- Focus on key facts and formulas
- Include quick-reference tables
- Highlight must-know information
- Use memory aids and mnemonics
""",
        "Exam Preparation": """
- Focus on exam-relevant topics
- Include sample questions within notes
- Highlight commonly tested concepts
- Provide tips and tricks
- Create comprehensive coverage
""",
        "Detailed Study": """
- Provide in-depth explanations
- Include background context
- Add extended examples
- Explore related concepts
- Include additional insights
"""
    }

    prompt = f"""You are an expert academic tutor creating professional study notes.

STUDENT PROFILE:
- Learning Level: {learning_level}
- Study Mode: {study_mode}

LEVEL-SPECIFIC APPROACH:
{level_instructions[learning_level]}

MODE-SPECIFIC APPROACH:
{mode_instructions[study_mode]}

KEY TOPICS TO COVER:
{", ".join(keywords[:10])}

FORMATTING REQUIREMENTS:

1. **Structure**: Use clear hierarchy with main topics, subtopics, and key points

2. **Visual Elements**: Include these where relevant:
   - Create ASCII flowcharts using arrows (→, ↓, ←, ↑) and boxes
   - Use ASCII diagrams with lines, boxes (┌─┐│└┘), and connecting symbols
   - Create process flows showing step-by-step sequences
   - Use tables for comparisons
   - Include concept maps showing relationships

3. **Content Organization**:
   - Start with an overview/introduction
   - Use numbered sections for main topics
   - Use bullet points (•) for key points
   - Use indentation for hierarchies
   - Include "💡 Key Insight" callouts for important concepts
   - Add "⚠️ Common Mistake" warnings where appropriate
   - Use "📌 Remember" for critical facts

4. **Examples**: Provide relevant examples for each major concept

5. **Summary**: End with a concise summary of key takeaways

STUDY MATERIAL:
{context}

Generate comprehensive, well-structured study notes with visual elements (flowcharts, diagrams, tables) that are appropriate for a {learning_level} student in {study_mode} mode.

Make the notes visually engaging using ASCII art for diagrams and flowcharts. Use markdown formatting extensively."""

    return generate_response(prompt, temperature=0.5)