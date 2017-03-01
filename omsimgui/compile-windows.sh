compiler=i686-w64-mingw32-g++
cxxflags="-Wno-deprecated -Wall -std=c++11 -static-libstdc++ -static-libgcc"
wxcxxflags=$(/usr/i686-w64-mingw32/bin/wx-config --cxxflags)
libs=$(/usr/i686-w64-mingw32/bin/wx-config --libs)

mkdir windows
cd windows
${compiler} -c -o AdvancedPanel.o ../src/AdvancedPanel.cpp ${wxcxxflags} ${cxxflags}
${compiler} -c -o BasicPanel.o ../src/BasicPanel.cpp ${wxcxxflags} ${cxxflags}
${compiler} -c -o EnzymeDialog.o ../src/EnzymeDialog.cpp ${wxcxxflags} ${cxxflags}
${compiler} -c -o ListBoxPanel.o ../src/ListBoxPanel.cpp ${wxcxxflags} ${cxxflags}
${compiler} -c -o main.o ../src/main.cpp ${wxcxxflags} ${cxxflags}
${compiler} -c -o MainFrame.o ../src/MainFrame.cpp ${wxcxxflags} ${cxxflags}
${compiler} -c -o Notebook.o ../src/Notebook.cpp ${wxcxxflags} ${cxxflags}
${compiler} -c -o TagPanel.o ../src/TagPanel.cpp ${wxcxxflags} ${cxxflags}
${compiler} -c -o tinyxml2.o ../src/tinyxml2.cpp  ${wxcxxflags} ${cxxflags}

${compiler} -o omsimgui-windows-64.exe *.o ${libs} ${cxxflags}

cp omsimgui-windows-64.exe ../../bin/
