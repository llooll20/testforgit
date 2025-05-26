from agents.registry import intent_classifier, intent_user_proxy


def classify_intent(prompt: str) -> str:
    # Reset to ensure clean state
    intent_classifier.reset()
    intent_user_proxy.reset()

    # Run classification dialogue
    intent_user_proxy.initiate_chat(
        recipient=intent_classifier,
        message=prompt,
    )

    # Receiving result from the classifier
    # Only 'play', 'open', .. intent for the return state.
    final_message = intent_classifier.chat_messages[-1]["content"].strip().lower()
    return final_message if final_message in {"play", "open"} else "unknown"
