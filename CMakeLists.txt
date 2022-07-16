cmake_minimum_required(VERSION 3.18.0)
project(eiger)

#set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_BUILD_TYPE Release)

set(CMAKE_CXX_STANDARD 20)

set(CMAKE_CXX_FLAGS "-O3")

find_package(Eigen3 3.3 REQUIRED NO_MODULE)

add_subdirectory(3rd_party/cpp_script)

macro(add_problem problem_name)
    add_custom_command(
        OUTPUT ${CMAKE_SOURCE_DIR}/genCpp/${problem_name}.cpp ${CMAKE_SOURCE_DIR}/genCpp/${problem_name}.hpp
        COMMAND ./gen_code.sh ${problem_name}
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        MAIN_DEPENDENCY ${CMAKE_SOURCE_DIR}/Maxima/${problem_name}.mac
    )
    add_library(${problem_name} SHARED
        src/${problem_name}.cpp
        genCpp/${problem_name}.cpp
    )
    target_compile_options(${problem_name}
        PRIVATE -Wno-return-type-c-linkage
        PRIVATE -Wno-return-type
    )
    target_link_libraries(${problem_name}
        PRIVATE Eigen3::Eigen
        PRIVATE cs
    )
    target_include_directories(${problem_name}
        PRIVATE genCpp
    )
endmacro()

add_problem(brachistochrone)

add_problem(min_triangle_circ)
