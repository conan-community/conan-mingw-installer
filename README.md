[![Build status](https://ci.appveyor.com/api/projects/status/48oc6nv4ju4b9gjb/branch/master?svg=true)](https://ci.appveyor.com/project/lasote/conan-mingw-installer-p6wrh/branch/master)

# conan-mingw-installer

[Bintray conan-center](https://bintray.com/conan/conan-center?filterByPkgName=mingw_installer%3Aconan) package for installing MinGW.

## Reference

**mingw_installer/1.0@conan/stable**


## Use as a build require

  This package is useful as a conan **build_require**, you can use it to build other packages using the MinGW packages.
  This package will automatically configure your PATH, CC and CXX environment variables to point to the package MinGW compiler.
  Check: [http://docs.conan.io/en/latest/mastering/build_requires.html](http://docs.conan.io/en/latest/mastering/build_requires.html)
  
  

  