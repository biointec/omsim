#include "Notebook.h"
#include "BasicPanel.h"
#include "AdvancedPanel.h"

Notebook::Notebook(const wxString& title)
      : wxFrame(NULL, wxID_ANY, title, wxDefaultPosition, wxSize(400, 350))
{
        wxNotebook *nb = new wxNotebook(this, -1, wxPoint(-1, -1), 
                wxSize(-1, -1), wxNB_TOP);
        wxMenuBar *menubar = new wxMenuBar;
        wxMenu *file = new wxMenu;
        file->Append(wxID_EXIT, wxT("Quit"), wxT(""));
        menubar->Append(file, wxT("&File"));
        SetMenuBar(menubar);
        Connect(wxEVT_COMMAND_MENU_SELECTED, 
                wxCommandEventHandler(Notebook::OnQuit)); 
        
        BasicPanel *bpanel = new BasicPanel(nb, -1);
        nb->AddPage(bpanel, wxT("Basic"));
        
        AdvancedPanel *apanel = new AdvancedPanel(nb, -1);
        nb->AddPage(apanel, wxT("Advanced"));
        
        CreateStatusBar();
        Center();
}

void Notebook::OnQuit(wxCommandEvent& event) 
{
        Close(true);
}
