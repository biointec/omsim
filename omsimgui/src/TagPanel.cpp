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
