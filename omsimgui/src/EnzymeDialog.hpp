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
#ifndef ENZYMEDIALOG_HPP
#define ENZYMEDIALOG_HPP

#include "wx.hpp"
#include <wx/dialog.h>

#include "enzyme.hpp"

class EnzymeDialog : public wxDialog
{
        private:
                wxTextCtrl *idCtrl;
                wxTextCtrl *patternCtrl;
                wxTextCtrl *fnCtrl;
                wxTextCtrl *fpCtrl;
                wxTextCtrl *labelCtrl;
                
                enzyme e;
        public:
                EnzymeDialog(wxWindow *parent, wxWindowID id, const wxString &title, enzyme const &e_=enzyme(wxString(), wxString(), wxString(), wxString(), wxString()), const wxPoint &pos=wxDefaultPosition, const wxSize &size=wxDefaultSize, long style=wxDEFAULT_DIALOG_STYLE, const wxString &name=wxDialogNameStr);
                
                enzyme GetEnzyme() {return e;}
                
                void OnTextID(wxCommandEvent& event);
                void OnTextPattern(wxCommandEvent& event);
                void OnTextFN(wxCommandEvent& event);
                void OnTextFP(wxCommandEvent& event);
                void OnTextLabel(wxCommandEvent& event);
};

enum {
        wxID_EnzymeID = wxID_HIGHEST + 1,
        wxID_EnzymePattern = wxID_HIGHEST + 2,
        wxID_EnzymeFN = wxID_HIGHEST + 3,
        wxID_EnzymeFP = wxID_HIGHEST + 4,
        wxID_EnzymeLabel = wxID_HIGHEST + 5
};

#endif
