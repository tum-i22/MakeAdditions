"""
cd - change the working directory
"""

from ..Transformer import TransformerLlvm
from ...constants import MAKEANNOTATIONHINT


class TransformCd(TransformerLlvm):
    """ transform cd commands """

    @staticmethod
    def can_be_applied_on(cmd: str) -> bool:
        # Keep only makefile cd commands
        return cmd.startswith("cd ") and cmd.endswith(MAKEANNOTATIONHINT)

    @staticmethod
    def apply_transformation_on(cmd: str, container) -> str:
        return cmd