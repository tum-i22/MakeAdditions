from ..Transformer import Transformer
from ..config import CLANG


class TransformCCCompile(Transformer):

    def canBeAppliedOn(cmd: str) -> bool:
        return any(cmd.startswith(s) for s in ["cc", "gcc"]) and " -c " in cmd

    def applyTransformationOn(cmd: str, container) -> str:
        # tokenize and remove the original command
        tokens = cmd.split()[1:]

        # remove optimizer flags
        tokens = list(filter(lambda t: t not in [
            '-O0', '-O1', '-O2', '-O3', '-Og', '-Os', '-Ofast'], tokens))

        # deactivate optimization
        tokens.insert(0, "-O0")

        newcmd = CLANG + " -emit-llvm "
        if "-g" not in tokens:
            newcmd += "-g "

        if "-o" in tokens:
            pos = tokens.index("-o")
            if tokens[pos + 1].endswith(".o"):
                tokens[pos + 1] = tokens[pos + 1][:-2] + ".bc"

        return newcmd + " ".join(tokens)