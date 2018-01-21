try:
    import StringIO
except ImportError:
    import io as StringIO
from conans import ConanFile, __version__ as conan_version
from conans.model.version import Version


class MinGWTestConan(ConanFile):
    
    generators = "gcc"
    if conan_version < Version("0.99"):
        os_name = "os"
        arch_name = "arch"
    else:
        os_name = "os_build"
        arch_name = "arch_build"

    settings = os_name, arch_name, "compiler"

    def build(self):
        self.run('gcc %s/main.cpp @conanbuildinfo.gcc -lstdc++ -o main' % self.source_folder)

    def test(self):
        self.run("main")
        output = StringIO.StringIO()
        self.run("gcc --version", output=output)
        assert(str(self.settings.compiler.version) in str(output.getvalue()))
