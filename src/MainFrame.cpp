#include "MainFrame.hpp"
#include "ListBoxPanel.hpp"
#include "EnzymePanel.hpp"
#include "ConfigurationPanel.hpp"

MainFrame::MainFrame(const wxString& title)
      : wxFrame(NULL, wxID_ANY, title, wxDefaultPosition, wxSize(700, 700))
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
        
        wxPanel * cPanel = new wxPanel(this, -1);
        wxBoxSizer *cclbbox = new wxBoxSizer(wxHORIZONTAL);
        configurationCheckListBox = new wxCheckListBox(cPanel, wxID_ConfigurationCheckListBox, wxPoint(-1, -1), wxSize(-1, -1)); 
        cclbbox->Add(configurationCheckListBox, 5, wxEXPAND | wxALL, 20);
        configurationPanel = new ConfigurationPanel(cPanel, configurationCheckListBox, configurations, enzymes);
        cclbbox->Add(configurationPanel, 1, wxEXPAND | wxRIGHT, 10);
        cPanel->SetSizer(cclbbox);
        cPanel->Center();
        
        Connect(wxID_ConfigurationCheckListBox, wxEVT_COMMAND_LISTBOX_DOUBLECLICKED, 
                wxCommandEventHandler(MainFrame::OnConfDblClick));
        
        configurationbox->Add(configurationTitle);
        configurationbox->Add(cPanel, 1, wxEXPAND);
        /*
        wxBoxSizer *xmlbox = new wxBoxSizer(wxVERTICAL);
        wxStaticText *xmlTitle = new wxStaticText(this, wxID_ANY, wxT("Configuration file"));
        
        wxPanel * xmlPanel = new wxPanel(this, -1);
        wxBoxSizer *xlbbox = new wxBoxSizer(wxHORIZONTAL);
        xmlListBox = new wxListBox(xmlPanel, ID_XMLListBox, wxPoint(-1, -1), wxSize(-1, -1)); 
        xlbbox->Add(xmlListBox, 5, wxEXPAND | wxALL, 20);
        ListBoxPanel *xmlBtnPanel = new ListBoxPanel(xmlPanel, xmlListBox, "XML", "xml");
        xlbbox->Add(xmlBtnPanel, 1, wxEXPAND | wxRIGHT, 10);
        xmlPanel->SetSizer(xlbbox);
        xmlPanel->Center();
        
        xmlbox->Add(xmlTitle);
        xmlbox->Add(xmlPanel, 1, wxEXPAND);
        */
        
        /*
                enzyme box
        */
        wxBoxSizer *enzymebox = new wxBoxSizer(wxVERTICAL);
        wxStaticText *enzymeTitle = new wxStaticText(this, wxID_ANY, wxT("Enzymes"));
        
        wxPanel * ePanel = new wxPanel(this, -1);
        wxBoxSizer *elbbox = new wxBoxSizer(wxHORIZONTAL);
        enzymeListBox = new wxListBox(ePanel, wxID_EnzymeCheckListBox, wxPoint(-1, -1), wxSize(-1, -1)); 
        elbbox->Add(enzymeListBox, 5, wxEXPAND | wxALL, 20);
        enzymePanel = new EnzymePanel(ePanel, enzymeListBox, configurations, enzymes);
        elbbox->Add(enzymePanel, 1, wxEXPAND | wxRIGHT, 10);
        ePanel->SetSizer(elbbox);
        ePanel->Center();
        
        Connect(wxID_EnzymeCheckListBox, wxEVT_COMMAND_LISTBOX_DOUBLECLICKED, 
                wxCommandEventHandler(MainFrame::OnEnzDblClick));
        
        enzymebox->Add(enzymeTitle);
        enzymebox->Add(ePanel, 1, wxEXPAND);
        
        
        mainbox->Add(configurationbox);
        mainbox->Add(enzymebox);
        
        SetSizer(mainbox);
        
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
        Close(true);
}

void MainFrame::update() {
        configurationPanel->update();
        enzymePanel->update();
}
