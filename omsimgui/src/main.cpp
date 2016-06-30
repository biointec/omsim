#include "main.hpp"
#include "MainFrame.hpp"

IMPLEMENT_APP(OMSim)

bool OMSim::OnInit()
{
//        Notebook *notebook = new Notebook(wxT("OMSim: Optical Map Simulator"));
//        notebook->Show(true);
        MainFrame *mainFrame = new MainFrame(wxT("OMSim: Optical Map Simulator"));
        mainFrame->Show(true);
        return true;
}
