"""Debug utilities for the A2A platform."""

import logging

logger = logging.getLogger(__name__)

def debug_message_structure(context, component_name="Unknown"):
    """Debug helper to understand message structure."""
    try:
        logger.info(f"[{component_name}] Debugging message structure:")
        
        if not context.message:
            logger.info(f"[{component_name}] No message in context")
            return "No message"
        
        message = context.message
        logger.info(f"[{component_name}] Message type: {type(message)}")
        logger.info(f"[{component_name}] Message attributes: {dir(message)}")
        
        # Try different ways to extract content
        content = ""
        
        if hasattr(message, 'artifacts') and message.artifacts:
            logger.info(f"[{component_name}] Found artifacts: {len(message.artifacts)}")
            for i, artifact in enumerate(message.artifacts):
                logger.info(f"[{component_name}] Artifact {i} type: {type(artifact)}")
                if hasattr(artifact, 'parts') and artifact.parts:
                    for j, part in enumerate(artifact.parts):
                        logger.info(f"[{component_name}] Part {j} type: {type(part)}")
                        if hasattr(part, 'text') and part.text:
                            content += part.text
                            logger.info(f"[{component_name}] Found text in part.text: {part.text[:100]}...")
                        elif hasattr(part, 'root') and hasattr(part.root, 'text'):
                            content += part.root.text
                            logger.info(f"[{component_name}] Found text in part.root.text: {part.root.text[:100]}...")
        
        elif hasattr(message, 'content'):
            content = str(message.content)
            logger.info(f"[{component_name}] Found content: {content[:100]}...")
        
        elif hasattr(message, 'text'):
            content = message.text
            logger.info(f"[{component_name}] Found text: {content[:100]}...")
        
        else:
            logger.info(f"[{component_name}] No recognizable content format")
            content = str(message)[:100] if message else "Empty message"
        
        return content or "Hello"
        
    except Exception as e:
        logger.error(f"[{component_name}] Error in debug_message_structure: {e}")
        return "Debug error"

def extract_message_content_safely(context, component_name="Unknown"):
    """Safely extract message content with debugging."""
    try:
        if not context.message:
            return "Hello"
        
        message = context.message
        content = ""
        
        # Try artifacts first (A2A format)
        if hasattr(message, 'artifacts') and message.artifacts:
            for artifact in message.artifacts:
                if hasattr(artifact, 'parts') and artifact.parts:
                    for part in artifact.parts:
                        if hasattr(part, 'text') and part.text:
                            content += part.text
                        elif hasattr(part, 'root') and hasattr(part.root, 'text'):
                            content += part.root.text
        
        # Try direct content
        elif hasattr(message, 'content') and message.content:
            content = str(message.content)
        
        # Try text attribute
        elif hasattr(message, 'text') and message.text:
            content = message.text
        
        # Fallback to string representation
        else:
            content = str(message) if message else ""
        
        result = content.strip() if content else "Hello"
        logger.debug(f"[{component_name}] Extracted content: {result[:100]}...")
        return result
        
    except Exception as e:
        logger.error(f"[{component_name}] Error extracting message content: {e}")
        return "Hello"
