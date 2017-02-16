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

