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
#ifndef BASICPANEL_HPP
#define BASICPANEL_HPP

#include <map>
#include "wx.hpp"
#include "configuration.hpp"

class TagPanel;

class BasicPanel : public wxPanel
{
        private:
                configuration &c;
                wxTextCtrl *nameCtrl;
                wxListBox *fastaListBox;
                wxListBox *xmlListBox;
                wxCheckListBox *enzymeCheckListBox;
                wxTextCtrl *sizeMeanCtrl;
                wxTextCtrl *sizeSDCtrl;
                wxCheckBox *circularCheckBox;
                std::vector<TagPanel*> tags;
        public:
                BasicPanel(wxWindow *parent, wxWindowID id, configuration &c_);
                void update();
                void OnNewEnz(wxCommandEvent& event);
                void OnEnzDblClick(wxCommandEvent& event);
                void OnEnzCheck(wxCommandEvent& event);
                void OnName(wxCommandEvent& Event);
                void OnSizeMean(wxCommandEvent& Event);
                void OnSizeSD(wxCommandEvent& Event);
                void OnCircularCheck(wxCommandEvent& Event);
                
                void addFasta(wxString fasta);
                void removeFasta(wxString fasta);
                void clearFasta();
};

enum {
        wxID_FastaListBox = wxID_HIGHEST + 1,
        wxID_EnzymeCheckListBox = wxID_HIGHEST + 2,
        wxID_SizeMean = wxID_HIGHEST + 3,
        wxID_SizeSD = wxID_HIGHEST + 4,
        wxID_CircularCheckBox = wxID_HIGHEST + 5,
        wxID_Name = wxID_HIGHEST + 6,
        wxID_New_Enz = wxID_HIGHEST + 7
};

#endif
