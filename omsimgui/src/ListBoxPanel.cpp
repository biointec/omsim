#include "ListBoxPanel.hpp"
#include <wx/textdlg.h>
#include "BasicPanel.hpp"


ListBoxPanel::ListBoxPanel(wxPanel * parent, wxListBox * lb, wxString const &Ext_, wxString const &ext_)
      : wxPanel(parent, wxID_ANY),
        Ext(Ext_),
        ext(ext_)
{
        wxBoxSizer *vbox = new wxBoxSizer(wxVERTICAL);
        m_lb = lb;
        m_newb = new wxButton(this, wxID_NEW, wxT("Add file"));
        m_deleteb = new wxButton(this, wxID_DELETE, wxT("Delete file"));
        m_clearb = new wxButton(this, wxID_CLEAR, wxT("Clear"));
        Connect(wxID_NEW, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(ListBoxPanel::OnNew) );
        Connect(wxID_CLEAR, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(ListBoxPanel::OnClear) );
        Connect(wxID_DELETE, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(ListBoxPanel::OnDelete) );
        
        
        
        vbox->Add(-1, 20);
        vbox->Add(m_newb);
        vbox->Add(m_deleteb);
        vbox->Add(m_clearb);
        vbox->Add(-1, 5);
        
        SetSizerAndFit(vbox);
}

void ListBoxPanel::OnNew(wxCommandEvent& event) 
{
        wxFileDialog* openDialog = new wxFileDialog(this,
                wxT("Choose a file to open"), wxEmptyString, wxEmptyString,
                wxT("" + Ext + " Files (*." + ext + ")|*." + ext), wxFD_MULTIPLE);
        if (openDialog->ShowModal() == wxID_CANCEL) {
                return;
        } else {
                m_lb->Append(openDialog->GetPath());
        }
        ((BasicPanel *) GetGrandParent())->addFasta(openDialog->GetPath());
}

void ListBoxPanel::OnClear(wxCommandEvent& event) 
{
        m_lb->Clear();
        ((BasicPanel *) GetGrandParent())->clearFasta();
}

void ListBoxPanel::OnDelete(wxCommandEvent& event) 
{
        int sel = m_lb->GetSelection();
        wxString fasta = m_lb->GetString(sel);
        if (sel != -1) {
                m_lb->Delete(sel);
        }
        ((BasicPanel *) GetGrandParent())->removeFasta(fasta);
}

