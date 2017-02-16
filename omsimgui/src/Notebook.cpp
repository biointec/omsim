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
#include "Notebook.hpp"
#include "BasicPanel.hpp"
#include "AdvancedPanel.hpp"

Notebook::Notebook(wxWindow *parent, wxWindowID id, const wxString &title, const configuration &c_, const std::map<wxString, enzyme> &enzymes_, const wxPoint &pos, const wxSize &size, long style, const wxString &name)
      : wxDialog(parent, id, title, pos, size, style, name), c(c_), enzymes(enzymes_)
{
        wxNotebook *nb = new wxNotebook(this, -1, wxPoint(-1, -1), 
                wxSize(-1, -1), wxNB_TOP);
        
        BasicPanel *bpanel = new BasicPanel(nb, -1, c, enzymes);
        nb->AddPage(bpanel, wxT("Basic"));
        
        AdvancedPanel *apanel = new AdvancedPanel(nb, -1, c);
        nb->AddPage(apanel, wxT("Advanced"));
        
        Center();
}
