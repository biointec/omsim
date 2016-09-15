#include "MainFrame.hpp"
#include "Notebook.hpp"
#include "BasicPanel.hpp"
#include "AdvancedPanel.hpp"
#include "main.hpp" //wxGetApp
#include <wx/msgdlg.h>
#include <iostream>

MainFrame::MainFrame(const wxString& title)
      : wxFrame(NULL, wxID_ANY, title, wxDefaultPosition, wxDefaultSize)
{
        wxMenuBar *menubar = new wxMenuBar;
        wxMenu *file = new wxMenu;
        file->Append(wxID_CNEW, wxT("New"), wxString());
        file->Append(wxID_COPEN, wxT("Open"), wxString());
        file->Append(wxID_CSAVE, wxT("Save"), wxString());
        file->Append(wxID_CCOPY, wxT("Save a copy"), wxString());
        file->Append(wxID_EXIT, wxT("Quit"), wxString());
        menubar->Append(file, wxT("&File"));
        SetMenuBar(menubar);
        
        Connect(wxID_CNEW, wxEVT_COMMAND_MENU_SELECTED,
                wxCommandEventHandler(MainFrame::OnNew));
        Connect(wxID_COPEN, wxEVT_COMMAND_MENU_SELECTED,
                wxCommandEventHandler(MainFrame::OnOpen));
        Connect(wxID_CSAVE, wxEVT_COMMAND_MENU_SELECTED,
                wxCommandEventHandler(MainFrame::OnSave));
        Connect(wxID_CCOPY, wxEVT_COMMAND_MENU_SELECTED,
                wxCommandEventHandler(MainFrame::OnCopy));
        Connect(wxID_EXIT, wxEVT_COMMAND_MENU_SELECTED,
                wxCommandEventHandler(MainFrame::OnQuit));

        wxBoxSizer *mainbox = new wxBoxSizer(wxVERTICAL);
        wxNotebook *nb = new wxNotebook(this, -1, wxPoint(-1, -1), 
                wxSize(-1, -1), wxNB_TOP);
        bpanel = new BasicPanel(nb, -1, c, enzymes);
        nb->AddPage(bpanel, wxT("Basic"));
        apanel = new AdvancedPanel(nb, -1, c);
        nb->AddPage(apanel, wxT("Advanced"));
        mainbox->Add(nb, 1, wxEXPAND | wxALL, 10);
        SetSizerAndFit(mainbox);
        CreateStatusBar();
        Center();
}

void MainFrame::update() {
        bpanel->update();
        apanel->update();
}

void MainFrame::OnNew(wxCommandEvent& event) 
{
        wxMessageDialog dlg(this, wxT("Creating a new configuration will delete any unsaved changes!"), wxMessageBoxCaptionStr, wxOK|wxCANCEL|wxCENTRE);
        if (dlg.ShowModal() == wxID_CANCEL) {
                return;
        } else {
                c.new_config();
        }
        update();
}

void MainFrame::OnOpen(wxCommandEvent& event) 
{
        wxMessageDialog dlg(this, wxT("Opening a new file will delete any unsaved changes!"), wxT(""), wxOK|wxCANCEL|wxCENTRE);
        if (dlg.ShowModal() == wxID_CANCEL) {
                return;
        } else {
                wxFileDialog openDialog(this, wxT("Choose a file to open"),
                        wxEmptyString, wxEmptyString,
                        wxT("XML Files (*.xml)|*.xml"), wxFD_MULTIPLE);
                if (openDialog.ShowModal() == wxID_CANCEL) {
                        return;
                } else {
                        c.open_config(openDialog.GetPath());
                }
        }
        update();
}

void MainFrame::OnSave(wxCommandEvent& event) 
{
        if (c.xml == "") {
                OnCopy(event);
        } else {
                c.save();
        }
}

void MainFrame::OnCopy(wxCommandEvent& event) 
{
        wxFileDialog saveDialog(this,
                wxT("Save XML file"), wxEmptyString, wxEmptyString,
                wxT("XML files (*.xml)|*.xml"), wxFD_SAVE|wxFD_OVERWRITE_PROMPT);
        if (saveDialog.ShowModal() == wxID_CANCEL) {
                return;
        } else {
                c.save_as(saveDialog.GetPath());
        }
}

void MainFrame::OnQuit(wxCommandEvent& event) 
{
        Close(true);
}
