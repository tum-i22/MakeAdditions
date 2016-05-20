from ..Transformer import Transformer
from ..config import LLVMLINK
import re


class TransformAr(Transformer):

    def canBeAppliedOn(cmd: str) -> bool:
        return cmd.startswith("ar cq ") and re.search("ar cq \w+.a", cmd)

    def applyTransformationOn(cmd: str, container) -> str:
        # tokenize and remove the original command with first option
        tokens = cmd.split()[1:]

        # llvm needs a flag for specifying the output file
        tokens[0] = "-o"

        # Add .bc file extension to static archive
        tokens[1] += ".bc"

        # register library to be direct linkable in later commands
        container.libs.add(tokens[1])

        # transform all linked .o-files to the corresponding .bc-file
        tokens = map(
            lambda x: x[:-2] + ".bc" if x.endswith(".o") else x, tokens)

        return LLVMLINK + " " + " ".join(tokens)