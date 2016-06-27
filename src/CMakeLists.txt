add_executable(omsimgui
BasicPanel.cpp
ConfigurationPanel.cpp
EnzymeDialog.cpp
EnzymePanel.cpp
ListBoxPanel.cpp
main.cpp
Notebook.cpp
tinyxml2.cpp
)
target_link_libraries(omsimgui ${wxWidgets_LIBRARIES})
target_link_libraries(omsimgui ${Boost_LIBRARIES})
