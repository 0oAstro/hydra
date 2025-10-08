"""
Stage 2: Specialized Reasoning Agents
Category-specific agents with chain-of-thought reasoning
"""

import re
import json
from typing import Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from config import (
    OPENAI_API_KEY, ANTHROPIC_API_KEY, GPT_MODEL, CLAUDE_MODEL,
    TEMPERATURE, CATEGORY_PROMPTS
)


class SpecializedReasoningAgent:
    """A specialized reasoning agent for a specific problem category"""
    
    def __init__(self, category: str, llm):
        self.category = category
        self.llm = llm
        self.prompt_template = CATEGORY_PROMPTS.get(category, self._get_general_prompt())
    
    def _get_general_prompt(self):
        """Fallback general reasoning prompt"""
        return """You are an expert problem solver.

Problem: {problem}

Answer Options:
1. {option_1}
2. {option_2}
3. {option_3}
4. {option_4}
5. {option_5}

Solve this step-by-step and select the correct option (1-5).
"""
    
    def solve(self, problem: str, options: Dict[str, str]) -> Dict:
        """
        Solve a reasoning problem
        
        Args:
            problem: The problem statement
            options: Dictionary with keys 'option_1' through 'option_5'
        
        Returns:
            Dictionary with reasoning and answer
        """
        # Format the prompt
        prompt = self.prompt_template.format(
            problem=problem,
            **options
        )
        
        # Add structured output instructions
        full_prompt = f"""{prompt}

Think step-by-step and provide:
1. Your detailed reasoning
2. The correct answer (1-5)
3. Your confidence (0.0-1.0)

Format your response as:
REASONING: [your detailed reasoning]
ANSWER: [option number 1-5]
CONFIDENCE: [0.0-1.0]
"""
        
        # Get response from LLM
        messages = [
            SystemMessage(content=f"You are an expert in {self.category}."),
            HumanMessage(content=full_prompt)
        ]
        
        response = self.llm.invoke(messages)
        response_text = response.content
        
        # Parse the response
        return self._parse_response(response_text)
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse LLM response to extract answer and reasoning"""
        # Try to extract structured response
        reasoning_match = re.search(r'REASONING:\s*(.+?)(?=ANSWER:|$)', response_text, re.DOTALL | re.IGNORECASE)
        answer_match = re.search(r'ANSWER:\s*(\d)', response_text, re.IGNORECASE)
        confidence_match = re.search(r'CONFIDENCE:\s*([0-9.]+)', response_text, re.IGNORECASE)
        
        # Extract values
        reasoning = reasoning_match.group(1).strip() if reasoning_match else response_text
        
        # Extract answer
        if answer_match:
            answer = int(answer_match.group(1))
        else:
            # Fallback: look for any number 1-5
            numbers = re.findall(r'\b([1-5])\b', response_text)
            answer = int(numbers[-1]) if numbers else 3
        
        # Extract confidence
        if confidence_match:
            confidence = float(confidence_match.group(1))
        else:
            confidence = 0.7  # Default confidence
        
        return {
            'problem_category': self.category,
            'final_answer': answer,
            'confidence': confidence,
            'explanation': reasoning[:500],  # Limit length
            'raw_response': response_text
        }


class MultiAgentReasoningSystem:
    """Coordinates multiple specialized agents"""
    
    def __init__(self):
        self.llm = self._initialize_llm()
        self.agents = self._create_agents()
    
    def _initialize_llm(self):
        """Initialize the language model"""
        if OPENAI_API_KEY:
            return ChatOpenAI(
                model=GPT_MODEL,
                temperature=TEMPERATURE,
                api_key=OPENAI_API_KEY
            )
        elif ANTHROPIC_API_KEY:
            return ChatAnthropic(
                model=CLAUDE_MODEL,
                temperature=TEMPERATURE,
                api_key=ANTHROPIC_API_KEY
            )
        else:
            raise ValueError("No API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY")
    
    def _create_agents(self) -> Dict:
        """Create specialized agents for each category"""
        agents = {}
        for category in CATEGORY_PROMPTS.keys():
            agents[category] = SpecializedReasoningAgent(category, self.llm)
        return agents
    
    def solve_problem(self, problem: str, options: Dict[str, str], 
                     category: Optional[str] = None) -> Dict:
        """
        Solve a problem using the appropriate specialized agent
        
        Args:
            problem: Problem statement
            options: Answer options
            category: Known category (optional)
        
        Returns:
            Solution dictionary
        """
        # Get the appropriate agent
        if category and category in self.agents:
            agent = self.agents[category]
        else:
            # Use first agent as fallback
            agent = list(self.agents.values())[0]
        
        # Solve the problem
        solution = agent.solve(problem, options)
        
        # Add metadata
        solution['category_used'] = agent.category
        
        return solution

