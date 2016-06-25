#include "main.hpp"
#include "Notebook.hpp"

IMPLEMENT_APP(MyApp)

bool MyApp::OnInit()
{
        Notebook *notebook = new Notebook(wxT("OMSim: Optical Map Simulator"));
        notebook->Show(true);
        return true;
}
