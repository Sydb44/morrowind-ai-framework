# AI Client component for OpenMW

set(AI_CLIENT
    client.cpp
    client.hpp
)

openmw_add_library(${OPENMW_TARGET_AI_CLIENT} SHARED ${AI_CLIENT})

# Find Boost with required components
find_package(Boost REQUIRED COMPONENTS system thread filesystem)

# Find nlohmann_json
find_package(nlohmann_json QUIET)
if(NOT nlohmann_json_FOUND)
    include(FetchContent)
    FetchContent_Declare(
        nlohmann_json
        URL https://github.com/nlohmann/json/releases/download/v3.11.2/json.tar.xz
    )
    FetchContent_MakeAvailable(nlohmann_json)
endif()

# Add include directories
target_include_directories(${OPENMW_TARGET_AI_CLIENT}
    PRIVATE
    ${OPENMW_SOURCE_DIR}/apps/openmw
    ${OPENMW_SOURCE_DIR}/components
    ${Boost_INCLUDE_DIRS}
)

# Link libraries
target_link_libraries(${OPENMW_TARGET_AI_CLIENT}
    ${Boost_SYSTEM_LIBRARY}
    ${Boost_FILESYSTEM_LIBRARY}
    ${Boost_THREAD_LIBRARY}
    ${CMAKE_THREAD_LIBS_INIT}
    nlohmann_json::nlohmann_json
)

# Add compile definitions
target_compile_definitions(${OPENMW_TARGET_AI_CLIENT}
    PRIVATE
    OPENMW_AI_CLIENT_EXPORT
)

if(WIN32)
    target_compile_definitions(${OPENMW_TARGET_AI_CLIENT}
        PRIVATE
        _WIN32_WINNT=0x0601 # Windows 7 or later
    )
endif()

# Install
if(WIN32)
    install(TARGETS ${OPENMW_TARGET_AI_CLIENT} RUNTIME DESTINATION ".")
else()
    install(TARGETS ${OPENMW_TARGET_AI_CLIENT} LIBRARY DESTINATION "${OPENMW_LIBRARY_DIR}")
endif()
