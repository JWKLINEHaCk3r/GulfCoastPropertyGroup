"""
Base AI Agent framework for multi-agent orchestration
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


class AIAgent(ABC):
    """Base class for all AI agents in the ecosystem"""
    
    def __init__(self, name: str, description: str, model: str = "gpt-4", temperature: float = 0.7):
        """
        Initialize an AI agent
        
        Args:
            name: Agent name
            description: Agent description
            model: LLM model to use (gpt-4, claude-3, etc.)
            temperature: LLM temperature parameter (0-1)
        """
        self.name = name
        self.description = description
        self.model = model
        self.temperature = temperature
        self.created_at = datetime.utcnow()
        self.execution_count = 0
        self.total_tokens_used = 0
        
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's primary function
        
        Args:
            task: Task configuration with required parameters
            
        Returns:
            Result dictionary
        """
        pass
    
    @abstractmethod
    def validate_task(self, task: Dict[str, Any]) -> bool:
        """
        Validate that task has required parameters
        
        Args:
            task: Task to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    async def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for agent execution
        
        Args:
            task: Task to execute
            
        Returns:
            Result with status, data, and metadata
        """
        logger.info(f"Agent '{self.name}' starting task: {task}")
        
        if not self.validate_task(task):
            return {
                "status": "error",
                "agent": self.name,
                "error": "Task validation failed",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        try:
            self.execution_count += 1
            result = await self.execute(task)
            
            result["status"] = "success"
            result["agent"] = self.name
            result["execution_id"] = f"{self.name}_{self.execution_count}_{datetime.utcnow().timestamp()}"
            result["timestamp"] = datetime.utcnow().isoformat()
            
            logger.info(f"Agent '{self.name}' completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Agent '{self.name}' failed: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def log_execution(self, result: Dict[str, Any]):
        """Log agent execution details"""
        logger.info(f"Agent {self.name} | Status: {result.get('status')} | "
                   f"Tokens: {result.get('tokens_used', 0)} | "
                   f"Execution ID: {result.get('execution_id')}")


class AgentOrchestrator:
    """
    Orchestrates multiple AI agents working together
    """
    
    def __init__(self):
        """Initialize the orchestrator"""
        self.agents: Dict[str, AIAgent] = {}
        self.execution_history: List[Dict[str, Any]] = []
        
    def register_agent(self, agent: AIAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.name] = agent
        logger.info(f"Agent '{agent.name}' registered with orchestrator")
        
    async def execute_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a workflow with multiple agents
        
        Args:
            workflow: Workflow definition with steps and dependencies
            
        Returns:
            Aggregated results from all agents
        """
        workflow_id = f"workflow_{datetime.utcnow().timestamp()}"
        results = {"workflow_id": workflow_id, "steps": [], "status": "running"}
        
        try:
            for step in workflow.get("steps", []):
                agent_name = step.get("agent")
                task = step.get("task", {})
                
                if agent_name not in self.agents:
                    results["steps"].append({
                        "agent": agent_name,
                        "status": "error",
                        "error": f"Agent '{agent_name}' not found"
                    })
                    continue
                
                # Add previous results to context if needed
                if step.get("use_previous_results", False) and results["steps"]:
                    task["context"] = results["steps"][-1]
                
                agent = self.agents[agent_name]
                result = await agent.run(task)
                result["step_number"] = len(results["steps"]) + 1
                
                results["steps"].append(result)
                
                # Stop on error unless specified otherwise
                if result["status"] == "error" and not step.get("continue_on_error", False):
                    results["status"] = "failed"
                    break
            
            results["status"] = "completed"
            self.execution_history.append(results)
            return results
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}", exc_info=True)
            results["status"] = "error"
            results["error"] = str(e)
            return results
    
    def get_agent_stats(self, agent_name: str) -> Dict[str, Any]:
        """Get statistics for a specific agent"""
        if agent_name not in self.agents:
            return {"error": f"Agent '{agent_name}' not found"}
        
        agent = self.agents[agent_name]
        return {
            "name": agent.name,
            "description": agent.description,
            "model": agent.model,
            "execution_count": agent.execution_count,
            "total_tokens_used": agent.total_tokens_used,
            "created_at": agent.created_at.isoformat()
        }


# Global orchestrator instance
_orchestrator: Optional[AgentOrchestrator] = None


def get_orchestrator() -> AgentOrchestrator:
    """Get or create the global orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgentOrchestrator()
    return _orchestrator
