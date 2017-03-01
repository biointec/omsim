/*
        Copyright (C) 2016 Giles Miclotte (giles.miclotte@ugent.be)
        This file is part of OMSim

        This program is free software; you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation; either version 2 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program; if not, write to the
        Free Software Foundation, Inc.,
        59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
*/
#include "BasicPanel.hpp"
#include "ListBoxPanel.hpp"
#include "EnzymeDialog.hpp"
#include "TagPanel.hpp"
#include <algorithm> //find

BasicPanel::BasicPanel(wxWindow *parent, wxWindowID id, configuration &c_/*, std::map<wxString, enzyme> &enzymes_*/)
      : wxPanel(parent, id), c(c_)/*, enzymes(enzymes_)*/
{
        wxBoxSizer *mainbox = new wxBoxSizer(wxVERTICAL);
        
        /*
                name box
        */
        wxBoxSizer *namebox = new wxBoxSizer(wxVERTICAL);
        wxStaticText *nameTitle = new wxStaticText(this, wxID_ANY, wxT("Experiment name"));
        nameCtrl = new wxTextCtrl(this, wxID_Name, c.get(wxT("name")), wxPoint(-1, -1), wxSize(-1, -1));
        namebox->Add(nameTitle);
        namebox->Add(nameCtrl, 0, wxEXPAND | wxALL, 20);
        
        Connect(wxID_Name, wxEVT_TEXT,
                wxCommandEventHandler(BasicPanel::OnName));
        
        /*
                fasta box
        */
        wxBoxSizer *fastabox = new wxBoxSizer(wxVERTICAL);
        wxStaticText *fastaTitle = new wxStaticText(this, wxID_ANY, wxT("Genome files"));
        
        wxPanel * fastaPanel = new wxPanel(this, -1);
        wxBoxSizer *flbbox = new wxBoxSizer(wxHORIZONTAL);
        fastaListBox = new wxListBox(fastaPanel, wxID_FastaListBox, wxPoint(-1, -1), wxSize(-1, -1)); 
        flbbox->Add(fastaListBox, 5, wxEXPAND | wxALL, 20);
        ListBoxPanel *fastaBtnPanel = new ListBoxPanel(fastaPanel, fastaListBox, wxT("Fasta"), wxT("fasta"));
        flbbox->Add(fastaBtnPanel, 1, wxEXPAND | wxRIGHT, 10);
        fastaPanel->SetSizerAndFit(flbbox);
        fastaPanel->Center();
        
        circularCheckBox = new wxCheckBox(this, wxID_CircularCheckBox, wxT("Circular Genome"), wxPoint(-1, -1), wxSize(-1, -1));
        circularCheckBox->SetValue(c.circular);
        Connect(wxID_CircularCheckBox, wxEVT_CHECKBOX,
                wxCommandEventHandler(BasicPanel::OnCircularCheck));
        
        fastabox->Add(fastaTitle, 0);
        fastabox->Add(fastaPanel, 1, wxEXPAND);
        fastabox->Add(circularCheckBox, 0, wxEXPAND);
        
        /*
                enzyme box
        */
        wxBoxSizer *enzymebox = new wxBoxSizer(wxVERTICAL);
        wxStaticText *enzymeTitle = new wxStaticText(this, wxID_ANY, wxT("Enzymes"));
        
        wxPanel * ePanel = new wxPanel(this, -1);
        wxBoxSizer *eclbbox = new wxBoxSizer(wxHORIZONTAL);
        
        enzymeCheckListBox = new wxCheckListBox(ePanel, wxID_EnzymeCheckListBox, wxPoint(-1, -1), wxSize(-1, -1)); 
        eclbbox->Add(enzymeCheckListBox, 5, wxEXPAND | wxALL, 20);
        ePanel->SetSizerAndFit(eclbbox);
        ePanel->Center();
        
        auto enzymeButton = new wxButton(this, wxID_New_Enz, wxT("Add enzyme"));
        Connect(wxID_New_Enz, wxEVT_COMMAND_BUTTON_CLICKED, 
                wxCommandEventHandler(BasicPanel::OnNewEnz));
        enzymebox->Add(enzymeTitle);
        enzymebox->Add(ePanel, 1, wxEXPAND);
        enzymebox->Add(enzymeButton, 0);
        
        Connect(wxID_EnzymeCheckListBox, wxEVT_COMMAND_LISTBOX_DOUBLECLICKED, 
                wxCommandEventHandler(BasicPanel::OnEnzDblClick));
        Connect(wxID_EnzymeCheckListBox, wxEVT_COMMAND_CHECKLISTBOX_TOGGLED,
                wxCommandEventHandler(BasicPanel::OnEnzCheck));
        /*
                settings box
        */
        wxBoxSizer *settingsbox = new wxBoxSizer(wxVERTICAL);
        wxStaticText *settingsTitle = new wxStaticText(this, wxID_ANY, wxT("Settings"));
        settingsbox->Add(settingsTitle);
        for (auto &entry : c.entries) {
                auto &tag = entry.tag;
                auto &val = entry.val;
                auto &str = entry.str;
                if (entry.type == BASIC) {
                        tags.push_back(new TagPanel(this, settingsbox, tag, val, str));
                }
        }
        /*
                main box
        */
        mainbox->Add(namebox, 0, wxEXPAND | wxALL, 10);
        mainbox->Add(fastabox, 0, wxEXPAND | wxALL, 10);
        mainbox->Add(enzymebox, 0, wxEXPAND | wxALL, 10);
        mainbox->Add(settingsbox, 0, wxEXPAND | wxALL, 10);
        
        SetSizerAndFit(mainbox);
        
        update();
}

