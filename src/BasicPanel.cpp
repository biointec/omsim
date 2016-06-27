#include "BasicPanel.hpp"
#include "ListBoxPanel.hpp"
#include "EnzymeDialog.hpp"

BasicPanel::BasicPanel(wxWindow *parent, wxWindowID id, configuration &c_, std::map<wxString, enzyme> &enzymes_)
      : wxPanel(parent, id), c(c_), enzymes(enzymes_)
{
        wxBoxSizer *mainbox = new wxBoxSizer(wxVERTICAL);
        /*
                fasta box
        */
        wxBoxSizer *fastabox = new wxBoxSizer(wxVERTICAL);
        wxStaticText *fastaTitle = new wxStaticText(this, wxID_ANY, wxT("Genome files"));
        
        wxPanel * fastaPanel = new wxPanel(this, -1);
        wxBoxSizer *flbbox = new wxBoxSizer(wxHORIZONTAL);
        fastaListBox = new wxListBox(fastaPanel, wxID_FastaListBox, wxPoint(-1, -1), wxSize(-1, -1)); 
        flbbox->Add(fastaListBox, 5, wxEXPAND | wxALL, 20);
        ListBoxPanel *fastaBtnPanel = new ListBoxPanel(fastaPanel, fastaListBox, "Fasta", "fasta");
        flbbox->Add(fastaBtnPanel, 1, wxEXPAND | wxRIGHT, 10);
        fastaPanel->SetSizer(flbbox);
        fastaPanel->Center();
        
        fastabox->Add(fastaTitle);
        fastabox->Add(fastaPanel, 1, wxEXPAND);
        
        /*
                enzyme box
        */
        wxBoxSizer *enzymebox = new wxBoxSizer(wxVERTICAL);
        wxStaticText *enzymeTitle = new wxStaticText(this, wxID_ANY, wxT("Enzymes"));
        
        wxPanel * ePanel = new wxPanel(this, -1);
        wxBoxSizer *eclbbox = new wxBoxSizer(wxHORIZONTAL);
        enzymeCheckListBox = new wxCheckListBox(ePanel, wxID_EnzymeCheckListBox, wxPoint(-1, -1), wxSize(-1, -1)); 
        eclbbox->Add(enzymeCheckListBox, 5, wxEXPAND | wxALL, 20);
        ePanel->SetSizer(eclbbox);
        ePanel->Center();
        
        enzymebox->Add(enzymeTitle);
        enzymebox->Add(ePanel, 1, wxEXPAND);
        
        Connect(wxID_EnzymeCheckListBox, wxEVT_COMMAND_LISTBOX_DOUBLECLICKED, 
                wxCommandEventHandler(BasicPanel::OnEnzDblClick));
                
        /*
                length box
        */
        wxBoxSizer *lengthbox = new wxBoxSizer(wxVERTICAL);
        wxStaticText *lengthTitle = new wxStaticText(this, wxID_ANY, wxT("Size distribution"));
        wxBoxSizer *sizedistbox = new wxBoxSizer(wxHORIZONTAL);
        wxStaticText *meanText = new wxStaticText(this, wxID_ANY, wxT("Mean:"));
        wxTextCtrl *mean = new wxTextCtrl(this, -1, wxT(""), wxPoint(-1, -1), wxSize(-1, -1));
        wxStaticText *stdText = new wxStaticText(this, wxID_ANY, wxT("Standard deviation:"));
        wxTextCtrl *std =  new wxTextCtrl(this, -1, wxT(""), wxPoint(-1, -1), wxSize(-1, -1));
        sizedistbox->Add(meanText, 0, wxEXPAND | wxALL, 20);
        sizedistbox->Add(mean, 0, wxEXPAND | wxTOP | wxBOTTOM, 20);
        sizedistbox->Add(stdText, 0, wxEXPAND | wxALL, 20);
        sizedistbox->Add(std, 0, wxEXPAND | wxRIGHT | wxTOP | wxBOTTOM, 20);
        lengthbox->Add(lengthTitle);
        lengthbox->Add(sizedistbox);
        
        
        
        mainbox->Add(fastabox);
        mainbox->Add(enzymebox);
        mainbox->Add(lengthbox);
        
        SetSizer(mainbox);
        
        update();
}

void BasicPanel::update() {
        for (auto f : c.files) {
                fastaListBox->Append(f);
        }
        
        for (auto kv : enzymes) {
                enzymeCheckListBox->Append(kv.first);
        }
        
        for (auto kv : c.enzymes) {
                int idx = enzymeCheckListBox->FindString(kv.first);
                if (idx != wxNOT_FOUND) {
                        enzymeCheckListBox->Check(idx);
                }
        }
}

void BasicPanel::OnEnzDblClick(wxCommandEvent& event)
{
        int sel = enzymeCheckListBox->GetSelection();
        if (sel != -1) {
                wxString id = enzymeCheckListBox->GetString(sel);
                EnzymeDialog dlg(this, wxID_ANY, _("Change label"), enzymes[id]);
                if (dlg.ShowModal() == wxID_CANCEL) {
                        return;
                } else {
                        enzyme e = dlg.GetEnzyme();
                        enzymes[e.id] = e;
                        enzymeCheckListBox->Delete(sel);
                        enzymeCheckListBox->Insert(e.id, sel);
                }
        }
}
