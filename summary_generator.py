from gemini_service import generate_response


def generate_summary(context, keywords, summary_length="medium"):
    """
    Generate a concise summary of the study material.
    
    Args:
        context: The text content to summarize
        keywords: Important keywords from the content
        summary_length: "short" (paragraph), "medium" (few paragraphs), "long" (detailed)
    """
    
    length_guide = {
        "short": "1-2 paragraphs, capturing only the absolute essentials",
        "medium": "3-5 paragraphs, covering main points and key details",
        "long": "6-10 paragraphs, comprehensive overview with important details"
    }
    
    prompt = f"""Create a clear, concise summary of the study material provided.

SUMMARY LENGTH: {summary_length.upper()} - {length_guide[summary_length]}

KEY TOPICS TO COVER:
{", ".join(keywords[:15])}

SUMMARY REQUIREMENTS:
1. Start with a brief overview sentence
2. Cover all major topics and themes
3. Include key facts, concepts, and ideas
4. Use clear, straightforward language
5. Organize logically (chronological, thematic, or hierarchical)
6. End with a concluding statement

FORMAT:
- Use paragraphs (not bullet points)
- Write in present tense
- Be objective and factual
- Maintain academic tone

STUDY MATERIAL:
{context}

Write the summary now:"""

    return generate_response(prompt, temperature=0.4, max_tokens=3000)
