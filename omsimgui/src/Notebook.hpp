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
#ifndef NOTEBOOK_HPP
#define NOTEBOOK_HPP

#include "wx.hpp"
#include <wx/dialog.h>
#include <wx/notebook.h>

#include <map>

#include "configuration.hpp"

class Notebook : public wxDialog
{
        private:
                configuration c;
                //std::map<wxString, enzyme> enzymes;
        public:
                Notebook(wxWindow *parent, wxWindowID id, const wxString &title, const configuration &c_=configuration(), const wxPoint &pos=wxDefaultPosition, const wxSize &size=wxDefaultSize, long style=wxDEFAULT_DIALOG_STYLE, const wxString &name=wxDialogNameStr);
                configuration GetConfiguration() {return c;}
};

#endif
