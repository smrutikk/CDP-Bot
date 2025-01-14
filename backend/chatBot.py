import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class CDP(Enum):
    SEGMENT = "segment"
    MPARTICLE = "mparticle"
    LYTICS = "lytics"
    ZEOTAP = "zeotap"

@dataclass
class Question:
    text: str
    cdp: Optional[CDP]
    task_type: str
    is_comparison: bool

class CDPChatbot:
    def __init__(self):
        self.cdp_keywords = {
            CDP.SEGMENT: ["segment", "segments"],
            CDP.MPARTICLE: ["mparticle", "mparticles"],
            CDP.LYTICS: ["lytics"],
            CDP.ZEOTAP: ["zeotap"]
        }
        
        # Common CDP tasks and their variations
        self.task_patterns = {
            "source_setup": r"(set up|create|add|configure).*(source|integration)",
            "profile_creation": r"(create|setup|configure).*(profile|user profile)",
            "audience_building": r"(create|build|make).*(audience|segment)",
            "data_integration": r"(integrate|connect|sync).*(data)"
        }
        
        # Initialize knowledge base (in practice, this would be loaded from documentation)
        self.knowledge_base = self._initialize_knowledge_base()

    def _initialize_knowledge_base(self) -> Dict:
        """Initialize the knowledge base with basic CDP documentation information."""
        return {
            CDP.SEGMENT: {
                "source_setup": [
                    "To set up a new source in Segment:",
                    "1. Navigate to Connections > Sources",
                    "2. Click 'Add Source'",
                    "3. Select your source type",
                    "4. Configure the source settings",
                    "5. Verify the connection"
                ],
                # Add more tasks...
            },
            # Add other CDPs...
        }

    def _parse_question(self, question: str) -> Question:
        """Parse the input question to identify CDP, task type, and if it's a comparison."""
        question_lower = question.lower()
        
        # Detect CDP
        detected_cdp = None
        for cdp, keywords in self.cdp_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                detected_cdp = cdp
                break
        
        # Detect task type
        detected_task = None
        for task, pattern in self.task_patterns.items():
            if re.search(pattern, question_lower):
                detected_task = task
                break
        
        # Check if it's a comparison question
        is_comparison = any(word in question_lower for word in ["compare", "difference", "versus", "vs"])
        
        return Question(
            text=question,
            cdp=detected_cdp,
            task_type=detected_task,
            is_comparison=is_comparison
        )

    def _get_answer_from_knowledge_base(self, parsed_question: Question) -> str:
        """Retrieve relevant answer from knowledge base based on parsed question."""
        if parsed_question.is_comparison:
            return self._handle_comparison_question(parsed_question)
        
        if not parsed_question.cdp or not parsed_question.task_type:
            return self._handle_invalid_question()
        
        try:
            answer = self.knowledge_base[parsed_question.cdp][parsed_question.task_type]
            return "\n".join(answer)
        except KeyError:
            return "I'm sorry, I don't have specific information about that task in my knowledge base."

    def _handle_comparison_question(self, parsed_question: Question) -> str:
        """Handle questions comparing different CDPs."""
        # Implementation for comparison logic
        return "Comparison functionality is under development."

    def _handle_invalid_question(self) -> str:
        """Handle questions that are not CDP-related or are invalid."""
        return ("I'm sorry, I can only answer questions about CDP platforms "
                "(Segment, mParticle, Lytics, and Zeotap) and their functionalities. "
                "Please rephrase your question to be related to these platforms.")

    def answer_question(self, question: str) -> str:
        """Main method to process and answer questions."""
        parsed_question = self._parse_question(question)
        return self._get_answer_from_knowledge_base(parsed_question)

    def validate_question_size(self, question: str) -> bool:
        """Validate if the question size is within acceptable limits."""
        return 10 <= len(question) <= 1000  # Arbitrary limits for demonstration