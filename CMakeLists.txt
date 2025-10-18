cmake_minimum_required(VERSION 3.16)
project(IntoTheDark VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Qt6 components
find_package(Qt6 REQUIRED COMPONENTS Core Widgets)

# Set Qt6 to use CMake's find_package
set(QT_NO_CREATE_TARGETS ON)

# Add executable
add_executable(IntoTheDark
    src/main.cpp
)

# Link Qt6 libraries
target_link_libraries(IntoTheDark
    Qt6::Core
    Qt6::Widgets
)

# Set target properties
set_target_properties(IntoTheDark PROPERTIES
    WIN32_EXECUTABLE TRUE
    MACOSX_BUNDLE TRUE
)

# Copy assets to build directory
file(COPY assets DESTINATION ${CMAKE_BINARY_DIR})
file(COPY python_backend DESTINATION ${CMAKE_BINARY_DIR})
file(COPY save DESTINATION ${CMAKE_BINARY_DIR})

# Create save directory if it doesn't exist
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/save)

# Install targets
install(TARGETS IntoTheDark
    BUNDLE DESTINATION .
    RUNTIME DESTINATION bin
)

# Install assets
install(DIRECTORY assets DESTINATION .)
install(DIRECTORY python_backend DESTINATION .)
install(DIRECTORY save DESTINATION .)

# Print configuration info
message(STATUS "Into the Dark - Game Configuration")
message(STATUS "Qt6 version: ${Qt6_VERSION}")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "Install prefix: ${CMAKE_INSTALL_PREFIX}")
