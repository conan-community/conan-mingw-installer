from conans import ConanFile, tools
from conans import __version__ as conan_version
from conans.model.version import Version
import os

class MingwInstallerConan(ConanFile):
    name = "mingw_installer"
    version = "1.0"
    license = "http://www.mingw.org/license"
    url = "http://github.com/lasote/conan-mingw-installer"

    if conan_version < Version("0.99"):
        os_name = "os"
        arch_name = "arch"
    else:
        os_name = "os_build"
        arch_name = "arch_build"

    settings = {os_name: ["Windows"],
                arch_name: ["x86", "x86_64"],
                "compiler": {"gcc": {"version": None,
                                     "libcxx": ["libstdc++", "libstdc++11"],
                                     "threads": ["posix", "win32"],
                                     "exception": ["dwarf2", "sjlj", "seh"]}}}

    # update the file listing the available MinGW versions
    options = {"update_list": [True, False] }
    default_options = "update_list=False"

    # we provide a list of MinGW
    exports_sources = [ 'repository.txt' ]

    # the link below is the online list of available MinGW
    # useful for ensuring this recipe provides the same versions available through the official mingw64-installer 
    repository_file = 'https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/installer/repository.txt/download'

    build_policy = "missing"
    description = 'MinGW, a contraction of "Minimalist GNU for Windows", ' \
                  'is a minimalist development environment for native Microsoft' \
                  ' Windows applications.'
    build_requires = "7z_installer/1.0@conan/stable"

    @property
    def arch(self):
        return self.settings.get_safe("arch_build") or self.settings.get_safe("arch")

    def update_repository(self):
        tools.download(self.repository_file, "repository.txt", overwrite=True)

    def build(self):

        if self.options.update_list:
            self.output.info("Updating MinGW List ... please wait.")
            self.update_repository()

        mingw_arch = 'x86_64' if self.arch == 'x86_64' else 'i686'

        mingw_list = MingwList()

        v = str(self.settings.compiler.version).split(".")
        if len(v) > 0:
            v_major = v[0]

        v_minor = v[1] if len(v) > 1 else "best"
        v_patch = v[2] if len(v) > 2 else "best"

        mingw_info, mingw_obj = mingw_list.get(mingw_arch, 
                                               str(self.settings.compiler.threads),
                                               str(self.settings.compiler.exception),
                                               v_major, v_minor, v_patch)
        self.output.info(mingw_info)
        self.output.info("Found MinGW: %s" % mingw_obj.print_obj())

        self.output.info("Downloading: %s" % mingw_obj.url)
        tools.download(mingw_obj.url, "file.7z")
        self.run("7z x file.7z")

    def package(self):
        self.copy("*", dst="", src="mingw32")
        self.copy("*", dst="", src="mingw64")

    def package_id(self):
        # option to update the list of mingw available does not affect package's id
        self.info.options.update_list = "any"

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
        self.env_info.MINGW_HOME = str(self.package_folder)
        self.env_info.CONAN_CMAKE_GENERATOR = "MinGW Makefiles"
        self.env_info.CXX = os.path.join(self.package_folder, "bin", "g++.exe")
        self.env_info.CC = os.path.join(self.package_folder, "bin", "gcc.exe")


class MinGW(object):

    config_data = {}

    def __init__(self, raw_data):
        mingw_version, mingw_arch, mingw_threads, mingw_exception, mingw_revision, mingw_url = [x.strip() for x in raw_data.split('|') ]

        self.config_data = {
            'version': mingw_version,
            'version_major': mingw_version.split(".")[0],
            'version_minor': mingw_version.split(".")[1],
            'version_patch': mingw_version.split(".")[2],
            'revision': mingw_revision.lstrip('rev'),
            'arch': mingw_arch,
            'threads': mingw_threads,
            'exception': mingw_exception,
            'url': mingw_url
        }

    def print_obj(self):
        return self.version + "-r" + self.revision + ", " + self.arch + ", " + self.threads + ", " + self.exception

    @property
    def version(self):
        return self.config_data['version']

    @property
    def version_major(self):
        return self.config_data['version_major']

    @property
    def version_minor(self):
        return self.config_data['version_minor']

    @property
    def version_patch(self):
        return self.config_data['version_patch']

    @property
    def revision(self):
        return self.config_data['revision']    

    @property
    def arch(self):
        return self.config_data['arch']

    @property
    def threads(self):
        return self.config_data['threads']

    @property
    def exception(self):
        return self.config_data['exception']

    @property
    def url(self):
        return self.config_data['url']

    def __gt__(self, other_mingw):
        return LooseVersion(self.version) > LooseVersion(other_mingw.version)

class MingwList(object):
    mingw = []

    def __init__(self, filename="repository.txt"):
        with open(filename) as f:
            for line in f.readlines():
                m = MinGW(line)
                self.mingw.append(m)


    def list_all(self):
        for i in self.mingw:
            print(i.print_obj())


    def find_version_minor(self, mingw_list, version_minor='best'):
        best = []
        best_value = "-1" if version_minor == 'best' else version_minor

        if version_minor == 'best':
            for i in mingw_list:
                if i.version_minor > best_value:
                    best_value = i.version_minor

        for i in mingw_list:
            if i.version_minor == best_value:
                best.append(i)

        return best


    def find_best_version_patch(self, mingw_list):
        best = []
        best_value = "-1"

        for i in mingw_list:
            if i.version_patch > best_value:
                best_value = i.version_patch

        for i in mingw_list:
            if i.version_patch == best_value:
                best.append(i)

        return best

    def find_best_revision(self, mingw_list):
        best = []
        best_value = "-1"

        for i in mingw_list:
            if i.revision > best_value:
                best_value = i.revision

        for i in mingw_list:
            if i.revision == best_value:
                best.append(i)

        return best

    def get(self, arch, threads, exception, version_major, version_minor='best', version_patch='best', revision='best'):
        msg = '\nSearching for: \n'
        msg += '                MinGW: '
        msg += version_major

        if version_minor != 'best':
            msg += '.'
            msg += version_minor
      
        if version_patch != 'best':
            msg += '.'
            msg += version_patch

        if revision != 'best':
            msg += '.'
            msg += revision

        msg += '\n         Architecture: ' + arch
        msg += '\n              Threads: ' + threads
        msg += '\n            Exception: ' + exception
        msg += '\n'

        #print(msg)

        # collect mingw configurations that are suitable
        candidates = []
        for i in self.mingw:
            if version_major == i.version_major and arch == i.arch and threads == i.threads and exception == i.exception:
                candidates.append(i)

        #print("-------------------------------------")
        #for i in candidates:
        #    print(i.print())

        candidates = self.find_version_minor(candidates, version_minor)

        # conan does not support controlling patch and custom mingw revision numbers.
        # we use the latest version of the compiler (i.e. 4.8 => 4.8.5-r2
        candidates = self.find_best_version_patch(candidates)
        candidates = self.find_best_revision(candidates)

        #print("-------------------------------------")
        #for i in candidates:
        #    print(i.print())
        #print("-------------------------------------")

        if len(candidates) > 1:
            raise ConanException("Unable to properly filter MingGW candidate releases. Please file a bug if you see this!!!")
        elif len(candidates) == 0:
            raise Exception("There is no suitable MinGW release for the requested features.")
        else:
            return msg, candidates[0]

    def has(self, version):
        v = self.normalize_version(version)
        print("Looking for version: " + v)

    def normalize_version(self, version):
        digit_list = version.split(".")
        while len(digit_list) < 3:
            digit_list.append('0')
        
        return '.'.join(digit_list)

