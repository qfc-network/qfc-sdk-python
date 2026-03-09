"""Inference client for high-level AI inference operations."""

import base64
import time

from eth_account import Account
from eth_account.messages import encode_defunct

from qfc_sdk.provider import QfcProvider
from qfc_sdk.types import InferenceModel, PublicTaskResult


class InferenceClient:
    """High-level client for AI inference operations.

    Examples:
        >>> inference = InferenceClient(provider)
        >>> models = inference.get_models()
        >>> fee = inference.estimate_fee("qfc-embed-small", "embedding")
    """

    def __init__(self, provider: QfcProvider):
        """Initialize the inference client.

        Args:
            provider: QFC provider
        """
        self._provider = provider

    def get_models(self) -> list[InferenceModel]:
        """Get list of approved inference models.

        Returns:
            List of supported models
        """
        return self._provider.get_supported_models()

    def estimate_fee(
        self,
        model_id: str,
        task_type: str,
        input_size: int = 0,
    ) -> int:
        """Estimate fee for an inference task.

        Args:
            model_id: Model identifier
            task_type: Type of task (e.g. "embedding", "completion")
            input_size: Input data size in bytes

        Returns:
            Estimated fee in wei
        """
        result = self._provider._rpc_call("qfc_estimateInferenceFee", [{
            "modelId": model_id,
            "taskType": task_type,
            "inputSize": input_size,
        }])
        return int(result, 16) if isinstance(result, str) else int(result)

    def submit_task(
        self,
        model_id: str,
        task_type: str,
        input_data: str,
        max_fee: int,
        private_key: str,
    ) -> str:
        """Submit an inference task.

        Signs the payload with eth_account. Input data is auto-base64
        encoded if it is a plain string.

        Args:
            model_id: Model identifier
            task_type: Type of task
            input_data: Input data (auto-base64 encoded if string)
            max_fee: Maximum fee in wei
            private_key: Private key for signing

        Returns:
            Task ID
        """
        # Auto-base64 encode if input_data looks like a plain string
        try:
            base64.b64decode(input_data, validate=True)
            encoded_data = input_data
        except Exception:
            encoded_data = base64.b64encode(input_data.encode()).decode()

        # Sign the payload
        message_text = f"{model_id}:{task_type}:{encoded_data}:{max_fee}"
        message = encode_defunct(text=message_text)
        signed = Account.sign_message(message, private_key=private_key)
        signature = signed.signature.hex()

        return self._provider._rpc_call("qfc_submitSignedTask", [{
            "modelId": model_id,
            "taskType": task_type,
            "inputData": encoded_data,
            "maxFee": hex(max_fee),
            "signature": signature,
        }])

    def get_task_status(self, task_id: str) -> PublicTaskResult:
        """Get status of an inference task.

        Args:
            task_id: Task identifier

        Returns:
            Task status
        """
        return self._provider.get_public_task_status(task_id)

    def wait_for_result(
        self,
        task_id: str,
        timeout: int = 120,
        interval: int = 2,
    ) -> PublicTaskResult:
        """Wait for an inference task to complete.

        Args:
            task_id: Task identifier
            timeout: Timeout in seconds
            interval: Poll interval in seconds

        Returns:
            Final task status

        Raises:
            TimeoutError: If the task does not complete within timeout
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            status = self.get_task_status(task_id)
            if status.status in ("Completed", "Failed"):
                return status
            time.sleep(interval)
        raise TimeoutError(
            f"Task {task_id} did not complete within {timeout} seconds"
        )

    def list_tasks(
        self,
        submitter: str | None = None,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[PublicTaskResult]:
        """List inference tasks.

        Args:
            submitter: Filter by submitter address
            status: Filter by task status
            limit: Maximum results to return
            offset: Offset for pagination

        Returns:
            List of task results
        """
        params: dict = {
            "limit": limit,
            "offset": offset,
        }
        if submitter is not None:
            params["submitter"] = submitter
        if status is not None:
            params["status"] = status

        results = self._provider._rpc_call("qfc_listPublicTasks", [params])
        return [
            PublicTaskResult(
                task_id=r["taskId"],
                status=r["status"],
                result_data=r.get("resultData"),
                miner_address=r.get("minerAddress"),
                execution_time_ms=r.get("executionTimeMs"),
                fee=int(r["fee"]) if r.get("fee") is not None else None,
            )
            for r in results
        ]
