#include "main.hpp"
#include "MainFrame.hpp"

IMPLEMENT_APP(OMSim)

bool OMSim::OnInit()
{
        MainFrame *mainFrame = new MainFrame(wxT("OMSim: Optical Map Simulator"));
        mainFrame->Show(true);
        return true;
}
