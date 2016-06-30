#ifndef ENZYME_HPP
#define ENZYME_HPP

#include "wx.hpp"

struct enzyme {
        wxString id;
        wxString pattern;
        wxString label;
        wxString fn;
        wxString fp;
        
        enzyme(wxString const &id_ = "", wxString const &pattern_ = "", wxString const &label_ = "", wxString const &fn_ = "", wxString const &fp_ = "")
        {
                wxString vals [5] = {"Enzyme ID", "ACGT", "label_0", "0.15", "1.5"};
                wxString vals_ [5] = {id_, pattern_, label_, fn_, fp_};
                for (auto i = 0; i < 5; ++i) {
                        if (vals_[i] != "") {
                                vals[i] = vals_[i];
                        }
                }
                id = vals[0];
                pattern = vals[1];
                label = vals[2];
                fn = vals[3];
                fp = vals[4];
        }
};

#endif
