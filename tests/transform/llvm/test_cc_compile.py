from ..TransformationTestCase import TransformationTestCase
from makeadditions.config import CLANG


class TestTransformLlvmCCCompile(TransformationTestCase):

    def test_cc_compile_basic(self):
        self.assertTransformation(
            CLANG + " -emit-llvm -g -O0 -c -o main.bc main.c",
            "cc    -c -o main.bc main.c"
        )

    def test_cc_compile_bzip2(self):
        self.assertTransformation(
            CLANG + " -emit-llvm -O0 -Wall -Winline -g "
            "-D_FILE_OFFSET_BITS=64 -c blocksort.c",
            "gcc -Wall -Winline -O2 -g -D_FILE_OFFSET_BITS=64 -c blocksort.c"
        )

    def test_cc_compile_with_userconfig_basic(self):
        self.assertTransformation(
            CLANG + " -emit-llvm -g -O0 -c -o main.bc main.c",
            CLANG + "    -c -o main.bc main.c"
        )

    def test_cc_compile_flags_flex(self):
        self.assertTransformation(
            CLANG + " -emit-llvm -O0 -DHAVE_CONFIG_H -I. -I../src -g " +
            "-c lib.c -fPIC -DPIC -o .libs/lib.bc",
            CLANG + " -DHAVE_CONFIG_H -I. -I../src -g " +
            "-O2  -MT lib.lo -MD -MP -MF .deps/lib.Tpo -c lib.c " +
            "-fPIC -DPIC -o .libs/lib.o"
        )

    def test_cc_compile_localdir_flex(self):
        self.assertTransformation(
            CLANG + " -emit-llvm -O0 -DHAVE_CONFIG_H -I. " +
            "'-DLOCALEDIR=" + '"' + "/usr/local/share/locale" + '"' + "'" +
            "-I../intl -g -c libmain.c -fPIC -DPIC -o .libs/libmain.bc",
            CLANG + " -DHAVE_CONFIG_H -I. " +
            "'-DLOCALEDIR=" + '"' + "/usr/local/share/locale" + '"' + "'" +
            "-I../intl -g -O2 -MT libmain.lo -MD -MP -MF " +
            ".deps/libmain.Tpo -c libmain.c -fPIC -DPIC " +
            "-o .libs/libmain.o"
        )
