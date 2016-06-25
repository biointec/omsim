add_executable(omsimgui
main.cpp
Notebook.cpp
)
target_link_libraries(omsimgui ${wxWidgets_LIBRARIES})
target_link_libraries(omsimgui ${Boost_LIBRARIES})
