"""QFC v2.0 AI Inference Types."""

from pydantic import BaseModel


class InferenceModel(BaseModel):
    """Approved model in the registry."""
    name: str
    version: str
    min_memory_mb: int
    min_tier: str
    approved: bool = True


class InferenceStats(BaseModel):
    """Network-wide inference statistics."""
    tasks_completed: int
    avg_time_ms: float
    flops_total: int
    pass_rate: float


class ComputeInfo(BaseModel):
    """Node compute capability information."""
    backend: str
    supported_models: list[str] = []
    gpu_memory_mb: int = 0
    inference_score: int = 0
    gpu_tier: str = "Cold"
    provides_compute: bool = False


class InferenceTask(BaseModel):
    """Inference task assigned to a miner."""
    task_id: str
    epoch: int
    task_type: str
    model_name: str
    model_version: str
    input_data: str
    deadline: int


class InferenceProofResult(BaseModel):
    """Result of a proof submission."""
    accepted: bool
    spot_checked: bool = False
    message: str = ""


class PublicTaskResult(BaseModel):
    """Public inference task result."""
    task_id: str
    status: str
    result_data: str | None = None
    miner_address: str | None = None
    execution_time_ms: int | None = None
    fee: int | None = None
