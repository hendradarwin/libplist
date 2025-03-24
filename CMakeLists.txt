cmake_minimum_required(VERSION 3.17)
project(libplist)

list(APPEND CMAKE_CXX_SOURCE_FILE_EXTENSIONS c)

FILE(GLOB_RECURSE header_file_list ${PROJECT_SOURCE_DIR}/include/*.h)
FILE(GLOB_RECURSE c_file_list ${PROJECT_SOURCE_DIR}/src/*.c)
FILE(GLOB_RECURSE cpp_file_list ${PROJECT_SOURCE_DIR}/src/*.cpp)


# FILE(GLOB_RECURSE libcnary_header_file_list ${PROJECT_SOURCE_DIR}/libcnary/*.h)
FILE(GLOB_RECURSE libcnary_c_file_list ${PROJECT_SOURCE_DIR}/libcnary/*.c)

# unused file, will make compile error
list(REMOVE_ITEM libcnary_c_file_list ${CMAKE_CURRENT_SOURCE_DIR}/libcnary/cnary.c)


# C file contain c++ code, treat them as c++ code
set_source_files_properties(${c_file_list} PROPERTIES LANGUAGE CXX)
set_source_files_properties(${libcnary_c_file_list} PROPERTIES LANGUAGE CXX)


list(APPEND libimobiledevice_source_files    
    ${c_file_list}
    ${cpp_file_list}    
    ${libcnary_c_file_list}
)

add_library(plist SHARED ${libimobiledevice_source_files})

target_include_directories(plist
    PUBLIC         
        include        
        libcnary/include
        src  
        ${CMAKE_SOURCE_DIR}          
)

target_compile_definitions(plist PUBLIC 
    PACKAGE_VERSION="2.6.0"
)

target_link_libraries(plist PUBLIC ole32 ws2_32 gdi32)

set_target_properties(plist PROPERTIES 
    PUBLIC_HEADER "${header_file_list}"
)

install(
    TARGETS plist
    EXPORT plist_targets
    PUBLIC_HEADER DESTINATION "include/plist"
    RUNTIME DESTINATION "bin/x64/$<$<PLATFORM_ID:Windows>:windows>$<$<PLATFORM_ID:Linux>:linux>$<$<CONFIG:Debug,DebugASan,DebugTSan>:/debug>"
    ARCHIVE DESTINATION "lib/x64/$<$<PLATFORM_ID:Windows>:windows>$<$<PLATFORM_ID:Linux>:linux>$<$<CONFIG:Debug,DebugASan,DebugTSan>:/debug>"
    LIBRARY DESTINATION "lib/x64/$<$<PLATFORM_ID:Windows>:windows>$<$<PLATFORM_ID:Linux>:linux>$<$<CONFIG:Debug,DebugASan,DebugTSan>:/debug>"
)

