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
#ifndef TAGPANEL_HPP
#define TAGPANEL_HPP

#include "wx.hpp"

class TagPanel : public wxPanel
{
        private:
                wxStaticText *label;
                wxTextCtrl *ctrl;
                
                wxString const &tag;
                wxString &val;
                wxString const &lab;
        public:
                TagPanel(wxWindow *parent, wxSizer *grid, wxString const &tag_, wxString &val_, wxString const &lab_);
                void update();
                void OnText(wxCommandEvent& event);
};

enum {
        wxID_Ctrl = wxID_HIGHEST + 1
};

#endif
