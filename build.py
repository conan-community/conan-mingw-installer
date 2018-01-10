from conan.packager import ConanMultiPackager
import copy


if __name__ == "__main__":
    builder = ConanMultiPackager()
    base = {"os": "Windows", "compiler": "gcc", "compiler.version": "7.1",
            "compiler.exception": "seh", "compiler.libcxx": "libstdc++",
            "compiler.threads": "posix"}
    for version in ["4.9", "5.4", "6.4", "7.2"]:
        tmp = copy.copy(base)
        tmp["compiler.version"] = version
        for th in ["posix", "win32"]:
            tmp2 = copy.copy(tmp)
            tmp2["compiler.threads"] = th
            for ex in ["seh", "sjlj"]:
                tmp3 = copy.copy(tmp2)
                tmp3["compiler.exception"] = ex
                builder.add(tmp3, {}, {}, {})
    
    builder.run()
