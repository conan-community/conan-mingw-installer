import os
import StringIO
from conans import ConanFile

class MinGWTestConan(ConanFile):
    
    generators = "gcc"
    settings = {"os", "arch", "compiler"}

    def build(self):
        self.run('gcc %s/main.cpp @conanbuildinfo.gcc -lstdc++ -o main' % self.conanfile_directory)

    def test(self):
        self.run("main")
        output = StringIO.StringIO()
        self.run("gcc --version", output=output)
        assert(str(self.settings.compiler.version) in str(output.getvalue()))