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
#include "EnzymeDialog.hpp"

#include <wx/stattext.h>
#include <wx/sizer.h>

EnzymeDialog::EnzymeDialog(wxWindow *parent, wxWindowID id, const wxString &title, enzyme const &e_, const wxPoint &pos, const wxSize &size, long style, const wxString &name)
      : wxDialog(parent, id, title, pos, size, style, name), e(e_)
{
        wxBoxSizer *vbox = new wxBoxSizer(wxVERTICAL);
        wxBoxSizer *hbox = new wxBoxSizer(wxHORIZONTAL);
        
        wxFlexGridSizer *grid = new wxFlexGridSizer(2, 10, 10);
        
        wxStaticText *idText = new wxStaticText(this, wxID_ANY, wxT("Enzyme ID:"));
        idCtrl = new wxTextCtrl(this, wxID_EnzymeID, e.id, wxPoint(-1, -1), wxSize(-1, -1));
        grid->Add(idText);
        grid->Add(idCtrl);
        Connect(wxID_EnzymeID, wxEVT_TEXT, 
                wxCommandEventHandler(EnzymeDialog::OnTextID));
        
        wxStaticText *patternText = new wxStaticText(this, wxID_ANY, wxT("Pattern:"));
        patternCtrl = new wxTextCtrl(this, wxID_EnzymePattern, e.pattern, wxPoint(-1, -1), wxSize(-1, -1));
        grid->Add(patternText);
        grid->Add(patternCtrl);
        Connect(wxID_EnzymePattern, wxEVT_TEXT, 
                wxCommandEventHandler(EnzymeDialog::OnTextPattern));
        
        wxStaticText *fnText = new wxStaticText(this, wxID_ANY, wxT("False negative rate (per nick):"));
        fnCtrl = new wxTextCtrl(this, wxID_EnzymeFN, e.fn, wxPoint(-1, -1), wxSize(-1, -1));
        grid->Add(fnText);
        grid->Add(fnCtrl);
        Connect(wxID_EnzymeFN, wxEVT_TEXT, 
                wxCommandEventHandler(EnzymeDialog::OnTextFN));
        
        wxStaticText *fpText = new wxStaticText(this, wxID_ANY, wxT("False positive rate (per 100 Kb):"));
        fpCtrl = new wxTextCtrl(this, wxID_EnzymeFP, e.fp, wxPoint(-1, -1), wxSize(-1, -1));
        grid->Add(fpText);
        grid->Add(fpCtrl);
        Connect(wxID_EnzymeFP, wxEVT_TEXT, 
                wxCommandEventHandler(EnzymeDialog::OnTextFP));
        
        wxStaticText *labelText = new wxStaticText(this, wxID_ANY, wxT("Label:"));
        labelCtrl = new wxTextCtrl(this, wxID_EnzymeLabel, e.label, wxPoint(-1, -1), wxSize(-1, -1));
        grid->Add(labelText);
        grid->Add(labelCtrl);
        Connect(wxID_EnzymeLabel, wxEVT_TEXT, 
                wxCommandEventHandler(EnzymeDialog::OnTextLabel));
        
        wxButton *ok = new wxButton(this, wxID_OK, wxT("Ok"));
        wxButton *cancel = new wxButton(this, wxID_CANCEL, wxT("Cancel"));
        hbox->Add(ok, 0, wxEXPAND | wxALL, 20);
        hbox->Add(cancel, 0, wxEXPAND | wxALL, 20);
        
        vbox->Add(grid, 0, wxEXPAND | wxALL, 20);
        vbox->Add(hbox);
        
        SetSizerAndFit(vbox);
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
