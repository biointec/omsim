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
#ifndef MAINFRAME_HPP
#define MAINFRAME_HPP

#include "wx.hpp"
#include <wx/dialog.h>
#include <wx/notebook.h>

#include <map>

#include "configuration.hpp"

class BasicPanel;
class AdvancedPanel;
class MainFrame : public wxFrame
{
        private:
                configuration c;
                BasicPanel *bpanel;
                AdvancedPanel *apanel;
        public:
                MainFrame(const wxString& title);
                void update();
                void OnNew(wxCommandEvent& event);
                void OnOpen(wxCommandEvent& event);
                void OnSave(wxCommandEvent& event);
                void OnCopy(wxCommandEvent& event);
                void OnQuit(wxCommandEvent& event);
};

enum {
        wxID_CNEW = wxID_HIGHEST + 1,
        wxID_COPEN = wxID_HIGHEST + 2,
        wxID_CSAVE = wxID_HIGHEST + 3,
        wxID_CCOPY = wxID_HIGHEST + 4
};
#endif
