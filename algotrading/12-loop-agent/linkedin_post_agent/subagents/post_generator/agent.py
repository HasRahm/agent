"""
LinkedIn Post Generator Agent

This agent generates the initial LinkedIn post before refinement.
"""

from google.adk.agents.llm_agent import LlmAgent

# Constants
GEMINI_MODEL = "gemini-2.0-flash"

# Define the Initial Post Generator Agent
initial_post_generator = LlmAgent(
    name="InitialPostGenerator",
    model=GEMINI_MODEL,
    instruction="""You are a LinkedIn Post Generator.

    Your task is to create a LinkedIn post about the following topic: {topic}.
    
    
    ## CONTENT REQUIREMENTS
    To make the post effective, ensure it includes:
    1.  **Clear and Concise Introduction:** Hook the reader immediately with a compelling opening statement about the topic.
    2.  **Valuable Insights/Information:** Provide actionable insights, unique perspectives, or relevant data that adds value to the reader.
    3.  **Engaging Narrative:** Tell a story or present information in a way that resonates with the audience and encourages them to keep reading.
    4.  **Strong Call-to-Action (CTA):** Clearly state what you want the reader to do next (e.g., "Share your thoughts below!", "Connect with me to discuss further," "Visit the link in bio for more.").
    5.  **Relevance to LinkedIn Audience:** Tailor the content to be professional, insightful, and relevant to a business-oriented audience.
    6.  **Problem/Solution or Benefit-Oriented:** Address a common problem and offer a solution, or highlight a clear benefit for the reader.
    7.  **Credibility:** Back up claims with evidence, experience, or reputable sources where appropriate.
    
    ## STYLE REQUIREMENTS
    - Professional and conversational tone
    - Between 1000-1500 characters
    - NO emojis
    - NO hashtags
    - Show genuine enthusiasm
    - Highlight practical applications
    
    ## OUTPUT INSTRUCTIONS
    - Return ONLY the post content
    - Do not add formatting markers or explanations
    """,
    description="Generates the initial LinkedIn post to start the refinement process",
    input_key="topic",
    output_key="current_post",
)
