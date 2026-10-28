cmake_minimum_required(VERSION 3.14)
project(imbss VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -stdlib=libc++")

include(FetchContent)

# set(CMAKE_VERBOSE_MAKEFILE 1)
# set(APP_VERSION_MAJOR 1)
# set(APP_VERSION_MINOR 0)

FetchContent_Declare(
    imgui
    URL https://github.com/ocornut/imgui/archive/refs/tags/v1.93.0.tar.gz
    # GIT_REPOSITORY https://github.com/ocornut/imgui/archive/refs/tags/v1.93.0.tar.gz
    # GIT_TAG        docking # Используйте 'master' или конкретный тег, например 'v1.91.5'
)


FetchContent_MakeAvailable(imgui)

add_library(imgui_lib STATIC)
set(IMGUI_DIR ${imgui_SOURCE_DIR})

target_sources(imgui_lib PRIVATE
    ${IMGUI_DIR}/imgui.cpp
    ${IMGUI_DIR}/imgui_demo.cpp
    ${IMGUI_DIR}/imgui_draw.cpp
    ${IMGUI_DIR}/imgui_tables.cpp
    ${IMGUI_DIR}/imgui_widgets.cpp
)

target_sources(imgui_lib PRIVATE
    ${IMGUI_DIR}/backends/imgui_impl_glfw.cpp
    ${IMGUI_DIR}/backends/imgui_impl_opengl3.cpp
)

target_include_directories(imgui_lib PUBLIC 
    ${IMGUI_DIR}
    ${IMGUI_DIR}/backends
)

#===========

set(APP_TARGET imbss)

# Указываем CMake сгенерировать реальный version.h из шаблона
# configure_file(
#     "${CMAKE_CURRENT_SOURCE_DIR}/src/version.hpp.in"
#     "${CMAKE_CURRENT_BINARY_DIR}/version.hpp"
# )


# NOTE: for
# including(https://stackoverflow.com/questions/61206703/is-there-includepath-option-in-clangd)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(SOURCES
    src/main.cpp
    src/application/application.cpp

    # calendar
    src/calendar/calendar.cpp
    src/calendar/core.cpp
    
    # bss
    src/bss/bss.cpp
    
    # UI
    src/ui/main_window/imgui_factory.cpp
    src/ui/main_window/main_window.cpp
    src/ui/utils/utils.cpp
    src/ui/about/about.cpp
    src/ui/files_navigator/files_navigator.cpp
    # src/ui/main_menu.cpp
)

# set(IMGUI_SOURCES
#     vendors/imgui/imgui.cpp 
#     # vendors/imgui/imgui_demo.cpp
#     vendors/imgui/imgui_draw.cpp 
#     vendors/imgui/imgui_widgets.cpp
#     vendors/imgui/imgui_tables.cpp)

# set(BACKEND_SOURCES vendors/imgui/backends/imgui_impl_glfw.cpp
#                     vendors/imgui/backends/imgui_impl_opengl3.cpp)

# add_library(backend STATIC ${BACKEND_SOURCES})

# add_library(imgui STATIC ${IMGUI_SOURCES})

# add_subdirectory(vendors/argparse)

# argparse ============================================
FetchContent_Declare(
    argparse
    GIT_REPOSITORY https://github.com/p-ranav/argparse.git
)
FetchContent_MakeAvailable(argparse)
# argparse ============================================




include_directories(${PROJECT_SOURCE_DIR})
# include_directories(vendors/imgui)
# include_directories(vendors/argparse/include)

add_executable(${APP_TARGET} ${SOURCES})
# target_link_libraries(${APP_TARGET} imgui backend)

# можно и так... add_executable(${APP_TARGET} ${SOURCES} ${IMGUI_SOURCES}
# ${BACKEND_SOURCES})
target_include_directories(${APP_TARGET} PRIVATE src)
# target_include_directories(${APP_TARGET} PRIVATE vendors/imgui) # Include the
# target_include_directories(${APP_TARGET} PRIVATE vendors/imgui/backends)

# Не забываем добавить путь к сгенерированному файлу в include
# target_include_directories(${APP_TARGET} PRIVATE "${CMAKE_CURRENT_BINARY_DIR}")

# Подключение зависимостей окна/графики (GLFW и OpenGL должны быть настроены в вашей системе)
find_package(glfw3 REQUIRED)
find_package(OpenGL REQUIRED)

# zlib
find_package(ZLIB REQUIRED)


# glfw
# find_package(glfw3 REQUIRED)
# include_directories(${GLFW_INCLUDE_DIRS})
# link_libraries(${GLFW_LIBRARY_DIRS})

# opengl
# find_package(OpenGL REQUIRED)
# include_directories(${OPENGL_INCLUDE_DIRS})

# glew find_package(GLEW REQUIRED) include_directories(${GLEW_INCLUDE_DIRS})

target_link_libraries(${APP_TARGET} PRIVATE
    imgui_lib
    glfw
    OpenGL::GL
    ZLIB::ZLIB
    argparse
)
# target_link_libraries(${APP_TARGET} PRIVATE
#   imgui_lib
#   glfw
#     OpenGL::GL
# #   ${OPENGL_LIBRARIES}
#   # ${GLEW_LIBRARIES}
# #   ${EXTRA_LIBS}
#   # for error undefined reference to symbol 'dlclose@@GLIBC_2.2.5'
#   ${CMAKE_DL_LIBS})



# Указываем стандартную подпапку bin. 
# Итоговый путь будет: CMAKE_INSTALL_PREFIX + DESTINATION
# install(TARGETS ${APP_TARGET}
#     RUNTIME DESTINATION bin
# )