void BasicPanel::addFasta(wxString fasta) {
        c.files.push_back(fasta);
        update();
}

void BasicPanel::removeFasta(wxString fasta) {
        auto it = std::find(c.files.begin(), c.files.end(), fasta);
        if (it != c.files.end()) {
                c.files.erase(it);
        }
        update();
}

void BasicPanel::clearFasta() {
        c.files.clear();
        update();
}

void BasicPanel::update() {
        fastaListBox->Clear();
        for (auto f : c.files) {
                fastaListBox->Append(f);
        }
        
        enzymeCheckListBox->Clear();
        for (auto kv : c.enzymes) {
                enzymeCheckListBox->Append(kv.first);
                if (kv.second.checked) {
                        enzymeCheckListBox->Check(enzymeCheckListBox->FindString(kv.first));
                }
        }
        for (auto tag : tags) {
                tag->update();
        }
}

void BasicPanel::OnEnzDblClick(wxCommandEvent& event)
{
        int sel = enzymeCheckListBox->GetSelection();
        if (sel != -1) {
                wxString id = enzymeCheckListBox->GetString(sel);
                EnzymeDialog dlg(this, wxID_ANY, wxT("Change enzyme details"), c.enzymes[id]);
                if (dlg.ShowModal() == wxID_CANCEL) {
                        return;
                } else {
                        enzyme e = dlg.GetEnzyme();
                        c.enzymes[e.id] = e;
                        enzymeCheckListBox->Delete(sel);
                        enzymeCheckListBox->Insert(e.id, sel);
                        if (e.checked) {
                                enzymeCheckListBox->Check(enzymeCheckListBox->FindString(e.id));
                        }
                }
        }
}

void BasicPanel::OnName(wxCommandEvent& Event)
{
        c.set(wxT("name"), nameCtrl->GetValue());
}

void BasicPanel::OnCircularCheck(wxCommandEvent& event) 
{
        c.circular = circularCheckBox->IsChecked();
}

void BasicPanel::OnEnzCheck(wxCommandEvent& event)
{
        auto item = event.GetInt();
        auto e = enzymeCheckListBox->GetString(item);
        c.enzymes[e].checked = enzymeCheckListBox->IsChecked(item);
}

void BasicPanel::OnNewEnz(wxCommandEvent& event)
{
        EnzymeDialog dlg(this, wxID_ANY, wxT("Change enzyme details"), enzyme());
        if (dlg.ShowModal() == wxID_CANCEL) {
                return;
        } else {
                enzyme e = dlg.GetEnzyme();
                c.enzymes[e.id] = e;
                update();
        }
}
