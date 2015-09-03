set (CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
include_directories( ${PROJECT_SOURCE_DIR}/include/topics )
add_executable( test_topics test_topics )
target_link_libraries( test_topics topics textio smh m)
