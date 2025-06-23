"""
Tools for LinkedIn Post Reviewer Agent

This module provides tools for analyzing and validating LinkedIn posts.
"""

from typing import Any, Dict

from google.adk.tools.tool_context import ToolContext


def count_characters(text: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Tool to count characters in the provided text and provide length-based feedback.
    Updates review_status in the state based on length requirements.

    Args:
        text: The text to analyze for character count
        tool_context: Context for accessing and updating session state

    Returns:
        Dict[str, Any]: Dictionary containing:
            - result: 'fail' or 'pass'
            - char_count: number of characters in text
            - message: feedback message about the length
    """
    char_count = len(text)
    MIN_LENGTH = 1000
    MAX_LENGTH = 1500

    print("\n----------- TOOL DEBUG -----------")
    print(f"Checking text length: {char_count} characters")
    print("----------------------------------\n")

    if char_count < MIN_LENGTH:
        chars_needed = MIN_LENGTH - char_count
        tool_context.state["review_status"] = "fail"
        return {
            "result": "fail",
            "char_count": char_count,
            "chars_needed": chars_needed,
            "message": f"Post is too short. Add {chars_needed} more characters to reach minimum length of {MIN_LENGTH}.",
        }
    elif char_count > MAX_LENGTH:
        chars_to_remove = char_count - MAX_LENGTH
        tool_context.state["review_status"] = "fail"
        return {
            "result": "fail",
            "char_count": char_count,
            "chars_to_remove": chars_to_remove,
            "message": f"Post is too long. Remove {chars_to_remove} characters to meet maximum length of {MAX_LENGTH}.",
        }
    else:
        tool_context.state["review_status"] = "pass"
        return {
            "result": "pass",
            "char_count": char_count,
            "message": f"Post length is good ({char_count} characters).",
        }


def exit_loop(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Call this function ONLY when the post meets all quality requirements,
    signaling the iterative process should end.

    Args:
        tool_context: Context for tool execution

    Returns:
        Empty dictionary
    """
    print("\n----------- EXIT LOOP TRIGGERED -----------")
    print("Post review completed successfully")
    print("Loop will exit now")
    print("------------------------------------------\n")

    tool_context.actions.escalate = True
    return {}

def check_content_elements(text: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Tool to check for the presence of required content elements in the LinkedIn post.

    Args:
        text: The text of the LinkedIn post to analyze.
        tool_context: Context for accessing and updating session state.

    Returns:
        Dict[str, Any]: Dictionary containing:
            - result: 'pass' or 'fail'
            - missing_elements: A list of elements that are missing.
            - message: A feedback message.
    """
    missing_elements = []

    # Check for @aiwithbrandon mention
    if "@aiwithbrandon" not in text:
        missing_elements.append("Mentions @aiwithbrandon")

    # Check for multiple ADK capabilities (at least 4)
    adk_capabilities = [
        "basic agent implementation",
        "tool integration",
        "LiteLLM",
        "sessions and memory",
        "persistent storage",
        "multi-agent orchestration",
        "stateful multi-agent systems",
        "callback systems",
        "sequential agents",
        "parallel agents",
        "loop agents",
    ]
    found_capabilities = [cap for cap in adk_capabilities if cap.lower() in text.lower()]
    if len(found_capabilities) < 4:
        missing_elements.append("Lists at least 4 ADK capabilities")

    # Check for clear call-to-action (example keywords)
    call_to_action_keywords = ["connect with me", "follow me", "learn more", "get in touch"]
    if not any(keyword in text.lower() for keyword in call_to_action_keywords):
        missing_elements.append("Has a clear call-to-action")

    # Check for practical applications (example keywords)
    practical_application_keywords = ["real-world", "practical", "applications", "use cases"]
    if not any(keyword in text.lower() for keyword in practical_application_keywords):
        missing_elements.append("Includes practical applications")

    # Check for genuine enthusiasm (example keywords)
    enthusiasm_keywords = ["excited", "thrilled", "love", "amazing", "fantastic", "great"]
    if not any(keyword in text.lower() for keyword in enthusiasm_keywords):
        missing_elements.append("Shows genuine enthusiasm")

    if missing_elements:
        tool_context.state["review_status"] = "fail"
        return {
            "result": "fail",
            "missing_elements": missing_elements,
            "message": "The post is missing some required content elements."
        }
    else:
        return {
            "result": "pass",
            "missing_elements": [],
            "message": "All required content elements are present."
        }

def check_style_elements(text: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Tool to check for style requirements in the LinkedIn post.

    Args:
        text: The text of the LinkedIn post to analyze.
        tool_context: Context for accessing and updating session state.

    Returns:
        Dict[str, Any]: Dictionary containing:
            - result: 'pass' or 'fail'
            - issues: A list of style issues found.
            - message: A feedback message.
    """
    style_issues = []

    # Check for emojis
    if any(char for char in text if char in "😀😃😄😁😆😅😂🤣🥲😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🥸🤩🥳😏😒😞😔😟😕🙁☹️😣😖😫😩🥺😢😭😤😠😡🤬🤯😳🥵🥶😱😨😰😥😓🤗🤔🫣🤫🫠🤥😶🫥😐😑🫨😬🫠🙄😯😦😧😮😲🥱😴🤤😪😵💫🤐🥴🤢🤮🤧😷🤒🤕🤑🤠😈👿👹👺🤡💩👻💀☠️👽👾🤖🎃😺😸😹😻😼😽🙀😿😾"): # Simplified emoji check
        style_issues.append("NO emojis")

    # Check for hashtags
    if "#" in text:
        style_issues.append("NO hashtags")

    # Check for professional tone (subjective, but can look for informal language)
    informal_keywords = ["lol", "lmao", "btw", "ikr", "omg", "wtf"]
    if any(keyword in text.lower() for keyword in informal_keywords):
        style_issues.append("Professional tone (avoid informal language)")

    # Check for conversational style (subjective, hard to automate perfectly)
    # This might require more advanced NLP, for now, a simple check.
    # For example, looking for direct address, questions, etc.

    # Check for clear and concise writing (subjective, hard to automate perfectly)
    # This might require more advanced NLP.

    if style_issues:
        tool_context.state["review_status"] = "fail"
        return {
            "result": "fail",
            "issues": style_issues,
            "message": "The post has some style issues."
        }
    else:
        return {
            "result": "pass",
            "issues": [],
            "message": "All style requirements are met."
        }
