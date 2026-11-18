class AgentError(Exception):
    """Exception générale de DevAgent."""
    pass

class ToolNotFoundError(AgentError):
    """Outil introuvable dans le registre de l'agent."""
    pass

class ToolExecutionError(AgentError):
    """Erreur pendant l'exécution d'un outil."""
    pass