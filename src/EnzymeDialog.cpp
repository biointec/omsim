#include "EnzymeDialog.hpp"

#include <wx/stattext.h>
#include <wx/sizer.h>

EnzymeDialog::EnzymeDialog(wxWindow *parent, wxWindowID id, const wxString &title, enzyme const &e_, const wxPoint &pos, const wxSize &size, long style, const wxString &name)
      : wxDialog(parent, id, title, pos, size, style, name), e(e_)
{
        wxBoxSizer *vbox = new wxBoxSizer(wxVERTICAL);
        wxBoxSizer *hbox1 = new wxBoxSizer(wxHORIZONTAL);
        wxBoxSizer *hbox2 = new wxBoxSizer(wxHORIZONTAL);
        wxBoxSizer *hbox3 = new wxBoxSizer(wxHORIZONTAL);
        wxBoxSizer *hbox4 = new wxBoxSizer(wxHORIZONTAL);
        wxBoxSizer *hbox5 = new wxBoxSizer(wxHORIZONTAL);
        wxBoxSizer *hbox6 = new wxBoxSizer(wxHORIZONTAL);
        
        wxStaticText *idText = new wxStaticText(this, wxID_ANY, wxT("Enzyme ID:"));
        idCtrl = new wxTextCtrl(this, wxID_EnzymeID, e.id, wxPoint(-1, -1), wxSize(-1, -1));
        hbox1->Add(idText, 0, wxEXPAND | wxTOP | wxLEFT, 20);
        hbox1->Add(idCtrl, 0, wxEXPAND | wxTOP | wxRIGHT, 20);
        Connect(wxID_EnzymeID, wxEVT_TEXT, 
                wxCommandEventHandler(EnzymeDialog::OnTextID));
        
        wxStaticText *patternText = new wxStaticText(this, wxID_ANY, wxT("Pattern:"));
        patternCtrl = new wxTextCtrl(this, wxID_EnzymePattern, e.pattern, wxPoint(-1, -1), wxSize(-1, -1));
        hbox2->Add(patternText, 0, wxEXPAND | wxLEFT, 20);
        hbox2->Add(patternCtrl, 0, wxEXPAND | wxRIGHT, 20);
        Connect(wxID_EnzymePattern, wxEVT_TEXT, 
                wxCommandEventHandler(EnzymeDialog::OnTextPattern));
        
        wxStaticText *fnText = new wxStaticText(this, wxID_ANY, wxT("False negative (%):"));
        fnCtrl = new wxTextCtrl(this, wxID_EnzymeFN, e.fn, wxPoint(-1, -1), wxSize(-1, -1));
        hbox3->Add(fnText, 0, wxEXPAND | wxLEFT, 20);
        hbox3->Add(fnCtrl, 0, wxEXPAND | wxRIGHT, 20);
        Connect(wxID_EnzymeFN, wxEVT_TEXT, 
                wxCommandEventHandler(EnzymeDialog::OnTextFN));
        
        wxStaticText *fpText = new wxStaticText(this, wxID_ANY, wxT("False Positive rate (per 100 Kb):"));
        fpCtrl = new wxTextCtrl(this, wxID_EnzymeFP, e.fp, wxPoint(-1, -1), wxSize(-1, -1));
        hbox4->Add(fpText, 0, wxEXPAND | wxLEFT, 20);
        hbox4->Add(fpCtrl, 0, wxEXPAND | wxRIGHT, 20);
        Connect(wxID_EnzymeFP, wxEVT_TEXT, 
                wxCommandEventHandler(EnzymeDialog::OnTextFP));
        
        wxStaticText *labelText = new wxStaticText(this, wxID_ANY, wxT("Label:"));
        labelCtrl = new wxTextCtrl(this, wxID_EnzymeLabel, e.label, wxPoint(-1, -1), wxSize(-1, -1));
        hbox5->Add(labelText, 0, wxEXPAND | wxBOTTOM | wxLEFT, 20);
        hbox5->Add(labelCtrl, 0, wxEXPAND | wxBOTTOM | wxRIGHT, 20);
        Connect(wxID_EnzymeLabel, wxEVT_TEXT, 
                wxCommandEventHandler(EnzymeDialog::OnTextLabel));
        
        wxButton *ok = new wxButton(this, wxID_OK, wxT("Ok"));
        wxButton *cancel = new wxButton(this, wxID_CANCEL, wxT("Cancel"));
        hbox6->Add(ok, 0, wxEXPAND | wxBOTTOM | wxLEFT, 20);
        hbox6->Add(cancel, 0, wxEXPAND | wxBOTTOM | wxLEFT, 20);
        
        vbox->Add(hbox1);
        vbox->Add(hbox2);
        vbox->Add(hbox3);
        vbox->Add(hbox4);
        vbox->Add(hbox5);
        vbox->Add(hbox6);
        
        SetSizer(vbox);
}

void EnzymeDialog::OnTextID(wxCommandEvent& event) 
{
        e.id = idCtrl->GetValue();
}

void EnzymeDialog::OnTextPattern(wxCommandEvent& event) 
{
        e.pattern = patternCtrl->GetValue();
}

void EnzymeDialog::OnTextFN(wxCommandEvent& event) 
{
        e.fn = fnCtrl->GetValue();
}

void EnzymeDialog::OnTextFP(wxCommandEvent& event) 
{
        e.fp = fpCtrl->GetValue();
}

void EnzymeDialog::OnTextLabel(wxCommandEvent& event) 
{
        e.label = labelCtrl->GetValue();
}
