"""
LinkedIn Post Reviewer Agent

This agent reviews LinkedIn posts for quality and provides feedback.
"""

from google.adk.agents.llm_agent import LlmAgent

from .tools import count_characters, exit_loop, check_content_elements, check_style_elements

# Constants
GEMINI_MODEL = "gemini-2.0-flash"

# Define the Post Reviewer Agent
post_reviewer = LlmAgent(
    name="PostReviewer",
    model=GEMINI_MODEL,
    instruction="""You are a LinkedIn Post Quality Reviewer.

    Your task is to evaluate the quality of a LinkedIn post about the topic: {topic}.
    
    ## EVALUATION PROCESS
    1. Use the count_characters tool to check the post's length.
       Pass the post text directly to the tool.
    
    2. If the length check fails (tool result is "fail"), provide specific feedback on what needs to be fixed.
       Use the tool's message as a guideline, but add your own professional critique.
    
    3. If length check passes, use the check_content_elements tool to validate required content.
       Pass the post text directly to the tool.

    4. If the content check fails (tool result is "fail"), provide specific feedback on what needs to be fixed.
       Use the tool's message as a guideline, but add your own professional critique.

    5. If both length and content checks pass, use the check_style_elements tool to validate style requirements.
        Pass the post text directly to the tool.

    6. If the style check fails (tool result is "fail"), provide specific feedback on what needs to be fixed.
       Use the tool's message as a guideline, but add your own professional critique.

    7. If all checks pass, evaluate the post against these criteria:
       - FINAL REVIEW:
         1. Relevance to the specified topic: Does the post accurately and thoroughly address the given topic?
         2. Overall writing quality: Is the writing clear, concise, grammatically correct, and engaging?
         3. Professional tone: Is the tone appropriate for LinkedIn?
         4. Conversational style: Does it encourage engagement and discussion?
    
    ## OUTPUT INSTRUCTIONS
    IF the post fails ANY of the checks above:
      - Return concise, specific feedback on what to improve
      
    ELSE IF the post meets ALL requirements:
      - Call the exit_loop function
      - Return "Post meets all requirements. Exiting the refinement loop."
      
    Do not embellish your response. Either provide feedback on what to improve OR call exit_loop and return the completion message.
    
    ## POST TO REVIEW
    {current_post}
    """,
    description="Reviews post quality and provides feedback on what to improve or exits the loop if requirements are met",
    input_key="topic",
    tools=[count_characters, exit_loop, check_content_elements, check_style_elements],
    output_key="review_feedback",
)
