#include "EnzymePanel.hpp"
#include <wx/textdlg.h>


EnzymePanel::EnzymePanel(wxPanel * parent, wxCheckListBox * clb)
      : wxPanel(parent, wxID_ANY)
{
        doc = new tinyxml2::XMLDocument();
        wxBoxSizer *vbox = new wxBoxSizer(wxVERTICAL);
        m_clb = clb;
        m_importb = new wxButton(this, wxID_IMPORT, wxT("Import file"));
        m_exportb = new wxButton(this, wxID_EXPORT, wxT("Export file"));
        m_newb = new wxButton(this, wxID_NEW, wxT("Add enzyme"));
        m_deleteb = new wxButton(this, wxID_DELETE, wxT("Delete file"));
        m_clearb = new wxButton(this, wxID_CLEAR, wxT("Clear"));
        Connect(wxID_IMPORT, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(EnzymePanel::OnImport));
        Connect(wxID_EXPORT, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(EnzymePanel::OnExport));
        Connect(wxID_NEW, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(EnzymePanel::OnNew));
        Connect(wxID_CLEAR, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(EnzymePanel::OnClear));
        Connect(wxID_DELETE, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(EnzymePanel::OnDelete));
        
        vbox->Add(-1, 20);
        vbox->Add(m_importb);
        vbox->Add(m_exportb);
        vbox->Add(m_newb);
        vbox->Add(m_deleteb);
        vbox->Add(m_clearb);
        vbox->Add(-1, 5);
        
        SetSizer(vbox);
}

void EnzymePanel::parseXML() {
        enzymes.clear();
        m_clb->Clear();
        auto child = doc->FirstChildElement("enzymes")->FirstChildElement("enzyme");
        count = 0;
        while (child != NULL) {
                count += 1;
                wxString id = child->FirstChildElement("id")->GetText();
                wxString pattern = child->FirstChildElement("pattern")->GetText();
                wxString label = "label_" + (count - 1);
                wxString fn = child->FirstChildElement("fn")->GetText();
                wxString fp = child->FirstChildElement("fp")->GetText();
                enzymes[id] = enzyme(id, pattern, label, fn, fp);
                m_clb->Append(id);
                child = child->NextSiblingElement("enzyme");
        }
}

void EnzymePanel::OnImport(wxCommandEvent& event) 
{
        wxFileDialog openDialog(this,
                _("Choose a file to open"), wxEmptyString, wxEmptyString,
                _("XML Files (*.xml)|*.xml"), wxFD_MULTIPLE);
        if (openDialog.ShowModal() == wxID_CANCEL) {
                return;
        } else {
                doc->LoadFile(openDialog.GetPath());
                parseXML();
        }
}

void EnzymePanel::OnExport(wxCommandEvent& event) 
{
        wxFileDialog saveDialog(this,
                _("Save XML file"), wxEmptyString, wxEmptyString,
                _("XML files (*.xml)|*.xml"), wxFD_SAVE|wxFD_OVERWRITE_PROMPT);
        if (saveDialog.ShowModal() == wxID_CANCEL) {
                return;
        } else {
                doc->SaveFile(saveDialog.GetPath());
        }
}

void EnzymePanel::OnNew(wxCommandEvent& event) 
{
        EnzymeDialog dlg(this, wxID_ANY, _("Add enzyme"));
        if (dlg.ShowModal() == wxID_OK) {
                
        }
        //wxString str = wxGetTextFromUser(wxT("Add new item"));
        //if (str.Len() > 0) {
        //        m_clb->Append(str);
        //}
}

void EnzymePanel::OnClear(wxCommandEvent& event) 
{
        m_clb->Clear();
}

void EnzymePanel::OnDelete(wxCommandEvent& event) 
{
        int sel = m_clb->GetSelection();
        if (sel != -1) {
                m_clb->Delete(sel);
        }
}

