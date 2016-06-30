#include "MainFrame.hpp"
#include "ListBoxPanel.hpp"
#include "EnzymePanel.hpp"
#include "ConfigurationPanel.hpp"
#include "executablePath.hpp"
#include "main.hpp" //wxGetApp

bool run_sim = false;

MainFrame::MainFrame(const wxString& title)
      : wxFrame(NULL, wxID_ANY, title, wxDefaultPosition, wxDefaultSize)
{
        wxMenuBar *menubar = new wxMenuBar;
        wxMenu *file = new wxMenu;
        file->Append(wxID_EXIT, wxT("Quit"), wxT(""));
        menubar->Append(file, wxT("&File"));
        SetMenuBar(menubar);
        Connect(wxEVT_COMMAND_MENU_SELECTED, 
                wxCommandEventHandler(MainFrame::OnQuit)); 
        
        wxBoxSizer *mainbox = new wxBoxSizer(wxVERTICAL);
        
        /*
                xml box
        */
        wxBoxSizer *configurationbox = new wxBoxSizer(wxVERTICAL);
        wxStaticText *configurationTitle = new wxStaticText(this, wxID_ANY, wxT("Configurations"));
        
        wxBoxSizer *cclbbox = new wxBoxSizer(wxHORIZONTAL);
        configurationCheckListBox = new wxCheckListBox(this, wxID_ConfigurationCheckListBox, wxPoint(-1, -1), wxSize(-1, -1)); 
        cclbbox->Add(configurationCheckListBox, 5, wxEXPAND | wxALL, 20);
        configurationPanel = new ConfigurationPanel(this, configurationCheckListBox, configurations, enzymes);
        cclbbox->Add(configurationPanel, 1, wxRIGHT, 10);
        
        Connect(wxID_ConfigurationCheckListBox, wxEVT_COMMAND_LISTBOX_DOUBLECLICKED, 
                wxCommandEventHandler(MainFrame::OnConfDblClick));
        
        configurationbox->Add(configurationTitle);
        configurationbox->Add(cclbbox, 1, wxEXPAND);
        
        /*
                enzyme box
        */
        wxBoxSizer *enzymebox = new wxBoxSizer(wxVERTICAL);
        wxStaticText *enzymeTitle = new wxStaticText(this, wxID_ANY, wxT("Enzymes"));
        
        wxBoxSizer *elbbox = new wxBoxSizer(wxHORIZONTAL);
        enzymeListBox = new wxListBox(this, wxID_EnzymeCheckListBox, wxPoint(-1, -1), wxSize(-1, -1)); 
        elbbox->Add(enzymeListBox, 5, wxEXPAND | wxALL, 20);
        enzymePanel = new EnzymePanel(this, enzymeListBox, configurations, enzymes);
        elbbox->Add(enzymePanel, 1, wxRIGHT, 10);
        
        Connect(wxID_EnzymeCheckListBox, wxEVT_COMMAND_LISTBOX_DOUBLECLICKED, 
                wxCommandEventHandler(MainFrame::OnEnzDblClick));
        
        enzymebox->Add(enzymeTitle);
        enzymebox->Add(elbbox, 1, wxEXPAND);
        
        /*
                run box
        */
        wxBoxSizer *runbox = new wxBoxSizer(wxVERTICAL);
        wxStaticText *runTitle = new wxStaticText(this, wxID_ANY, wxT("Simulation"));
        wxButton *runButton = new wxButton(this, wxID_RunButton, _T("Save and run simulation"), wxPoint(0, 0), wxDefaultSize, 0);
        runbox->Add(runTitle);
        runbox->Add(runButton, 1, wxALL, 10);
        
        Connect(wxID_RunButton, wxEVT_BUTTON, 
                wxCommandEventHandler(MainFrame::OnRunOmsim));
        
        mainbox->Add(configurationbox, 1, wxEXPAND | wxALL, 10);
        mainbox->Add(enzymebox, 1, wxEXPAND | wxALL, 10);
        mainbox->Add(runbox, 0, wxEXPAND | wxALL, 10);
        
        SetSizerAndFit(mainbox);
        
        CreateStatusBar();
        Center();
}


void MainFrame::OnConfDblClick(wxCommandEvent& event)
{
        configurationPanel->OnConfDblClick(event);
}

void MainFrame::OnEnzDblClick(wxCommandEvent& event)
{
        enzymePanel->OnEnzDblClick(event);
}

void MainFrame::OnQuit(wxCommandEvent& event) 
{
        simulator_thread.join();
        Close(true);
}

void MainFrame::OnRunOmsim(wxCommandEvent& event) {
        if(!run_sim) {
                wxFileDialog saveDialog(this,
                        _("Save XML file"), wxEmptyString, wxEmptyString,
                        _("XML files (*.xml)|*.xml"), wxFD_SAVE|wxFD_OVERWRITE_PROMPT);
                if (saveDialog.ShowModal() == wxID_CANCEL) {
                        return;
                } else {
                        configurationPanel->updateXML();
                        configurationPanel->doc->SaveFile(saveDialog.GetPath());
                }

                if (simulator_thread.joinable()) {
                        simulator_thread.join();
                }
                run_sim = true;
                wxPuts("Start new thread.");
                const char *argv0 = wxGetApp().argv[0];
                wxString path = executable_path(argv0);
                path = path.substr(0, path.size() - 8) + wxString("omsim/__main__ ") + saveDialog.GetPath();
                simulator_thread = std::thread{ [path](){
                        std::system(path);
                        run_sim = false;
                }};
        }
}


void MainFrame::update() {
        configurationPanel->update();
        enzymePanel->update();
}
