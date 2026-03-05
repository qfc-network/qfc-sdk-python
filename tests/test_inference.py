"""Tests for v2.0 inference types."""

import pytest
from qfc_sdk.types import (
    InferenceModel,
    InferenceStats,
    ComputeInfo,
    InferenceTask,
    InferenceProofResult,
    PublicTaskResult,
)


class TestInferenceModel:
    """Test InferenceModel type."""

    def test_basic_creation(self):
        model = InferenceModel(
            name="qfc-embed-small",
            version="v1.0",
            min_memory_mb=512,
            min_tier="Cold",
        )
        assert model.name == "qfc-embed-small"
        assert model.version == "v1.0"
        assert model.min_memory_mb == 512
        assert model.min_tier == "Cold"
        assert model.approved is True

    def test_unapproved_model(self):
        model = InferenceModel(
            name="custom-model",
            version="v0.1",
            min_memory_mb=4096,
            min_tier="Hot",
            approved=False,
        )
        assert model.approved is False


class TestInferenceStats:
    """Test InferenceStats type."""

    def test_basic_creation(self):
        stats = InferenceStats(
            tasks_completed=42000,
            avg_time_ms=150.5,
            flops_total=9876543210,
            pass_rate=98.5,
        )
        assert stats.tasks_completed == 42000
        assert stats.avg_time_ms == 150.5
        assert stats.flops_total == 9876543210
        assert stats.pass_rate == 98.5


class TestComputeInfo:
    """Test ComputeInfo type."""

    def test_basic_creation(self):
        info = ComputeInfo(
            backend="Metal",
            supported_models=["qfc-embed-small", "qfc-embed-medium"],
            gpu_memory_mb=16384,
            inference_score=6699,
            gpu_tier="Warm",
            provides_compute=True,
        )
        assert info.backend == "Metal"
        assert len(info.supported_models) == 2
        assert info.gpu_memory_mb == 16384
        assert info.gpu_tier == "Warm"
        assert info.provides_compute is True

    def test_defaults(self):
        info = ComputeInfo(backend="CPU")
        assert info.supported_models == []
        assert info.gpu_memory_mb == 0
        assert info.gpu_tier == "Cold"
        assert info.provides_compute is False


class TestInferenceTask:
    """Test InferenceTask type."""

    def test_basic_creation(self):
        task = InferenceTask(
            task_id="0x" + "ab" * 32,
            epoch=100,
            task_type="embedding",
            model_name="qfc-embed-small",
            model_version="v1.0",
            input_data="0xdeadbeef",
            deadline=1704153600000,
        )
        assert task.task_id == "0x" + "ab" * 32
        assert task.epoch == 100
        assert task.task_type == "embedding"
        assert task.model_name == "qfc-embed-small"


class TestInferenceProofResult:
    """Test InferenceProofResult type."""

    def test_accepted(self):
        result = InferenceProofResult(accepted=True, spot_checked=False, message="OK")
        assert result.accepted is True
        assert result.spot_checked is False

    def test_rejected(self):
        result = InferenceProofResult(accepted=False, message="Epoch mismatch")
        assert result.accepted is False
        assert result.message == "Epoch mismatch"

    def test_defaults(self):
        result = InferenceProofResult(accepted=True)
        assert result.spot_checked is False
        assert result.message == ""


class TestPublicTaskResult:
    """Test PublicTaskResult type."""

    def test_completed(self):
        result = PublicTaskResult(
            task_id="0x" + "cd" * 32,
            status="Completed",
            result_data="0xresultdata",
            miner_address="0x" + "1" * 40,
            execution_time_ms=120,
            fee=10**15,
        )
        assert result.status == "Completed"
        assert result.result_data == "0xresultdata"
        assert result.fee == 10**15

    def test_pending(self):
        result = PublicTaskResult(
            task_id="0x" + "cd" * 32,
            status="Pending",
        )
        assert result.status == "Pending"
        assert result.result_data is None
        assert result.miner_address is None
        assert result.execution_time_ms is None
        assert result.fee is None
