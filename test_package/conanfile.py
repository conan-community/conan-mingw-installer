
import os
from conans import ConanFile


class MinGWTestConan(ConanFile):
    """ MinGW installer Conan package test """

    settings = "os", "arch", "compiler", "build_type"
    generators = "virtualenv", "gcc"

    def build(self):
        self.run('activate && gcc %s/main.cpp @conanbuildinfo.gcc -lstdc++ -o main' % self.conanfile_directory)
        
    def configure(self):
        self.options["mingw_installer"].version = self.settings.compiler.version
        self.options["mingw_installer"].arch = self.settings.arch

    def test(self):
        self.run("activate && main")