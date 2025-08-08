from conan import ConanFile
from conan.tools.cmake import cmake_layout
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import copy
from os.path import join
from conan.tools.apple import fix_apple_shared_install_name

class libplistConan(ConanFile):
    name = "libplist"
    version = "2.6.0"
    package_type = "library"

    # Optional metadata
    license = "GNU GENERAL PUBLIC LICENSE"
    author = "Aaron Burghardt"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "A small portable C library to handle Apple Property List files in binary, XML, JSON, or OpenStep format."
    topics = ("ios", "apple", "open source")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}


    
    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):        
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):                    
        lib_path = "lib"
        bin_path = "bin"

        # self.cpp_info.set_property("cmake_file_name", "libplist")
        # self.cpp_info.set_property("cmake_target_name", "libplist::libplist")
        # self.cpp_info.set_property("cmake_find_mode", "both")
        # self.cpp_info.set_property("pkg_config_name", "libplist")        
        
        self.cpp_info.libdirs = [lib_path]
        self.cpp_info.bindirs = [bin_path]
       
        if self.settings.os=="Windows":
            self.cpp_info.libs = ["plist"]
            self.cpp_info.components["libplist"].libs = ["plist.lib"]
        elif self.settings.os in ["Macos", "Linux"]:    
            self.cpp_info.libs = ["libplist"]
            self.cpp_info.components["libplist"].libs = ["libplist.a"]


        fix_apple_shared_install_name(self)

