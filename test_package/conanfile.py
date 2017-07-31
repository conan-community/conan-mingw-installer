
import os
from conans import ConanFile


class MinGWTestConan(ConanFile):
    """ MinGW installer Conan package test """

    settings = "os", "arch", "compiler", "build_type"
    generators = "virtualenv", "gcc"

    def build(self):
        self.run('activate && gcc %s/main.cpp @conanbuildinfo.gcc -lstdc++ -o main' % self.conanfile_directory)

    def test(self):
        self.run("activate && main")