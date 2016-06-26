#include "BasicPanel.hpp"
#include "ListBoxPanel.hpp"
#include "EnzymePanel.hpp"

BasicPanel::BasicPanel(wxWindow *parent, wxWindowID id)
      : wxPanel(parent, id)
{
        wxBoxSizer *mainbox = new wxBoxSizer(wxVERTICAL);
        
        /*
                xml box
        */
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
        
        /*
                fasta box
        */
        wxBoxSizer *fastabox = new wxBoxSizer(wxVERTICAL);
        wxStaticText *fastaTitle = new wxStaticText(this, wxID_ANY, wxT("Genome files"));
        
        wxPanel * fastaPanel = new wxPanel(this, -1);
        wxBoxSizer *flbbox = new wxBoxSizer(wxHORIZONTAL);
        fastaListBox = new wxListBox(fastaPanel, ID_FastaListBox, wxPoint(-1, -1), wxSize(-1, -1)); 
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
        enzymeCheckListBox = new wxCheckListBox(ePanel, ID_EnzymeCheckListBox, wxPoint(-1, -1), wxSize(-1, -1)); 
        eclbbox->Add(enzymeCheckListBox, 5, wxEXPAND | wxALL, 20);
        enzymePanel = new EnzymePanel(ePanel, enzymeCheckListBox);
        eclbbox->Add(enzymePanel, 1, wxEXPAND | wxRIGHT, 10);
        ePanel->SetSizer(eclbbox);
        ePanel->Center();
        
        Connect(wxEVT_COMMAND_LISTBOX_DOUBLECLICKED, 
                wxCommandEventHandler(BasicPanel::OnEnzDblClick));
        
        enzymebox->Add(enzymeTitle);
        enzymebox->Add(ePanel, 1, wxEXPAND);
        
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
        
        
        
        mainbox->Add(xmlbox);
        mainbox->Add(fastabox);
        mainbox->Add(enzymebox);
        mainbox->Add(lengthbox);
        
        SetSizer(mainbox);
}

void BasicPanel::OnEnzDblClick(wxCommandEvent& event)
{
        enzymePanel->OnEnzDblClick(event);
}

