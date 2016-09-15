add_executable(omsimgui
AdvancedPanel.cpp
BasicPanel.cpp
EnzymeDialog.cpp
ListBoxPanel.cpp
main.cpp
MainFrame.cpp
Notebook.cpp
TagPanel.cpp
tinyxml2.cpp
)
target_link_libraries(omsimgui ${wxWidgets_LIBRARIES})
#target_link_libraries(omsimgui ${Boost_LIBRARIES})
