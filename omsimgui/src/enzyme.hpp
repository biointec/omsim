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
#ifndef ENZYME_HPP
#define ENZYME_HPP

#include "wx.hpp"

struct enzyme {
        wxString id;
        wxString pattern;
        wxString label;
        wxString fn;
        wxString fp;
        bool checked;
        
        enzyme(wxString const &id_ = wxString(), wxString const &pattern_ = wxString(), wxString const &label_ = wxString(), wxString const &fn_ = wxString(), wxString const &fp_ = wxString())
        {
                wxString vals [5] = {wxT("BspQI"), wxT("GCTCTTC"), wxT("label_0"), wxT("0.15"), wxT("1.0")};
                wxString vals_ [5] = {id_, pattern_, label_, fn_, fp_};
                for (auto i = 0; i < 5; ++i) {
                        if (vals_[i] != wxString()) {
                                vals[i] = vals_[i];
                        }
                }
                id = vals[0];
                pattern = vals[1];
                label = vals[2];
                fn = vals[3];
                fp = vals[4];
                checked = true;
        }
};

#endif
