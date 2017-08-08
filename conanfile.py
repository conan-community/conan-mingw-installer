from conans import ConanFile, tools
import os


class MingwInstallerConan(ConanFile):
    name = "mingw_installer"
    version = "1.0"
    license = "http://www.mingw.org/license"
    url = "http://github.com/lasote/conan-mingw-installer"
    settings = {"os": ["Windows"],
                "arch": ["x86", "x86_64"],
                "compiler": {"gcc": {"version": None,
                                     "libcxx": ["libstdc++"],
                                     "threads": ["posix", "win32"],
                                     "exception": ["dwarf2", "sjlj", "seh"]}}}
    build_policy = "missing"
    description = 'MinGW, a contraction of "Minimalist GNU for Windows", ' \
                  'is a minimalist development environment for native Microsoft' \
                  ' Windows applications.'
    build_requires = "7z_installer/1.0@conan/stable"
    
    def configure(self):
        if (self.settings.arch == "x86" and self.settings.compiler.exception == "seh") or \
           (self.settings.arch == "x86_64" and self.settings.compiler.exception == "dwarf2"):
            raise Exception("Not valid %s and %s combination!" % (self.settings.arch, 
                                                                  self.settings.compiler.exception))       

    def build(self):
        keychain = "%s_%s_%s_%s" % (str(self.settings.compiler.version).replace(".", ""), 
                                    self.settings.arch,
                                    self.settings.compiler.exception,
                                    self.settings.compiler.threads)
        files = {"48_x86_dwarf2_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/4.8.2/threads-posix/dwarf/i686-4.8.2-release-posix-dwarf-rt_v3-rev0.7z",
                 "48_x86_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/4.8.2/threads-posix/sjlj/i686-4.8.2-release-posix-sjlj-rt_v3-rev0.7z",
                 "48_x86_64_seh_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.8.2/threads-posix/seh/x86_64-4.8.2-release-posix-seh-rt_v3-rev0.7z",
                 "48_x86_64_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.8.2/threads-posix/sjlj/x86_64-4.8.2-release-posix-sjlj-rt_v3-rev0.7z",
                 "48_x86_dwarf2_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/4.8.2/threads-win32/dwarf/i686-4.8.2-release-win32-dwarf-rt_v3-rev0.7z",
                 "48_x86_sjlj_win32": "https://github.com/tim-lebedkov/packages/releases/download/2016_Q2/i686-4.9.2-release-win32-sjlj-rt_v3-rev1.7z",
                 "48_x86_64_seh_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.8.2/threads-win32/seh/x86_64-4.8.2-release-win32-seh-rt_v3-rev0.7z",
                 "48_x86_64_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.8.2/threads-win32/sjlj/x86_64-4.8.2-release-win32-sjlj-rt_v3-rev0.7z",
                 "49_x86_dwarf2_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/4.9.2/threads-posix/dwarf/i686-4.9.2-release-posix-dwarf-rt_v3-rev1.7z",
                 "49_x86_sjlj_posix": "https://github.com/tim-lebedkov/packages/releases/download/2016_Q1/i686-4.9.2-release-posix-sjlj-rt_v3-rev0.7z",
                 "49_x86_64_seh_posix": "https://github.com/tim-lebedkov/packages/releases/download/2016_Q1/x86_64-4.9.2-release-posix-seh-rt_v3-rev1.7z",
                 "49_x86_64_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.9.2/threads-posix/sjlj/x86_64-4.9.2-release-posix-sjlj-rt_v3-rev1.7z",
                 "49_x86_dwarf2_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/4.9.2/threads-win32/dwarf/i686-4.9.2-release-win32-dwarf-rt_v3-rev1.7z",
                 "49_x86_sjlj_win32": "https://github.com/tim-lebedkov/packages/releases/download/2016_Q2/i686-4.9.2-release-win32-sjlj-rt_v3-rev1.7z",
                 "49_x86_64_seh_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.9.2/threads-win32/seh/x86_64-4.9.2-release-win32-seh-rt_v3-rev1.7z",
                 "49_x86_64_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.9.2/threads-win32/sjlj/x86_64-4.9.2-release-win32-sjlj-rt_v3-rev1.7z",

                 "62_x86_dwarf2_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.2.0/threads-win32/dwarf/i686-6.2.0-release-win32-dwarf-rt_v5-rev1.7z",
                 "62_x86_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.2.0/threads-win32/sjlj/i686-6.2.0-release-win32-sjlj-rt_v5-rev1.7z",
                 "62_x86_dwarf2_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.2.0/threads-posix/dwarf/i686-6.2.0-release-posix-dwarf-rt_v5-rev1.7z",
                 "62_x86_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.2.0/threads-posix/sjlj/i686-6.2.0-release-posix-sjlj-rt_v5-rev1.7z",

                 "62_x86_64_seh_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.2.0/threads-win32/seh/x86_64-6.2.0-release-win32-seh-rt_v5-rev1.7z",
                 "62_x86_64_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.2.0/threads-win32/sjlj/x86_64-6.2.0-release-win32-sjlj-rt_v5-rev1.7z",
                 "62_x86_64_seh_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.2.0/threads-posix/seh/x86_64-6.2.0-release-posix-seh-rt_v5-rev1.7z",
                 "62_x86_64_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.2.0/threads-posix/sjlj/x86_64-6.2.0-release-posix-sjlj-rt_v5-rev1.7z",
                                        
                 "54_x86_dwarf2_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/5.4.0/threads-win32/dwarf/i686-5.4.0-release-win32-dwarf-rt_v5-rev0.7z",
                 "54_x86_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/5.4.0/threads-win32/sjlj/i686-5.4.0-release-win32-sjlj-rt_v5-rev0.7z",
                 "54_x86_dwarf2_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/5.4.0/threads-posix/dwarf/i686-5.4.0-release-posix-dwarf-rt_v5-rev0.7z",
                 "54_x86_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/5.4.0/threads-posix/sjlj/i686-5.4.0-release-posix-sjlj-rt_v5-rev0.7z",

                 "54_x86_64_seh_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/5.4.0/threads-win32/seh/x86_64-5.4.0-release-win32-seh-rt_v5-rev0.7z",
                 "54_x86_64_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/5.4.0/threads-win32/sjlj/x86_64-5.4.0-release-win32-sjlj-rt_v5-rev0.7z",
                 "54_x86_64_seh_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/5.4.0/threads-posix/seh/x86_64-5.4.0-release-posix-seh-rt_v5-rev0.7z",
                 "54_x86_64_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/5.4.0/threads-posix/sjlj/x86_64-5.4.0-release-posix-sjlj-rt_v5-rev0.7z",
                 
                 "63_x86_dwarf2_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/6.3.0/threads-win32/dwarf/i686-6.3.0-release-win32-dwarf-rt_v5-rev1.7z",
                 "63_x86_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/6.3.0/threads-win32/sjlj/i686-6.3.0-release-win32-sjlj-rt_v5-rev1.7z",
                 "63_x86_dwarf2_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/6.3.0/threads-posix/dwarf/i686-6.3.0-release-posix-dwarf-rt_v5-rev1.7z",
                 "63_x86_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/6.3.0/threads-posix/sjlj/i686-6.3.0-release-posix-sjlj-rt_v5-rev1.7z",

                 "63_x86_64_seh_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.3.0/threads-win32/seh/x86_64-6.3.0-release-win32-seh-rt_v5-rev1.7z",
                 "63_x86_64_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.3.0/threads-win32/sjlj/x86_64-6.3.0-release-win32-sjlj-rt_v5-rev1.7z",
                 "63_x86_64_seh_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.3.0/threads-posix/seh/x86_64-6.3.0-release-posix-seh-rt_v5-rev1.7z",
                 "63_x86_64_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.3.0/threads-posix/sjlj/x86_64-6.3.0-release-posix-sjlj-rt_v5-rev1.7z",

                 "71_x86_dwarf2_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/7.1.0/threads-win32/dwarf/i686-7.1.0-release-win32-dwarf-rt_v5-rev1.7z",
                 "71_x86_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/7.1.0/threads-win32/sjlj/i686-7.1.0-release-win32-sjlj-rt_v5-rev1.7z",
                 "71_x86_dwarf2_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/7.1.0/threads-posix/dwarf/i686-7.1.0-release-posix-dwarf-rt_v5-rev1.7z",
                 "71_x86_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/7.1.0/threads-posix/sjlj/i686-7.1.0-release-posix-sjlj-rt_v5-rev1.7z",

                 "71_x86_64_seh_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/7.1.0/threads-win32/seh/x86_64-7.1.0-release-win32-seh-rt_v5-rev1.7z",
                 "71_x86_64_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/7.1.0/threads-win32/sjlj/x86_64-7.1.0-release-win32-sjlj-rt_v5-rev1.7z",
                 "71_x86_64_seh_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/7.1.0/threads-posix/seh/x86_64-7.1.0-release-posix-seh-rt_v5-rev1.7z",
                 "71_x86_64_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/7.1.0/threads-posix/sjlj/x86_64-7.1.0-release-posix-sjlj-rt_v5-rev1.7z",}

        tools.download(files[keychain], "file.7z")
        self.run("7z x file.7z")
    
    def package(self):
        self.copy("*", dst="", src="mingw32")
        self.copy("*", dst="", src="mingw64")

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
        self.env_info.CXX = os.path.join(self.package_folder, "bin", "g++.exe")
        self.env_info.CC = os.path.join(self.package_folder, "bin", "gcc.exe")
