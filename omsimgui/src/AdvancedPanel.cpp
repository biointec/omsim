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
#include "AdvancedPanel.hpp"
#include "TagPanel.hpp"

#include <wx/scrolwin.h>


AdvancedPanel::AdvancedPanel(wxWindow *parent, wxWindowID id, configuration &c_)
      : wxPanel(parent, id), c(c_)
{
        wxBoxSizer *mainbox = new wxBoxSizer(wxHORIZONTAL);
        
        /*
                ctrl box
        */
        wxScrolledWindow *scrollbox = new wxScrolledWindow(this, wxID_ANY);
        
        wxBoxSizer *vbox = new wxBoxSizer(wxVERTICAL);
        
        for (auto &entry : c.entries) {
                auto &tag = entry.tag;
                auto &val = entry.val;
                auto &str = entry.str;
                if (entry.type == ADVANCED) {
                        tags.push_back(new TagPanel(scrollbox, vbox, tag, val, str));
                        }
        }
        
        scrollbox->SetSizerAndFit(vbox);
        scrollbox->FitInside();
        scrollbox->SetScrollRate(5, 5);
        mainbox->Add(scrollbox, 0, wxEXPAND | wxALIGN_CENTER | wxALL, 5);
        
        SetSizerAndFit(mainbox);
}

void AdvancedPanel::update(){
        for (auto tag : tags) {
                tag->update();
        }
}
