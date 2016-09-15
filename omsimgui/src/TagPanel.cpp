#include "TagPanel.hpp"

TagPanel::TagPanel(wxWindow *parent, wxSizer *sizer, wxString const &tag_, wxString &val_, wxString const &lab_)
      : wxPanel(parent, wxID_ANY), tag(tag_), val(val_), lab(lab_)
{
        wxBoxSizer *hbox = new wxBoxSizer(wxHORIZONTAL);
        label = new wxStaticText(this, wxID_ANY, lab + wxT(":"));
        ctrl = new wxTextCtrl(this, wxID_Ctrl, val, wxPoint(-1, -1), wxSize(-1, -1));
        hbox->Add(label, 1, wxEXPAND | wxRIGHT, 20);
        hbox->Add(ctrl, 0, wxEXPAND | wxALIGN_RIGHT | wxRIGHT, 5);
        
        Connect(wxID_Ctrl, wxEVT_TEXT,
                wxCommandEventHandler(TagPanel::OnText));
        
        SetSizerAndFit(hbox);
        sizer->Add(this, 0, wxEXPAND);
}

void TagPanel::OnText(wxCommandEvent& event) 
{
        val = ctrl->GetValue();
}

void TagPanel::update() {
        ctrl->SetValue(val);
}
